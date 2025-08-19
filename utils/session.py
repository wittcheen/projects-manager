import json
from dataclasses import dataclass, field
from ftplib import FTP, error_perm, all_errors
from io import BytesIO

@dataclass
class FTPSession:
    """ Model representing connection state and behavior. """
    _ftp: FTP = field(init = False, default = None)
    host: str = ""
    username: str = ""
    password: str = ""
    file_path: str = "projects.json"

    def to_dict(self) -> dict:
        """ Serialize session data. """
        return {
            "host": self.host,
            "username": self.username,
            "password": self.password
        }

    def connect(self):
        """ Establish FTP connection. """
        if not all([self.host, self.username, self.password]):
            raise ValueError("Missing required credential(s).")
        try:
            ftp = FTP(self.host)
            ftp.login(self.username, self.password)
            self._ftp = ftp
        except error_perm:
            raise PermissionError("Invalid FTP credentials")
        except OSError:
            raise ConnectionError("Couldn't reach FTP server.")
        except all_errors as e:
            raise RuntimeError("Unexpected FTP error.") from e

    def disconnect(self):
        """ Terminate the FTP session cleanly. """
        if self._ftp:
            try:
                self._ftp.quit()
            except all_errors:
                pass
            finally:
                self._ftp = None

    def load_json(self) -> dict:
        """ Download and deserialize JSON from remote file. """
        try:
            buffer = BytesIO()
            self._ftp.retrbinary(f"RETR {self.file_path}", buffer.write)
            buffer.seek(0)
            return json.load(buffer)
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in '{self.file_path}'")
        except all_errors as e:
            raise RuntimeError(f"Failed to load JSON from '{self.file_path}': {e}")

    def save_json(self, data: dict):
        """ Serialize and upload JSON to remote file. """
        self._require_connection()
        try:
            buffer = BytesIO(json.dumps(data, indent = 4).encode("utf-8"))
            buffer.seek(0)
            self._ftp.storbinary(f"STOR {self.file_path}", buffer)
        except all_errors as e:
            raise RuntimeError(f"Failed to save JSON to '{self.file_path}': {e}")

    def _require_connection(self):
        try:
            # Check connection; raises if dead or None
            self._ftp.voidcmd("NOOP")
        except all_errors:
            self.connect()
