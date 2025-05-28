import keyring
import keyring.errors
import json

class KeyVault:
    _SERVICE = "wittcheen/projects-manager"
    _USERNAME = "default"

    @classmethod
    def store(cls, credentials: dict):
        """ Store credentials to the keyring. """
        try:
            keyring.set_password(cls._SERVICE, cls._USERNAME, json.dumps(credentials))
        except keyring.errors.PasswordSetError:
            pass

    @classmethod
    def retrieve(cls) -> dict | None:
        """ Retrieve credentials from the keyring. """
        try:
            data = keyring.get_password(cls._SERVICE, cls._USERNAME)
            return json.loads(data) if data else None
        except keyring.errors.KeyringError:
            return None

    @classmethod
    def delete(cls):
        """ Delete credentials from the keyring. """
        try:
            keyring.delete_password(cls._SERVICE, cls._USERNAME)
        except keyring.errors.PasswordDeleteError:
            pass
