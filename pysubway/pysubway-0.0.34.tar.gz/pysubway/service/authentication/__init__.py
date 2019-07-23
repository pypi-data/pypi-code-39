from typing import Optional

try:
    from service.authentication.base import AuthenticationBase
    from service.authentication.file import AuthenticationFile
except (ModuleNotFoundError, ImportError) as e:
    from pysubway.service.authentication.base import AuthenticationBase
    from pysubway.service.authentication.file import AuthenticationFile

class AuthenticationFactory:

    def __new__(self, style: str) -> Optional[type]:
        if style.lower() == 'file':
            return AuthenticationFile
        return None
