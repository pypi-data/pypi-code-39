from typing import Optional

from service.authentication.base import AuthenticationBase
from service.authentication.file import AuthenticationFile


class AuthenticationFactory:

    def __new__(self, style: str) -> Optional[type]:
        if style.lower() == 'file':
            return AuthenticationFile
        return None
