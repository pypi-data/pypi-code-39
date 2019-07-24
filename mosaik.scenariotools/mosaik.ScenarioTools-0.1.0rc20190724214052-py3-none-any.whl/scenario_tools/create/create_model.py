import mosaik


def create_model(
    *,
    model: type,
    # model_dto: object = None,
    simulator: type,
    world: mosaik.scenario.World,
):
    """
    Create a model of a given type on a simulator of a given type.
    :param world: The world in which to create the model and simulator.
    :param simulator: The type of simulator to create in the world.
    :param model: The type of model to create in the simulator.

    :return: The model instance.
    """
    #     :param model_dto: The data transfer object for the model.
    simulator_instance = world.start(simulator.__name__)
    model_mock = \
        getattr(simulator_instance, model.__name__)

    # help(model_mock)
    # if model_dto is not None:
    #    model_instance = model_mock(model_dto)
    # else:
    model_instance = model_mock()

    return model_instance
