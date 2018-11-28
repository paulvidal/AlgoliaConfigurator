import os


# Get environment variable
def get_env_var(var_name):
    env_var = os.environ.get(var_name)

    if env_var is None:
        raise KeyError('Environnement variable "' + var_name + '" needs to be set! Alternatively, you can define it in the yaml file')

    return env_var