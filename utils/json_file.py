import json
from models.session import Session
from io import BytesIO

class JSONHandler:
    """ Utility for managing JSON files over a FTP session. """
    def __init__(self, session: Session):
        self.session = session
        self.remote_path = "projects.json"

    def load(self) -> dict:
        """ Download and deserialize JSON data from the FTP server. """
        _memory_file = self.session.download_file(self.remote_path)
        return json.load(_memory_file)

    def save(self, data: dict):
        """ Serialize and upload JSON data to the FTP server. """
        _memory_file = BytesIO(json.dumps(data, indent = 4).encode("utf-8"))
        self.session.upload_file(self.remote_path, _memory_file)
