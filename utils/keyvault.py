import keyring, keyring.errors
import json

class KeyVault:
    _ID = "wittcheen/projects-manager"

    @classmethod
    def store(cls, credentials: dict):
        """ Store credentials to the system keyring. """
        try:
            cls.delete()
            keyring.set_password(cls._ID, cls._ID, json.dumps(credentials))
        except keyring.errors.PasswordSetError:
            pass

    @classmethod
    def retrieve(cls) -> dict | None:
        """ Retrieve credentials from the system keyring. """
        try:
            data = keyring.get_password(cls._ID, cls._ID)
            return json.loads(data) if data else None
        except keyring.errors.KeyringError:
            return None

    @classmethod
    def delete(cls):
        """ Delete credentials from the system keyring. """
        try:
            keyring.delete_password(cls._ID, cls._ID)
        except keyring.errors.PasswordDeleteError:
            pass
