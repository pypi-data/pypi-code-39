from typing import Dict

import jwt


class Jwt:

    @staticmethod
    def encode(data: Dict) -> str:
        return jwt.encode(data, 'secret', algorithm='HS256')

    @staticmethod
    def decode(encoded: str) -> Dict:
        return jwt.decode(encoded, 'secret', algorithms=['HS256'])
