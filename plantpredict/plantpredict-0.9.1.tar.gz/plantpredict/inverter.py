import requests

from plantpredict.plant_predict_entity import PlantPredictEntity
from plantpredict.error_handlers import handle_refused_connection, handle_error_response
from plantpredict.enumerations import EntityTypeEnum


class Inverter(PlantPredictEntity):
    """
    """
    def create(self):
        """POST /Inverter"""
        self.create_url_suffix = "/Inverter"
        return super(Inverter, self).create()

    def delete(self):
        """DELETE /Inverter/{Id}"""
        self.delete_url_suffix = "/Inverter/{}".format(self.id)
        return super(Inverter, self).delete()

    def get(self):
        """GET /Inverter/{Id}"""
        self.get_url_suffix = "/Inverter/{}".format(self.id)
        return super(Inverter, self).get()

    def update(self):
        """PUT /Inverter"""
        self.update_url_suffix = "/Inverter".format(self.id)
        return super(Inverter, self).update()

    @handle_refused_connection
    @handle_error_response
    def change_inverter_status(self, new_status, note=""):
        """

        :param new_status:
        :param note:
        :return:
        """
        return requests.post(
            url=self.api.base_url + "/Inverter/Status",
            headers={"Authorization": "Bearer " + self.api.access_token},
            json=[{
                "name": self.name,
                "id": self.id,
                "type": EntityTypeEnum.INVERTER,
                "status": new_status,
                "note": note
            }]
        )
