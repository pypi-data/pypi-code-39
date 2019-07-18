from guillotina import configure
from guillotina.interfaces import IContainer
from guillotina.transactions import managed_transaction
from guillotina.utils import get_current_request
from guillotina_evolution.interfaces import IEvolutionUtility
from typing import Awaitable

import logging

logger = logging.getLogger("guillotina_evolution")


GENERATION_KEY = "guillotina_evolution.utility.generation"


@configure.utility(provides=IEvolutionUtility)
class EvolutionUtility(object):
    def __init__(self, settings=None, loop=None):
        self._settings = settings or {}
        self._loop = loop
        self._evolvers = {}

    def register(self, gen: int, evolver: Awaitable):
        if gen in self._evolvers:
            raise Exception(f"Evolver for generation '{gen}' already exist")

        self._evolvers[gen] = evolver

    async def evolve(self, container: IContainer):
        cur_gen = self._get_curr_gen()
        evolvers = self._get_evolvers(cur_gen)

        if len(evolvers) > 0:
            logger.info(f"Start evolving container {container}")
            for gen, evolver in evolvers:
                async with managed_transaction(adopt_parent_txn=True):
                    logger.info(f"Evolving from generation '{cur_gen}' to '{gen}'")
                    await evolver(container)
                    self._update_curr_gen(gen)
                    cur_gen = self._get_curr_gen()

            logger.info(f"Container {container} is now at generation {gen}")
        else:
            logger.info(f"Container already at latest generation")

    def _get_evolvers(self, from_):
        evolvers = []
        for gen in sorted(self._evolvers.keys()):
            if gen > from_:
                evolvers += [(gen, self._evolvers[gen])]
        return evolvers

    def _get_curr_gen(self):
        registry = self._get_registry()
        return registry[GENERATION_KEY]

    def _update_curr_gen(self, gen):
        registry = self._get_registry()
        registry[GENERATION_KEY] = gen
        registry._p_register()

    def _get_registry(self):
        request = get_current_request()
        registry = request.container_settings
        if GENERATION_KEY not in registry:  # first time we run guillotina_evolution
            registry[GENERATION_KEY] = self._get_greatest_registered_gen()
            registry._p_register()
        return registry

    def _get_greatest_registered_gen(self):
        gens = sorted(self._evolvers.keys())
        if len(gens) > 0:
            return gens[-1]
        else:
            return 0
