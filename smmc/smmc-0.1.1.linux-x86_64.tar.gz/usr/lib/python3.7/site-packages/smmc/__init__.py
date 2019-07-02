import json
import base64
import os.path
from typing import Dict


class SMMC(object):
    def __init__(self, message_limiter=["---BEGIN-SCANNERMANAGER-MESSAGE---", "---END-SCANNERMANAGER-MESSAGE---"]):
        """
        Scanner Manager Message Coder is a library offering functions to set Atlas Scan Status and send Scan Output via StdOut. 
        When writing scripts for Atlas Docker Containers make sure you never write something to StdOut because it's the standard 
        way to send messages to Atlas.

        Params:
        message_limiter (List[str]): Limiter strings used to mark begin and end of ATLAS message
        """
        self._message_limiter = message_limiter

    def send_status(self, status: str, details: Dict = {}):
        """send a status update"""
        message: Dict = {
            "message_type": "status", "payload": {"status": status,
                                                  "details": details}
        }
        self.__send_message(message)

    def __send_output(self, filename: str, encoding: str, payload, description: str = None):
        """send an output file in given encoding"""
        message = {"message_type": "output", "encoding": encoding, "filename": filename,
                   "payload": payload}

        if description:
            message["description"] = description

        self.__send_message(message)

    def send_output_string(self, filename: str, payload: str, description: str = None):
        """send a string as output file"""
        if not isinstance(payload, str):
            raise Exception("payload is no valid object of type string")
        self.__send_output(filename=filename, encoding="plaintext",
                           payload=payload, description=description)

    def send_output_json(self, filename: str, payload: Dict, description: str = None):
        """send a json as output"""
        self.__send_output(filename=filename, encoding="json",
                           payload=payload, description=description)

    def send_output_file(self, path_to_file: str, filename=None, description: str = None):
        if not os.path.isfile(path_to_file):
            raise Exception("File is not existent")
        with open(path_to_file, "rb") as f:
            file_bytes = f.read()
        payload = base64.b64encode(file_bytes).decode()
        original_filename = os.path.basename(path_to_file)
        if not filename:
            filename = original_filename
        self.__send_output(filename=filename, payload=payload,
                           description=description, encoding="base64")

    def __send_message(self, message: Dict):
        """send message encoded as json and having start and end limiter """
        message_json: str = json.dumps(message)
        print(self._message_limiter[0])
        print(message_json)
        print(self._message_limiter[1])
