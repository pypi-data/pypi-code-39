from guillotina import testing
from guillotina.content import create_content_in_container
from guillotina.interfaces import IAnnotations
from guillotina.registry import Registry
from guillotina.registry import REGISTRY_DATA_KEY
from guillotina.tests import utils
from guillotina.tests.fixtures import ContainerRequesterAsyncContextManager
from guillotina.transactions import managed_transaction

import json
import pytest


def base_settings_configurator(settings):
    if "applications" in settings:
        settings["applications"].append("guillotina_evolution")
    else:
        settings["applications"] = ["guillotina_evolution"]


testing.configure_with(base_settings_configurator)


class guillotina_evolution_Requester(ContainerRequesterAsyncContextManager):  # noqa
    async def __aenter__(self):
        await super().__aenter__()
        await self.requester(
            "POST",
            "/db/guillotina/@addons",
            data=json.dumps({"id": "guillotina_evolution"}),
        )
        return self.requester


@pytest.fixture(scope="function")
async def guillotina_evolution_requester(guillotina):
    return guillotina_evolution_Requester(guillotina)


@pytest.fixture(scope="function")
async def environment(guillotina):
    root = guillotina.root
    db = root["db"]

    request = utils.get_mocked_request(db)
    utils.login(request)

    async with managed_transaction(request=request):
        container = await create_content_in_container(
            db, "Container", "container", request=request, title="Container"
        )

        request.container = container

        annotations_container = IAnnotations(container)
        await annotations_container.async_set(REGISTRY_DATA_KEY, Registry())
        request.container_settings = await annotations_container.async_get(
            REGISTRY_DATA_KEY
        )

    yield request, container
