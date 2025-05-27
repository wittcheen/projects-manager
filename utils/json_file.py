import json
from models.session import Session
from io import BytesIO

class JSONHandler:
    """ Utility for managing JSON files over a FTP session. """
    def __init__(self, session: Session, remote_path: str):
        self.session = session
        self.remote_path = remote_path

    def load(self) -> dict:
        """ Download and deserialize JSON data from the FTP server. """
        try:
            _memory_file = self.session.download_file(self.remote_path)
            return json.load(_memory_file)
        except Exception as e:
            raise FileNotFoundError(f"Failed to load JSON file: {e}")

    def save(self, data: dict):
        """ Serialize and upload JSON data to the FTP server. """
        try:
            _memory_file = BytesIO(json.dumps(data, indent = 4).encode("utf-8"))
            self.session.upload_file(self.remote_path, _memory_file)
        except Exception as e:
            raise IOError(f"Failed to save JSON file: {e}")
