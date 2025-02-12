import os
import time

settings_file = "settings"
settings_update_interval = 5 * 60

defaults = {
        "client_secrets_file": os.path.expanduser("~/.google_client/improved_subscriptions_secret.json"),
        "initial_subscription_backdate": 14,
        "subscriptions_dir": os.path.join(os.path.dirname(__file__), 'subscriptions') 
        }

class Settings:
    def read_settings(self):
        try:
            settings_dict = {}
            with open(settings_file, 'rt') as f:
                lines = f.readlines()
            settings_dict = { tokens[0].strip() : tokens[1].strip() for tokens in
                        [x.split('=') for x in lines] }


            with open(settings_file, 'at') as f:
                for k in defaults:
                    if k not in settings_dict:
                        settings_dict[k] = defaults[k]
                        f.write(f"{k} = {defaults[k]}\n")
                for k in list(settings_dict.keys()):
                    if k not in defaults:
                        del settings_dict[k]
        except FileNotFoundError:
            with open(settings_file, 'wt') as f:
                for k in defaults:
                    settings_dict[k] = defaults[k]
                    f.write(f"{k} = {defaults[k]}\n")
        return settings_dict

    def __init__(self):
        settings_dict = self.read_settings()
        for k in settings_dict:
            try:
                val = eval(settings_dict[k])
            except:
                val = settings_dict[k]
            setattr(self, k, val)

        cred_dirname = os.path.dirname(settings_dict['client_secrets_file'])
        setattr(self, 'auth_token_file', os.path.join(cred_dirname, 'token.json'))

_settings = Settings()
_last_settings_update = time.time()
def get_settings():
    global _settings
    if time.time() - _last_settings_update > settings_update_interval:
        _settings = Settings()
    return _settings

def reset_settings_to_default():
    if os.path.exists(settings_file):
        os.remove(settings_file)

    Settings()
