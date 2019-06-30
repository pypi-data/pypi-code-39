"""
Identity protocol backbone, and a generic user lookup command.

Config:
    identities (int):
        List of identity provider names from which to allow lookups.
    public (bool):
        ``True`` to allow anyone with access to the ``who`` command to do a lookup, without
        necessarily being identified themselves.

Commands:
    who <name>:
        Recall a known identity and all of its links.

This module defines a subclass for all hooks providing identity services -- no hook is needed from
here if using an identity hook elsewhere.  The :class:`.WhoIsHook` provides a command for users to
query basic identity information.
"""

from asyncio import gather
import logging

from voluptuous import ALLOW_EXTRA, Optional, Schema

import immp
from immp.hook.command import command


CROSS = "\N{CROSS MARK}"
TICK = "\N{WHITE HEAVY CHECK MARK}"


log = logging.getLogger(__name__)


class _Schema:

    config = Schema({"identities": [str],
                     Optional("public", default=False): bool},
                    extra=ALLOW_EXTRA, required=True)


@immp.pretty_str
class Identity:
    """
    Basic representation of an external identity.

    Attributes:
        name (str):
            Common name used across any linked platforms.
        provider (.IdentityProvider):
            Service hook where the identity information was acquired from.
        links (User list):
            Physical platform users assigned to this identity.
        roles (str list):
            Optional set of role names, if applicable to the backend.
    """

    @classmethod
    async def gather(cls, *tasks):
        """
        Helper for fetching users from plugs, filtering out calls with no matches::

            >>> await Identity.gather(plug1.user_from_id(id1), plug2.user_from_id(id2))
            [<Plug1User: '123' 'User'>]

        Args:
            tasks (coroutine list):
                Non-awaited coroutines or tasks.

        Returns:
            list:
                Gathered results of those tasks.
        """
        tasks = list(filter(None, tasks))
        if not tasks:
            return []
        users = []
        for result in await gather(*tasks, return_exceptions=True):
            if isinstance(result, BaseException):
                log.warning("Failed to retrieve user for identity", exc_info=result)
            else:
                users.append(result)
        return users

    def __init__(self, name, provider=None, links=(), roles=()):
        self.name = name
        self.provider = provider
        self.links = links
        self.roles = roles

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                (self.name, self.provider) == (other.name, other.provider))

    def __hash__(self):
        return hash(self.name, self.provider)

    def __repr__(self):
        return "<{}: {} x{}{}>".format(self.__class__.__name__, repr(self.name), len(self.links),
                                       " ({})".format(" ".join(self.roles)) if self.roles else "")


class IdentityProvider:
    """
    Interface for hooks to provide identity information from a backing source.
    """

    async def identity_from_name(self, name):
        """
        Look up an identity by the external provider's username for them.

        Args:
            name (str):
                External name to query.

        Returns:
            .Identity:
                Matching identity from the provider, or ``None`` if not found.
        """
        raise NotImplementedError

    async def identity_from_user(self, user):
        """
        Look up an identity by a linked network user.

        Args:
            user (.User):
                Plug user referenced by the identity.

        Returns:
            .Identity:
                Matching identity from the provider, or ``None`` if not found.
        """
        raise NotImplementedError


class WhoIsHook(immp.Hook):
    """
    Hook to provide generic lookup of user profiles across one or more identity providers.
    """

    _identities = immp.ConfigProperty([IdentityProvider])

    def __init__(self, name, config, host):
        super().__init__(name, _Schema.config(config), host)

    @command("who")
    async def who(self, msg, name):
        """
        Recall a known identity and all of its links.
        """
        if self.config["public"]:
            providers = self._identities
        else:
            tasks = (provider.identity_from_user(msg.user) for provider in self._identities)
            providers = [identity.provider for identity in await gather(*tasks) if identity]
        if providers:
            identities = list(filter(None, await gather(*(provider.identity_from_name(name)
                                                          for provider in providers))))
            links = {link for identity in identities for link in identity.links}
            if links:
                text = immp.RichText([immp.Segment(name, bold=True),
                                      immp.Segment(" may appear as:")])
                for user in sorted(links, key=lambda user: user.plug.network_name):
                    text.append(immp.Segment("\n"))
                    text.append(immp.Segment("({}) ".format(user.plug.network_name)))
                    if user.link:
                        text.append(immp.Segment(user.real_name or user.username, link=user.link))
                    elif user.real_name and user.username:
                        text.append(immp.Segment("{} [{}]".format(user.real_name, user.username)))
                    else:
                        text.append(immp.Segment(user.real_name or user.username))
            else:
                text = "{} Name not in use".format(CROSS)
        else:
            text = "{} Not identified".format(CROSS)
        await msg.channel.send(immp.Message(text=text))
