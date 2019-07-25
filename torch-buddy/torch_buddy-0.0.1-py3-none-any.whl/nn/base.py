# Standard libraries
import os
import time
import warnings
import datetime
from abc import ABC, abstractmethod

# Third party libraries
import glob
import torch
import numpy as np
import matplotlib.pyplot as plt
import torchvision.transforms.functional as FT
from torch import nn
from torch import optim
from torch.utils.data import DataLoader
from sklearn.externals import joblib

# User define libraries
from ..utils.helper import ProgressBar
from .lr_scheduler import ConstantLR
from .lr_scheduler import LinearLR4Finder
from .lr_scheduler import ExponentialLR4Finder
from .nn_helper import AverageMeter, clip_gradient
from ..utils.helper import mkdir
from .nn_helper import get_device, VisdomLinePlotter

warnings.filterwarnings(action="ignore")
DEVICE = get_device()


# ==============================================================================
# Base Class
# ==============================================================================
class PTBaseModel(ABC):
    """Interface containing some boilerplate code for training pytorch models.

    Parameters
    ----------
    data_loader : PTBaseDataLoader
        Class with function train_data_loader, valid_data_loader and attributes train_compose,
        valid_compose that yield tuple mapping data (pytorch tensor), label(pytorch tensor)
    scheduler : _LRScheduler, optional
        Child class of Pytorch learning rate scheduler., by default None
    scheduler_params : dict, optional
        Parameters of learning rate scheduler, by default {}
    plotter : VisdomLinePlotter, optional
        Class for tracking data history, by default None
    batch_size : int, optional
        Train and valid batch size, by default 16
    num_training_epochs : int, optional
        Number of training epoachs, by default 100
    lr : double, optional
        Learning rate of optimizer, by default 5e-4
    optimizer_name : str, optional
        Optimizer name used for training model, by default "adam"
    grad_clip : int, optional
        Clip bound of weights, by default 5
    early_stopping_steps : int, optional
        Number of epoch to do early stop, by default 5
    warm_start_init_epoch : int, optional
        Warm Started epoch, by default 0
    log_interval : int, optional
        Logging interval by epoch, by default 1
    log_dir : str, optional
        Log directory, by default "logs"
    checkpoint_dir : str, optional
        Check point directory, will be created if not exist, by default "checkpoints"
    multi_gpus : bool, optional
        true: Use multi gpus, false: Do not use multi gpus, by default false
    num_restarts : int, optional
         Number of times to do restart after early stop, by default None
    is_larger_better : bool, optional
        True: Evaluation metric larger better, False: Evaluation metric smaller better, by default True
    verbose : int, optional
        Print log information level, can be 1, 2, 3, 4, by default 1


    Raises
    ------
    ValueError, NotImplementedError
    """

    def __init__(
        self,
        data_loader,
        scheduler=None,
        scheduler_params: dict = {},
        use_plotter=None,
        batch_size=16,
        num_training_epochs=100,
        lr=5e-4,
        optimizer_name="adam",
        grad_clip=5,
        early_stopping_steps=5,
        warm_start_init_epoch=0,
        log_interval=1,
        log_dir="logs",
        checkpoint_dir="checkpoints",
        multi_gpus=False,
        num_restarts=None,
        is_larger_better=True,
        verbose=0,
    ):
        self.data_loader = data_loader
        self.scheduler = scheduler
        self.scheduler_params = scheduler_params
        self.use_plotter = use_plotter
        self.batch_size = batch_size
        self.num_training_epochs = num_training_epochs
        self.lr = lr
        self.optimizer_name = optimizer_name
        self.grad_clip = grad_clip
        self.early_stopping_steps = early_stopping_steps
        self.warm_start_init_epoch = warm_start_init_epoch
        self.log_interval = log_interval
        self.log_dir = log_dir
        self.checkpoint_dir = checkpoint_dir
        self.multi_gpus = multi_gpus
        self.num_restarts = num_restarts
        self.is_larger_better = is_larger_better
        self.verbose = verbose

        self.logging = print
        self.best_validation_loss = np.inf
        self.best_evaluation_score = 0
        self.best_validation_epoch = 1
        self.model = self.define_model()
        self._progress_bar_train = None
        self._progress_bar_valid = None
        self.now = datetime.datetime.now()
        self.lr_history = {"lr": [], "loss": []}
        self._best_lr_loss = None
        self.optimizer = None
        self._auto_init()

        # If scheduler is None, use ConstantLR, else use user defined learning rate scheduler.
        if self.scheduler is None:
            self.scheduler = ConstantLR(self.optimizer)
        else:
            self.scheduler = self.scheduler(optimizer=self.optimizer, **self.scheduler_params)

    def _auto_init(self):
        # Move model to multi gpus if needed.
        if self.multi_gpus is True:
            self.model = nn.DataParallel(self.model).to(DEVICE)
            self.logging("Training use {} GPUs.".format(torch.cuda.device_count()))
        else:
            self.model = self.model.to(DEVICE)
            self.logging("Training use {} GPU.".format(torch.cuda.device_count()))

        # Define plotter
        if self.use_plotter is True:
            self.plotter = VisdomLinePlotter(env_name="main")
        else:
            self.plotter = None

        # TODO 把这个改的更加容易理解
        # Define loss function
        self.criterion = self.define_loss_function()

        # Define optimizer
        self.optimizer = self.get_optimizer()

        # Define trackers
        if self.is_larger_better is True:
            self.best_evaluation_score = -np.inf
        else:
            self.best_evaluation_score = np.inf

    def fit(self):
        """
        If you do not re-initialize your model, all state will be keeped,
        and this fit function will be run on the previous state.
        """

        # ==============================================================================================================
        # Step-1: load pretrained model from warm_start_init_epoch if specifed, else train from beginning.
        # ==============================================================================================================
        if self.warm_start_init_epoch:
            epoch = self.restore(self.warm_start_init_epoch)
            self.logging("warm start from epoch {}.".format(epoch))
        else:
            self.checkpoint_dir += (
                str(self.now.year)
                + "_"
                + str(self.now.month)
                + "_"
                + str(self.now.day)
                + "_"
                + str(self.now.hour)
                + "_"
                + str(self.now.minute)
                + "_"
                + self.model.__class__.__name__
                + "/"
            )
            epoch = 1

        # ==============================================================================================================
        # Step2: get train and valid data loader.
        # ==============================================================================================================
        train_data_loader = self.data_loader.train_data_loader(self.batch_size)
        valid_data_loader = self.data_loader.valid_data_loader(self.batch_size)

        # ==============================================================================================================
        # Start training and validation.
        # ==============================================================================================================
        restarts = 0
        epochs_since_improvement = 0
        while epoch <= self.num_training_epochs:
            # Step-1: initialize progress bar.
            self._progress_bar_train = ProgressBar(len(train_data_loader))
            self._progress_bar_valid = ProgressBar(len(valid_data_loader))

            # Step-2: Scheduler learning rate after each epoch.
            self.scheduler.step()

            # Step-3: Train model.
            self._train(train_data_loader, epoch)

            # Step-4: Validate model by every log_interval epoch.
            if epoch % self.log_interval == 0:
                validation_loss, val_evaluation_score, evaluate_score_name = self._valid(valid_data_loader, epoch, restarts)

            # Step-5: Update best validation loss.
            validation_gap_loss = self.best_validation_loss - validation_loss
            self.best_validation_loss = min(validation_loss, self.best_validation_loss)

            # Step-6: Update best validation evaluation score.
            if self.is_larger_better is True:
                validation_gap_metric = val_evaluation_score - self.best_evaluation_score
                self.best_evaluation_score = max(self.best_evaluation_score, val_evaluation_score)
            else:
                validation_gap_metric = self.best_evaluation_score - val_evaluation_score
                self.best_evaluation_score = min(self.best_evaluation_score, val_evaluation_score)

            # Step-7: Update epochs_since_improvement.
            # If [loss decrease] or [evaluation score improved] then save checkpoint and reset
            # "epochs_since_improvement" and "best_validation_epoch"
            if validation_gap_loss > 0 or validation_gap_metric > 0:
                self.save(self.checkpoint_dir, epoch)
                epochs_since_improvement = 0
                self.best_validation_epoch = epoch
                self.logging(
                    " * Save model at Epoch {}\t| Improved loss: {:.3f}\t\t| Improved {}: {:.3f}".format(
                        epoch, validation_gap_loss, evaluate_score_name, validation_gap_metric
                    )
                )
            # If [loss increase] and [evaluation score become worse] then increase early stop rounds.
            else:
                epochs_since_improvement += 1
                self.logging(f" * Have not improved for {epochs_since_improvement} rounds")

            # Step-8: early stop policy.
            if epochs_since_improvement >= self.early_stopping_steps:
                # If reach early stop round and restart times is zero then stop training.
                if self.num_restarts is None or restarts >= self.num_restarts:
                    self.logging(
                        "Best validation [loss: {:.3f}], [{}: {:.3f}] at training epoch [{}]".format(
                            self.best_validation_loss, evaluate_score_name, self.best_evaluation_score, self.best_validation_epoch
                        )
                    )
                    return
                # If reach early stop round and have restart times then load best weights and decrease learning rate
                # and continue training.
                if restarts < self.num_restarts:
                    self.restore(self.best_validation_epoch)
                    epochs_since_improvement = 0
                    self.logging(" * Restore from epoch {}".format(self.best_validation_epoch))
                    for param_group, lr in zip(self.optimizer.param_groups, self.scheduler.get_lr()):
                        param_group["lr"] = lr / 2
                    epoch = self.best_validation_epoch
                    restarts += 1

            # Update epoch round
            epoch += 1

        self.logging("num_training_steps reached - ending training")

    def _train(self, data_loader, epoch):
        """Train one epoch.

        Parameters
        ----------
        data_loader: torch.utils.data.DataLoader
            Train data loader
        epoch: int
            Epoch number
        """
        self.model.train()  # training mode enables dropout

        # ==============================================================================================================
        # Define model performance tracker
        # ==============================================================================================================
        losses = AverageMeter()  # loss tracker
        data_time = AverageMeter()  # data loading time tracker
        batch_time = AverageMeter()  # forward prop + back prop time tracker

        # ==============================================================================================================
        # Train one epoch
        # ==============================================================================================================
        start = time.time()
        self.logging("\n")

        # Step1: train model
        for i, (inputs, labels) in enumerate(data_loader):
            # Step-1: display training progress.
            self._progress_bar_train.step(i + 1)

            # Step-2: calculate batch data load time.
            data_time.update(time.time() - start)

            # Step-3: train one batch
            # Compute loss -> clear gradient -> back propagation -> update weights
            loss, _ = self._train_one_batch(inputs, labels)

            # Step-4: clean up gradient
            # TODO 写专栏文章阐述为什么要zero_gradient, 从累加导致计算错误和对RNN的便利性
            self.optimizer.zero_grad()

            # Step-5: do back propagation
            loss.backward()

            # Step-6: clip gradients if necessary
            if self.grad_clip is not None:
                clip_gradient(self.optimizer, self.grad_clip)

            # Step-7: update weights and bias
            self.optimizer.step()

            # Step-7: update loss
            losses.update(loss.item(), data_loader.batch_size)

            # Step-8: update time
            batch_time.update(time.time() - start)
            start = time.time()

        # Step2: print training information
        self.logging("\n" + "=" * 80)
        self.logging(
            "Epoch: {}/{} | progress => {:.0%}".format(
                epoch, self.num_training_epochs, epoch / self.num_training_epochs
            )
        )
        self.logging("Batch: {}/{} | progress => {:.0%}".format(i, len(data_loader), i / len(data_loader)))
        self.logging(
            "Data Load Time : batch=>{:.2f}[s] | average => {:.2f}[s] | sum  ==> {:.2f}[s]".format(
                data_time.value, data_time.avg, data_time.sum
                )
            )
        self.logging(
            "Batch Run Time : batch=>{:.2f}[s] | average => {:.2f}[s] | sum  ==> {:.2f}[s]".format(
                batch_time.value, batch_time.avg, batch_time.sum
            )
        )
        self.logging("Training Loss  : batch=>{:.4f}\t| average  => {:.4f}".format(losses.value, losses.avg))
        self.logging("=" * 80)

        # ==============================================================================================================
        # Model performance tracking
        # ==============================================================================================================
        # Embed tracker data into plot
        if self.plotter is None:
            pass
        else:
            self.plotter.plot(
                "loss", "train", "Loss | Time [{}:{}]".format(self.now.hour, self.now.minute), epoch, losses.avg
            )

    def _train_one_batch(self, inputs, labels):
        """Train one batch, compute loss and predicted scores.

        Parameters
        ----------
        inputs: torch.tensor
            Predicted scores.
        labels: torch.tensor
            True labels.

        Return
        ------
        loss: float [need fix some bug, 考虑loss为数组的情况]
            Loss value.

        predicted_scores: tensor
            Model predicted score.
        """

        # TODO 对不同任务的兼容需要加强
        # ==============================================================================================================
        # Check different tasks
        # ==============================================================================================================
        # Task: Multi object detection [need fix some bug]
        # labels is list and label in labels is list.
        multi_outputs_single_input_flag = type(inputs) == torch.Tensor and type(labels) == list

        # Task: Tabular dataset, embedding categorical + continuous.
        # Inputs is a list that contain many tensors. [need fix some bug]
        multi_inputs_single_output_flag = type(inputs) == list and type(labels) == torch.Tensor

        # Task: Object classification
        # Inputs is a tensors. [need fix some bug]
        single_input_single_output_flag = type(inputs) == torch.Tensor and type(labels) == torch.Tensor
        # ==============================================================================================================
        # Predict scores
        # ==============================================================================================================
        if multi_outputs_single_input_flag:
            # Move labels to correct device
            labels_update = []
            for label in labels:
                labels_update.append([l.to(DEVICE) for l in label])
            labels = labels_update

            # Move predicted_scores to correct device
            predicted_scores = self.model(inputs.to(DEVICE))
            predicted_scores = [predicted_score.to(DEVICE) for predicted_score in predicted_scores]
        elif multi_inputs_single_output_flag:
            # Move inputs to correct device
            inputs_update = []
            for input in inputs:
                inputs_update.append(input.to(DEVICE))
            inputs = inputs_update

            # Move predicted_scores to correct device
            predicted_scores = self.model(inputs).to(DEVICE)

            # Move labels to correct device
            labels = labels.to(DEVICE)
        elif single_input_single_output_flag:
            # Move predicted_scores to correct device
            predicted_scores = self.model(inputs.to(DEVICE)).to(DEVICE)

            # Move labels to correct device
            labels = labels.to(DEVICE)
        else:
            assert False, "Unrecognized inputs and labels format!"

        if self.verbose:
            if multi_outputs_single_input_flag:
                self.logging("Multi outputs single input!")
                self.logging(
                    "Predicted_scores type\t: {}\nLabels type\t\t: {}".format(
                        [predicted_score.type() for predicted_score in predicted_scores],
                        [label.type() for label in labels],
                    )
                )
                self.logging(
                    "Predicted_scores shape\t: {}\nLabels shape\t\t: {}".format(
                        [predicted_score.shape for predicted_score in predicted_scores],
                        [label.shape for label in labels],
                    )
                )
            elif multi_inputs_single_output_flag:
                self.logging("Multi inputs single output!")
                self.logging(
                    "Predicted_scores type\t: {}\nLabels type\t\t: {}".format(predicted_scores.type(), labels.type())
                )
                self.logging(
                    "Predicted_scores shape\t: {}\nLabels shape\t\t: {}".format(predicted_scores.shape, labels.shape)
                )
            elif single_input_single_output_flag:
                self.logging("Single input single output!")
                self.logging(
                    "Predicted_scores type\t: {}\nLabels type\t\t: {}".format(predicted_scores.type(), labels.type())
                )
                self.logging(
                    "Predicted_scores shape\t: {}\nLabels shape\t\t: {}".format(predicted_scores.shape, labels.shape)
                )
            else:
                assert False, "Unrecognized inputs and labels format!"

        # ==============================================================================================================
        # Compute loss
        # ==============================================================================================================
        # Step-1: compute loss
        loss = self.criterion(predicted_scores, labels)

        return loss, predicted_scores

    def _valid(self, data_loader, epoch, restarts):
        """Train one batch.

        Parameters
        ----------
        data_loader : torch.utils.data.DataLoader
            Train data loader.
        epoch : int
            Epoch number, use for tracking performance.
        restarts : int
            Restart times.
        """
        self.model.eval()  # eval mode disables dropout

        # ==============================================================================================================
        # Define model performance tracker
        # ==============================================================================================================
        losses = AverageMeter()  # loss tracker
        validation_score = AverageMeter()  # TODO accuracy tracker, 需要改成更加通用的表示，有些评估指标并不是accuracy
        batch_time = AverageMeter()  # forward prop + back prop time tracker

        # ==============================================================================================================
        # Train one epoch
        # ==============================================================================================================
        start = time.time()
        with torch.no_grad():  # Prohibit gradient computation explicitly.
            for i, (inputs, labels) in enumerate(data_loader):
                # Step-1: Update progress bar.
                self._progress_bar_valid.step(i + 1)

                # Step-2: compute loss and predicted scores.
                loss, predicted_scores = self._train_one_batch(inputs, labels)

                # Step-3: compute evaluation metric
                evaluate_score_name, evaluate_score = self.evaluate(predicted_scores, labels)

                # Step-4: Track loss information
                losses.update(loss.item(), data_loader.batch_size)

                # Step-5: Track evaluation score information
                # If None do not track, else track it.
                if evaluate_score is None:
                    pass
                else:
                    validation_score.update(evaluate_score, data_loader.batch_size)

                batch_time.update(time.time() - start)
                start = time.time()

        # Print logging information
        self.logging(
                "\n * Validation Loss: {:.3f}\t| Validation {}: {:.2f}\t\t| Restart times: {}".format(
                    losses.avg, evaluate_score_name, validation_score.avg, restarts
                )
            )

        # Embed tracker data into plot
        if self.plotter is None:
            pass
        else:
            self.plotter.plot(
                "loss", "valid", "Loss | Time [{}:{}]".format(self.now.hour, self.now.minute), epoch, losses.avg
            )
            if evaluate_score is not None:
                self.plotter.plot(
                    evaluate_score_name,
                    "valid",
                    evaluate_score_name + " | Time [{}:{}]".format(self.now.hour, self.now.minute),
                    epoch,
                    validation_score.avg,
                )

        return losses.avg, validation_score.avg, evaluate_score_name

    def find_optimal_rate(
        self, loss_type="train", end_lr=10, num_iter=100, step_mode="exp", smooth_f=0.05, diverge_th=5
    ):
        """Performs the learning rate range test.

        Parameters
        ----------
        loss_type: str, optional "train" or "valid"
            Monitor on train or valid dataset.
        end_lr: float, optional
            The maximum learning rate to test. Default: 10.
        num_iter: int, optional
            The number of iterations over which the test
            occurs. Default: 100.
        step_mode: str, optional, One of the available learning rate policies,
            linear or exponential ("linear", "exp"). Default: "exp".
        smooth_f: float, optional, The loss smoothing factor within the [0, 1]
            Use smooth_f of this loss and (1-smooth_f) of last loss
        diverge_th: int, optional
            The test is stopped when the loss surpasses the threshold:  diverge_th * best_loss. Default: 5.
        """
        # Step-1: init states
        self._auto_init()
        self.lr_history = {"lr": [], "loss": []}
        self._best_lr_loss = None
        loss_type = loss_type.lower()
        assert loss_type in ("train", "valid"), "loss_type should be in train or valid"

        # Step-2: select learning rate scheduler
        if step_mode.lower() == "exp":
            lr_schedule = ExponentialLR4Finder(self.optimizer, end_lr, num_iter)
        elif step_mode.lower() == "linear":
            lr_schedule = LinearLR4Finder(self.optimizer, end_lr, num_iter)
        else:
            raise ValueError("expected one of (exp, linear), got {}".format(step_mode))

        assert 0 < smooth_f <= 1, "smooth_f is outside the range [0, 1]"

        # Step-3: train num_iter batches.
        iterator = iter(self.data_loader.train_data_loader(self.batch_size))
        if loss_type == "valid":
            valid_data_loader = self.data_loader.valid_data_loader(self.batch_size)
        lr_progressBar = ProgressBar(num_iter)

        try:
            for iteraion in range(num_iter):
                lr_progressBar.step(iteraion)

                # Step-1: load one batch.
                inputs, labels = next(iterator)

                # Step-2: train one batch.
                self.model.train()
                loss, _ = self._train_one_batch(inputs=inputs, labels=labels)

                # Step-4: clean up gradient
                self.optimizer.zero_grad()

                # Step-5: do back propagation
                loss.backward()
                lr_loss = loss.item()

                # Step-6: clip gradients if necessary
                if self.grad_clip is not None:
                    clip_gradient(self.optimizer, self.grad_clip)

                # Step-7: update weights and bias
                self.optimizer.step()

                if loss_type == "valid":
                    self._progress_bar_valid = ProgressBar(len(valid_data_loader))
                    lr_loss, _ = self._valid(valid_data_loader, epoch=0, restarts=0)

                # Step-8: update learning rate
                lr_schedule.step()
                self.lr_history["lr"].append(lr_schedule.get_lr()[0])

                # Step-8: smooth loss
                if iteraion == 0:
                    self._best_lr_loss = lr_loss
                else:
                    if smooth_f > 0:
                        lr_loss = smooth_f * lr_loss + (1 - smooth_f) * self.lr_history["loss"][-1]
                    if lr_loss < self._best_lr_loss:
                        self._best_lr_loss = lr_loss

                # Step-9: check if the loss has diverged; if it has, stop the test
                self.lr_history["loss"].append(lr_loss)
                if lr_loss > diverge_th * self._best_lr_loss:
                    print("Stopping early, the loss has diverged")
                    break
        finally:
            self._auto_init()

    def plot_lr_finder_curve(self, skip_start=5, skip_end=5, log_lr=True, suggestion=True):
        """Plot learning rate finder curve to find the best learning rate

        Parameters
        ----------
        skip_start: int, optional (Default: 10)
            Number of batches to trim from the start.
        skip_end: int, optional (Default: 5)
            Number of batches to trim from the start.
        log_lr: bool,
            Optional True to plot the learning rate in a logarithmic
            scale; otherwise, plotted in a linear scale. Default: True.

        """

        assert skip_start >= 0, "skip_start cannot be negative"
        assert skip_end >= 0, "skip_end cannot be negative"

        # Get the data to plot from the history dictionary. Also, handle skip_end=0
        # properly so the behaviour is the expected
        lrs = self.lr_history["lr"]
        losses = self.lr_history["loss"]
        if skip_end == 0:
            lrs = lrs[skip_start:]
            losses = losses[skip_start:]
        else:
            lrs = lrs[skip_start:-skip_end]
            losses = losses[skip_start:-skip_end]

        # Plot loss as a function of the learning rate
        plt.plot(lrs, losses)
        if suggestion:
            try:
                mg = (np.gradient(np.array(losses))).argmin()
            except Exception:
                print("Failed to compute the gradients, there might not be enough points.")
                return

            print("Min numerical gradient: {:.2E}".format(lrs[mg]))
            plt.plot(lrs[mg], losses[mg], markersize=10, marker="o", color="red")
            self.min_grad_lr = lrs[mg]

        if log_lr:
            plt.xscale("log")
        plt.xlabel("Learning rate")
        plt.ylabel("Loss")
        plt.show()

    def predict(self, image):
        """
        Args:
            image: PIL format
        """
        with torch.no_grad():
            try:
                image = self.data_loader.valid_compose(image)
            except AttributeError:
                image = FT.to_tensor(image)
            image = image.unsqueeze(0)
            image = image.to("cpu")
            # s = time.time()
            predicted_score = self.model(image)
            # e = time.time()
            # print(e - s)
        return predicted_score

    def __predict_folder(self, batch_size=16):
        test_data_loader = self.data_loader.test_data_loader(batch_size)

        predicted_scores_list = []
        with torch.no_grad():
            # Batches
            for i, image in enumerate(test_data_loader):
                # Move to default device
                image = image.to("cpu")
                # Forward prop.
                predicted_scores = self.model(image).double()
                predicted_scores_list.append(predicted_scores)

        res = torch.cat(predicted_scores_list, dim=0)

        joblib.dump(res, self.prediction_dir + "")
        return res

    def save(self, checkpoint_dir, epoch):
        mkdir(checkpoint_dir)
        state = {"epoch": epoch, "model": checkpoint_dir + "model_" + "epoch" + str(epoch) + ".pth"}
        if self.multi_gpus:
            torch.save(self.model.module.state_dict(), checkpoint_dir + "model_" + "epoch" + str(epoch) + ".pth")
        else:
            torch.save(self.model.state_dict(), checkpoint_dir + "model_" + "epoch" + str(epoch) + ".pth")
        torch.save(state, checkpoint_dir + "model_" + "epoch" + str(epoch) + ".pth.tar")
        self._save_latest_checkpoint(checkpoint_dir)

    def _save_latest_checkpoint(self, checkpoint_dir, max_to_keep=4, verbose=0):
        # Save latest n files in checkpoint dir.
        saved_model_files = glob.glob(checkpoint_dir + "*.pth") + glob.glob(checkpoint_dir + "*.pth.tar")
        saved_model_files_lasted_n = sorted(saved_model_files, key=os.path.getctime)[-max_to_keep:]
        files_tobe_deleted = set(saved_model_files).difference(saved_model_files_lasted_n)

        for file in files_tobe_deleted:
            os.remove(file)
            if verbose:
                self.logging("Only keep {} model files, remove {}".format(max_to_keep, checkpoint_dir + file))

    def restore(self, epoch=None):
        # If epoch is None, restore weights from the best epoch.
        # Else restore weights from a specified epoch.
        if epoch is None:
            newest_model_files = sorted(glob.glob(self.checkpoint_dir + "*.pth"), key=os.path.getctime)[-1]
            self.model.load_state_dict(torch.load(newest_model_files, map_location=DEVICE.type))
        else:
            checkpoint = torch.load(self.checkpoint_dir + "model_" + "epoch" + str(epoch) + ".pth.tar")
            epoch = checkpoint["epoch"]
            self.model.load_state_dict(torch.load(checkpoint["model"], map_location=DEVICE.type))
        return epoch

    @abstractmethod
    def evaluate(self, preds, labels):
        """ Implement evaluation function here

        Parameters
        ----------
        preds : Pytorch tensor or [Pytorch tensor, ...]
                Predict scores, shape is [batch_size, num_pictures, num_classes]

        labels : Pytorch tensor or [Pytorch tensor, ...]
                True labels, shape is [batch_size, num_pictures, 1]


        Returns
        -------
        anonymous : tensor
        """
        raise NotImplementedError

    @abstractmethod
    def define_loss_function(self):
        """ Implement loss function here

        Returns
        -------
        Pytorch Module Object, must implement __init__() and forward() method.
        """
        raise NotImplementedError

    @abstractmethod
    def define_model(self):
        """ Implement model structure here

        Returns
        -------
        Pytorch Module Object, must implement __init__() and forward() method.
        """
        raise NotImplementedError

    def get_optimizer(self):
        if self.optimizer_name == "adam":
            return optim.Adam(self.model.parameters(), lr=self.lr)
        elif self.optimizer_name == "sgd":
            return optim.SGD(self.model.parameters(), lr=self.lr)
        else:
            return None


class PTBaseDataLoader:
    def __init__(self, dataset, folder, train_compose, valid_compose, **kwargs):
        """ Dataloader for loading dataset

        Parameters
        ----------
        PTBaseDataset: Pytorch Dataset
            Dataset class contains data transformation and loading function.
        folder: str
            Folder contain train and valid dataset.
        train_compose:
            Augmentation operations for train dataset.
        valid_compose:
            Augmentation operations for test dataset.
        kwargs:


        Examples
        --------
        Your code here.
        """

        self.folder = folder
        self.dataset = dataset
        self.train_compose = train_compose
        self.valid_compose = valid_compose
        self.kwargs = kwargs

    def train_data_loader(self, batch_size):
        # return train data loader
        train_dataset = self.dataset(self.folder, "train", self.train_compose, **self.kwargs)
        return DataLoader(train_dataset, batch_size=batch_size, shuffle=True, collate_fn=train_dataset.collate_fn)

    def valid_data_loader(self, batch_size):
        # return valid data loader
        valid_dataset = self.dataset(self.folder, "valid", self.valid_compose, **self.kwargs)
        return DataLoader(valid_dataset, batch_size=batch_size, shuffle=False, collate_fn=valid_dataset.collate_fn)
