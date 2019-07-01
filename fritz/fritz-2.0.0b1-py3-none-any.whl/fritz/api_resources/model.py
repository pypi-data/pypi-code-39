"""
fritz.api_resources.model
~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: © 2019 by Fritz Labs Incorporated
:license: MIT, see LICENSE for more details.
"""

import fritz
from fritz.api_resources import fritz_object


class Model(fritz_object.FritzObject):
    """Fritz Model object."""

    OBJECT_NAME = "Model"

    def summary(self):
        """Print summary of object."""
        details = [
            ("Created At", self.created_date),
            ("Description", self.description),
            ("Model Format", self.model_format),
            ("Project ID", self.project_uid),
            ("Active Version", self.active_version),
            ("Is Global", self.is_global),
        ]
        return self._summary(self.name, details)

    @property
    def framework(self):
        """Gets associated framework for model.

        Returns: frameworks.ModelFramework
        """
        if self.model_format == "coreml":
            return fritz.frameworks.CORE_ML
        if self.model_format == "tflite":
            return fritz.frameworks.TENSORFLOW_LITE
        if self.model_format == "tfmobile":
            return fritz.frameworks.TENSORFLOW_MOBILE
        if self.model_format == "keras":
            return fritz.frameworks.KERAS

        return None

    @classmethod
    def get(cls, api_key=None, model_id=None):
        """Get model.

        Args:
            model_id: ID of model to query.
            api_key: Optional API Key to use.

        Returns: Model
        """
        if not model_id:
            raise fritz.errors.ArgumentRequiredError("model_id")

        url = "/model/" + model_id
        response = cls.client_get(url, api_key=api_key)
        return fritz.utils.convert_to_fritz_object(response)

    @classmethod
    def list(cls, api_key=None, project_id=None, all_projects=False):
        """Get model, restricting results to specified arguments.

        Args:
            api_key: Optional API Key to use.
            project_id: Project ID
            all_projects: If True and no project_id specified, returns models
                from all projects. Default False.

        Returns: List[Model]
        """
        url = "/model"
        if not project_id and not all_projects:
            project_id = fritz.project_id

        params = {"project_uid": project_id}
        response = cls.client_get(url, api_key=api_key, params=params)

        return [
            fritz.utils.convert_to_fritz_object(model)
            for model in response["models"]
        ]

    def get_version(self, version_number=None):
        """Get specific version matching version number.

        Args:
            version_number (int): Version to fetch. If not provided uses
                active_version.

        returns: Optional[fritz.ModelVersion]
        """
        version_number = version_number or self.active_version
        versions = [
            version
            for version in fritz.ModelVersion.list(self.id)
            if version.version_number == version_number
        ]

        if versions:
            return versions[0]

        return None

    def download(self, api_key=None, version_number=None, output_dir=None):
        """Download model file of either active version or specified version.

        Args:
            api_key (str): Optional API Key to use.
            version_number (int): Optional version number. If not specified
                downloads active version.
            output_dir (str): Output directory.

        Returns: Tuple of (ModelVersion, path) of downloaded file.
        """

        version_number = version_number or self.active_version

        versions = fritz.ModelVersion.list(self.id, api_key=api_key)
        version = next(
            (
                version
                for version in versions
                if version.version_number == version_number
            ),
            None,
        )
        if not version:
            return (None, None)

        path = version.download(download_dir=output_dir)
        return (version, path)

    def update(self, api_key=None, **updates):
        """Update model with specified updates.

        Args:
            api_key: Optional API Key to use.
            kwargs: Dictionary of updates.

        Returns: New model with updates.
        """
        url = "/model/" + self.id
        result = self.client_put(url, params=updates)
        return fritz.utils.convert_to_fritz_object(result)
