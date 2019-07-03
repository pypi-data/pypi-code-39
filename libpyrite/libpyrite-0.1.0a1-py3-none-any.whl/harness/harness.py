from abc import ABC, abstractmethod, abstractproperty
from collections import defaultdict
from functools import singledispatch

import attr
import torch
from torch import nn
from torch import optim
from torch.utils.data import DataLoader

from ._utils import get_tqdm_aliases


class Callback:
    def on_epoch_begin(self, harness, epoch):
        pass

    def on_epoch_end(self, harness, epoch, logs=None):
        pass

    def on_fit_batch_begin(self, harness, epoch, batch, logs=None):
        pass

    def on_fit_batch_end(self, harness, epoch, batch, logs=None):
        pass

    def on_evaluate_batch_begin(self, harness, batch, logs=None):
        pass

    def on_evaluate_batch_end(self, harness, batch, logs=None):
        pass

    def on_predict_batch_begin(self, harness, batch, logs=None):
        pass

    def on_predict_batch_end(self, harness, batch, logs=None):
        pass

    def on_fit_begin(self, harness, logs=None):
        pass

    def on_fit_end(self, harness, logs=None):
        pass

    def on_evaluate_begin(self, harness, logs=None):
        pass

    def on_evaluate_end(self, harness, logs=None):
        pass

    def on_predict_begin(self, harness, logs=None):
        pass

    def on_predict_end(self, harness, logs=None):
        pass


class AbstractModelHarnessMixin(ABC):
    @abstractproperty
    def device(self):
        pass

    def fit(
        self,
        producer,
        epochs=1,
        val_producer=None,
        callbacks=None,
        verbose=True,
        notebook_mode=False,
    ):
        callbacks = callbacks or []
        tqdm, _ = get_tqdm_aliases(notebook_mode)

        for c in callbacks:
            c.on_fit_begin(self)

        history = []
        for epoch in range(epochs):
            with tqdm(
                total=estimate_producer_epoch_sample_size(producer),
                desc="Epoch {}".format(epoch + 1),
                unit="sample",
                disable=not verbose,
            ) as t:
                self.train()

                for c in callbacks:
                    c.on_epoch_begin(self, epoch)

                epoch_history = []
                metric_averages = {}

                for i, batch in enumerate(producer, 0):
                    for c in callbacks:
                        c.on_fit_batch_begin(self, epoch, i)

                    batch_metrics, batch_size = self._fit_batch(batch)
                    batch_metrics = {k: v.item() for k, v in batch_metrics.items()}
                    metric_averages = _update_means(
                        batch_metrics, metric_averages, i + 1
                    )

                    summary = {"metrics": metric_averages, "batch_size": batch_size}
                    epoch_history.append(summary)

                    for c in callbacks:
                        c.on_fit_batch_end(self, epoch, i, logs=summary)

                    t.set_postfix(**metric_averages)
                    t.update(batch_size)

                if val_producer is not None:
                    val_metrics = self.evaluate(
                        val_producer,
                        callbacks=callbacks,
                        verbose=False,
                        notebook_mode=notebook_mode,
                    )
                    val_metrics = {
                        "val_{}".format(k): v for k, v in val_metrics.items()
                    }
                    val_metrics.update(metric_averages)
                    t.set_postfix(**val_metrics)

                summary = {"metrics": metric_averages, "history": epoch_history}
                if val_producer is not None:
                    summary["metrics"] = val_metrics
                history.append(summary)

                for c in callbacks:
                    c.on_epoch_end(self, epoch, logs=summary)

        for c in callbacks:
            c.on_fit_end(self)

        return history

    def fit_batch(self, batch):
        self.train()
        res, _ = self._fit_batch(batch)
        return {k: v.item() for k, v in res.items()}

    @abstractmethod
    def _fit_batch(self, batch):
        pass

    def evaluate(self, producer, callbacks=None, verbose=True, notebook_mode=False):
        callbacks = callbacks or []
        tqdm, _ = get_tqdm_aliases(notebook_mode)

        self.eval()

        for c in callbacks:
            c.on_evaluate_begin(self)

        metric_averages = {}
        with tqdm(
            total=producer.batch_size * len(producer),
            unit="sample",
            disable=not verbose,
        ) as t:
            for i, batch in enumerate(producer, 0):
                for c in callbacks:
                    c.on_evaluate_batch_begin(self, i)

                batch_metrics, batch_size = self._evaluate_batch(batch)
                batch_metrics = {k: v.item() for k, v in batch_metrics.items()}
                metric_averages = _update_means(batch_metrics, metric_averages, i + 1)

                for c in callbacks:
                    c.on_evaluate_batch_end(
                        self,
                        i,
                        logs={"metrics": metric_averages, "batch_size": batch_size},
                    )

                t.set_postfix(**metric_averages)
                t.update(batch_size)

        for c in callbacks:
            c.on_evaluate_end(self)

        return metric_averages

    def evaluate_batch(self, batch):
        self.eval()
        res, _ = self._evaluate_batch(batch)
        return {k: v.item() for k, v in res.items()}

    @abstractmethod
    def _evaluate_batch(self, batch):
        pass

    def predict(self, producer, callbacks=None):
        callbacks = callbacks or []

        self.eval()

        for c in callbacks:
            c.on_predict_begin(self)

        for i, batch in enumerate(producer, 0):
            for c in callbacks:
                c.on_predict_batch_begin(self, i)

            res, batch_size = self._predict_batch(batch)

            for c in callbacks:
                c.on_predict_batch_end(self, i, logs={"batch_size": batch_size})

            yield res, batch_size

        for c in callbacks:
            c.on_predict_end(self)

    def predict_batch(self, batch):
        self.eval()
        return self._predict_batch(batch)

    @abstractmethod
    def _predict_batch(self, batch):
        pass

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def eval(self):
        pass


