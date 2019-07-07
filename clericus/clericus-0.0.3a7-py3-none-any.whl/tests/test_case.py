import sys
sys.path.append(".")

from .. import Clericus
from ..config import defaultSettings, connectToDB

import unittest
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

import json
import faker
fake = faker.Faker()

from ..schemas import createCollections


class ClericusTestCase(AioHTTPTestCase):
    async def tearDownAsync(self):
        await self.db.client.drop_database(self.db.name)

    async def get_application(self) -> Clericus:
        settings = defaultSettings()
        settings["db"]["name"] = f"test{type(self).__name__}"
        settings = connectToDB(settings)
        await settings["db"].client.drop_database(settings["db"].name)
        self._settings = settings
        self.db = settings["db"]
        await createCollections(self.db)
        return Clericus(self._settings, logging=False)

    async def login(self, user=None):
        if not user:
            user = {
                "username": fake.user_name(),
                "email": fake.email(),
                "password": fake.password(),
            }
            resp = await self.client.request(
                "POST",
                "/sign-up/",
                json=user,
            )
        else:
            resp = await self.client.request(
                "POST",
                "/log-in/",
                json=user,
            )
        return user

    async def logout(self):
        resp = await self.client.request(
            "GET",
            "/log-out/",
        )
        return None