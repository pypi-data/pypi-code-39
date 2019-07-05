"""
fritz.keras.model_checkpoint
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This module contains a Keras callback to upload new versions of a
model to Fritz.
"""
import logging

import keras

import fritz

_logger = logging.getLogger(__name__)


# pylint: disable=too-many-instance-attributes
class FritzSnapshotCallback(keras.callbacks.Callback):
    """Keras callback to create a ModelSnapshot in Fritz.

    Adding this callback will convert and upload mobile-ready models
    during training.
    """

    def __init__(
        self,
        api_key=None,
        project_id=None,
        model_ids_by_framework=None,
        converters_by_framework=None,
        output_file_name=None,
        period=10,
        deploy=False,
        metadata=None,
    ):
        # pylint: disable=line-too-long
        """Save a Fritz Snapshot to Fritz.

        Args:
            api_key (Optional[str]): Optional API Key.
            project_id (Optional[str]): Optional project id, required if not
                globally set.
            model_ids_by_framework (Dict[frameworks.ModelFramework,str]):
                Dictionary mapping model framework to model ids. If model_id
                not set for a given platform, a new model will be created.
            converters_by_framework (Dict[frameworks.ModelFramework,Callable[[keras.models.Model], Any]]):
                Dictionary mapping model framework to conversion function.
            output_file_name (str): Name of output_file.
            period (int): Interval (number of epochs) between checkpoints.
            deploy (bool): If True will set active version of model to latest
                uploaded model. Default False.
            metadata (dict): Optional dictionary of metadata to include about
                job arguments.

        """
        super().__init__()
        self._api_key = api_key
        self._project_id = project_id
        self._output_file_name = output_file_name
        self._period = period
        self._deploy = deploy
        self._model_ids = model_ids_by_framework or {}
        self._converters = converters_by_framework or {}
        self._job_metadata = metadata or {}

    def add_model_metadata(
        self, logs
    ):  # noqa pylint: disable=unused-argument,no-self-use
        """Adds additional metadata about the model to be stored in Fritz.

        Optionally override this method returning custom information.

        Args:
            logs (dict): Includes values such as `acc` and `loss`.

        Returns: Dict of model metadata.
        """
        return {}

    def on_epoch_end(self, epoch, logs=None):
        """Saves model to Fritz on epoch end.

        Args:
            epoch (int): the epoch number
            logs (dict, optional): logs dict
        """
        _logger.info(
            "{num_epochs} - {epoch}".format(
                num_epochs=self.params.get("epochs"), epoch=epoch
            )
        )
        is_last_epoch = self.params.get("epochs") == (epoch + 1)
        # Adding one so that the very first run does not trigger an upload.
        # If you specify period to be 3, the first upload will be on the 3rd
        # epoch.
        if not is_last_epoch and (epoch + 1) % self._period != 0:
            return

        _logger.info("Creating ModelSnapshot - epoch %s", epoch)
        metadata = {"epoch": epoch, "keras_model_path": self._output_file_name}
        metadata.update(logs or {})
        metadata["job_arguments"] = self._job_metadata
        metadata.update(self.add_model_metadata(logs))
        _, _, models = fritz.ModelSnapshot.create(
            api_key=self._api_key,
            project_id=self._project_id,
            filename=self._output_file_name,
            keras_model=self.model,
            set_active=self._deploy,
            metadata=metadata,
            converters=self._converters,
            model_ids=self._model_ids,
        )

        # Update previously unset model_ids with created models.
        for model in models:
            if not self._model_ids.get(model.framework):
                self._model_ids[model.framework] = model.id