class AbstractSupervisedLearningHarnessMixin(ABC):
    @abstractmethod
    def split_batch(self, batch):
        pass

    @abstractmethod
    def calculate_loss(self, batch, pred):
        pass

    @abstractmethod
    def calculate_metrics(self, batch, pred):
        pass


@attr.s(frozen=True, slots=True)
class Criterion:
    name = attr.ib()
    exec = attr.ib()


@attr.s(frozen=True, slots=True)
class Metric:
    name = attr.ib()
    exec = attr.ib()


class SupervisedLearningHarness(
    AbstractModelHarnessMixin, AbstractSupervisedLearningHarnessMixin
):
    def __init__(
        self, model, optimizer, criterion, loss_weights=None, metrics=None, device=None
    ):
        if isinstance(criterion, Criterion):
            criterion = [criterion]
        else:
            criterion = list(criterion)

        if loss_weights is None:
            loss_weights = [1] * len(criterion)
        else:
            loss_weights = list(loss_weights)

        if metrics is None:
            metrics = []
            nested = False
        else:
            metrics, nested = _process_metrics_arg(metrics, criterion)

        if len(criterion) != len(loss_weights):
            raise ValueError(
                "Number of criterion must equal the number of loss weights"
            )

        self.model = model
        self.optimizer = optimizer
        self._device = device
        self._criterion = criterion
        self._loss_weights = loss_weights
        self._metrics = metrics
        self._has_nested_metrics = nested
        self._criterion_name_to_index = {
            c.name: i for i, c in enumerate(self._criterion)
        }

    @property
    def device(self):
        return self._device

    def train(self):
        self.model.train()

    def eval(self):
        self.model.eval()

    def split_batch(self, batch):
        input = batch[0]

        target = batch[1:]

        # Attempt to handle nested tuples/lists
        if len(target) == 1 and len(self._criterion) > 1:
            target = target[0]
            if isinstance(target, torch.Tensor):
                raise ValueError("Expected multiple outputs")
        if len(target) != len(self._criterion):
            raise ValueError("Expected number of outputs to equal number of criteria")

        return input, target

    def _fit_batch(self, batch):
        self.optimizer.zero_grad()
        pred, size = self._run_model(batch)
        loss_metrics = self.calculate_loss(batch, pred)

        loss = sum(
            [
                self._loss_weights[self._criterion_name_to_index[k]] * v
                for k, v in loss_metrics.items()
            ]
        )
        loss.backward()
        self.optimizer.step()

        metrics = self.calculate_metrics(batch, pred)
        loss_metrics.update(metrics)
        return loss_metrics, size

    def _evaluate_batch(self, batch):
        with torch.no_grad():
            pred, size = self._run_model(batch)
            loss_metrics = self.calculate_loss(batch, pred)
            metrics = self.calculate_metrics(batch, pred)

            loss_metrics.update(metrics)
            return loss_metrics, size

    def _predict_batch(self, batch):
        with torch.no_grad():
            return self._run_model(batch)

    def _run_model(self, batch):
        input, _ = self.split_batch(batch)
        return self.model(input.to(self.device)), len(input)

    def calculate_loss(self, batch, prediction):
        _, target = self.split_batch(batch)

        if isinstance(prediction, torch.Tensor):
            prediction = [prediction]

        losses = {}
        for p, t, criterion in zip(prediction, target, self._criterion):
            p, t = p.to(self.device), t.to(self.device)

            losses[criterion.name] = criterion.exec(p, t)

        return losses

    def calculate_metrics(self, batch, prediction):
        _, target = self.split_batch(batch)

        metric_results = {}
        if self._has_nested_metrics:
            for p, t, metric_list in zip(prediction, target, self._metrics):
                p, t = p.to(self.device), t.to(self.device)

                for metric in metric_list:
                    metric_results[metric.name] = metric.exec(p, t)
        else:
            assert len(target) == 1
            target = target[0]

            prediction, target = prediction.to(self.device), target.to(self.device)

            for metric in self._metrics:
                metric_results[metric.name] = metric.exec(prediction, target)

        return metric_results


