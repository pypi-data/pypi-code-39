from collections import defaultdict

import numpy as np
from scipy.sparse import coo_matrix
import torch
from torch import nn

from . import harness
from ._utils import get_tqdm_aliases


class Accuracy(nn.Module):
    def forward(self, prediction, target):
        pred = prediction.max(1, keepdim=True)[1]
        return 100 * pred.eq(target.view_as(pred)).type(torch.float32).mean()


def confusion_matrix(h, producer, classes=None, verbose=True, notebook_mode=False):
    y_true = defaultdict(list)
    y_pred = defaultdict(list)
    metric_averages = {}

    raw_history = []
    average_history = []

    tqdm, _ = get_tqdm_aliases(notebook_mode)
    with tqdm(
        total=harness.estimate_producer_epoch_sample_size(producer),
        desc="Evaluating",
        unit="samples",
    ) as t:
        for i, batch in enumerate(producer, 0):
            _, target = h.split_batch(batch)
            pred, batch_size = h.predict_batch(batch)

            if isinstance(pred, torch.Tensor):
                pred_list = [pred]
            else:
                pred_list = pred

            for j, (p, tt) in enumerate(zip(pred_list, target)):
                y_pred[j].extend(p.argmax(1).squeeze(-1).cpu().numpy())
                y_true[j].extend(tt.squeeze(-1).cpu().numpy())

            loss_metrics = h.calculate_loss(batch, pred)
            metrics = h.calculate_metrics(batch, pred)
            loss_metrics.update(metrics)
            loss_metrics = {k: v.item() for k, v in loss_metrics.items()}

            metric_averages = harness._update_means(
                loss_metrics, metric_averages, i + 1
            )

            raw_history.append(loss_metrics)
            average_history.append(metric_averages)

            t.set_postfix(**metric_averages)
            t.update(batch_size)

    cms = []
    if len(y_true) == 1:
        t = np.asarray(y_true[0])
        p = np.asarray(y_pred[0])

        if classes is None:
            classes = np.unique(t).tolist()
        num_classes = len(classes)

        cm = coo_matrix(
            (np.ones(len(t)), (t, p)), shape=(num_classes, num_classes), dtype=t.dtype
        ).toarray()
        cms.append(cm)
    else:
        if classes is None:
            classes = [None] * len(y_true)
        for k in y_true:
            t = np.asarray(y_true[k])
            p = np.asarray(y_pred[k])
            c = classes[k]

            if c is None:
                c = np.unique(t).tolist()
            num_classes = len(c)

            cm = coo_matrix(
                (np.ones(len(t)), (t, p)),
                shape=(num_classes, num_classes),
                dtype=t.dtype,
            ).toarray()
            cms.append(cm)

    return cms, (raw_history, average_history)


__all__ = ["Accuracy", "confusion_matrix"]
