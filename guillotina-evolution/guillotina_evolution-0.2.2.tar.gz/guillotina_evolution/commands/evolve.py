from guillotina.commands import Command
from guillotina.component import get_utility
from guillotina.interfaces import IAnnotations
from guillotina.registry import REGISTRY_DATA_KEY
from guillotina.utils import get_containers
from guillotina_evolution.utility import IEvolutionUtility

import aiotask_context


class EvolveCommand(Command):
    description = "Run evolution"

    async def run(self, arguments, settings, app):
        request = self.request
        aiotask_context.set("request", request)

        utility = get_utility(IEvolutionUtility)

        async for _, _, container in get_containers(request):
            annotations_container = IAnnotations(container)
            registry = await annotations_container.async_get(REGISTRY_DATA_KEY)
            request.container_settings = registry
            await utility.evolve(container)
