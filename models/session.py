from dataclasses import dataclass, asdict
from ftplib import FTP, error_perm, all_errors
from utils.core import Error
from io import BytesIO

@dataclass
class Session:
    """ Manage the FTP session. """
    host: str = ""
    username: str = ""
    password: str = ""

    def to_dict(self, mask_password: bool = False) -> dict:
        """ Return a dictionary of credentials. """
        data = asdict(self)
        if mask_password and "password" in data:
            data["password"] = "*****"
        return data

    def connect(self):
        """ Attempt to connect to the FTP server using stored credentials. """
        if any(v.strip() == "" for v in self.to_dict().values()):
            raise Error.MissingCredentials("Missing required credential(s).")
        try:
            self.ftp = FTP(self.host)
            self.ftp.login(self.username, self.password)
            return self
        except error_perm:
            raise Error.InvalidCredentials("Invalid credentials")
        except OSError:
            raise Error.ServerUnreachable("Couldn't reach the server.")
        except all_errors as e:
            raise Error.Unexpected("Unexpected error occurred.") from e

    def _ensure_connection(self):
        """ Ensure the FTP connection is established. """
        if not hasattr(self, "ftp") or self.ftp is None:
            raise ConnectionError("FTP connection not established.")

    def disconnect(self):
        """ Gracefully close the FTP connection. """
        self._ensure_connection()
        try:
            self.ftp.quit()
        except Exception:
            pass
        finally:
            del self.ftp

    def download_file(self, remote_path: str) -> BytesIO:
        """ Download a file from the FTP server. """
        self._ensure_connection()
        _memory_file = BytesIO()
        self.ftp.retrbinary(f"RETR {remote_path}", _memory_file.write)
        _memory_file.seek(0)
        return _memory_file

    def upload_file(self, remote_path: str, file_obj: BytesIO):
        """ Upload a file to the FTP server. """
        self._ensure_connection()
        file_obj.seek(0)
        self.ftp.storbinary(f"STOR {remote_path}", file_obj)
