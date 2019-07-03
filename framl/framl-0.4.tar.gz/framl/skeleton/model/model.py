class Model:

    def __init__(self):
        """
        this method is called once at the startup
        please make sure you put all the initialization here
        """

        # declare your model input data
        self.input_validation = {
            "field_name" : str,
            "field_name_two" : float,
        }

        pass

    def predict(self, single_data: dict) -> dict:
        """
        This function is called for each row in the request payload.
        Add your prediction logic here.
        Make sure you return your result as a dictionary
        :param single_data: dict
        :return result: dict
        """
        return single_data