@singledispatch
def estimate_producer_epoch_sample_size(producer):
    return producer.batch_size * len(producer)


@estimate_producer_epoch_sample_size.register(DataLoader)
def _estimate_dataloader_epoch_sample_size(producer):
    return len(producer.dataset)


def _process_metrics_arg(metrics, criterion):
    metrics = list(metrics)
    is_metric = list(isinstance(obj, Metric) for obj in metrics)
    if not all(is_metric) and any(is_metric):
        raise ValueError(
            "metrics must be an iterable of Metrics, or an iterable of iterables of Metrics"
        )

    nested = not any(is_metric)
    if nested:
        metrics = [list(it) for it in metrics]
        metric_duplications = defaultdict(list)
        for metric_list in metrics:
            for metric in metric_list:
                metric_duplications[metric.name].append(metric)

        current_indices = {k: 0 for k, v in metric_duplications.items() if len(v) > 1}
        for i in range(len(metrics)):
            metric_list = metrics[i]
            for j in range(len(metric_list)):
                metric = metric_list[j]
                if metric.name in current_indices:
                    metric_list[j] = attr.evolve(
                        metric,
                        name="{}_{}".format(metric.name, current_indices[metric.name]),
                    )
                    current_indices[metric.name] += 1
    elif len(criterion) > 1:
        current_indices = {metric.name: 0 for metric in metrics}
        metrics = [metrics] * len(criterion)

        for metric_list in metrics:
            for i in range(len(metric_list)):
                metric = metric_list[i]
                metric_list[i] = attr.evolve(
                    metric,
                    name="{}_{}".format(metric.name, current_indices[metric.name]),
                )
                current_indices[metric.name] += 1
        nested = True

    return metrics, nested


def _update_means(current, previous, n):
    new_means = {}
    for k, v in current.items():
        new_means[k] = previous.get(k, 0) + (v - previous.get(k, 0)) / n
    return new_means


__all__ = [
    "AbstractModelHarnessMixin",
    "AbstractSupervisedLearningHarnessMixin",
    "Callback",
    "Criterion",
    "Metric",
    "SupervisedLearningHarness",
    "estimate_producer_epoch_sample_size",
]
