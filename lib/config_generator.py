import yaml

LOCKFILE = {}
LOCKFILE_NAME = 'ALGOLIA.lock'

def init_lockfile(app_id):
    LOCKFILE['ALGOLIA_APP_ID'] = app_id
    LOCKFILE['indices'] = {}


def add_indice_to_lockfile(indice_name, settings, forward_to_replicas):
    LOCKFILE['indices'][indice_name] = {}
    LOCKFILE['indices'][indice_name]['forwardToReplicas'] = forward_to_replicas
    LOCKFILE['indices'][indice_name]['settings'] = settings


def generate_lockfile():

    with open(LOCKFILE_NAME, 'w') as yml:

        yml.write(
            "####################################################################################\n"
            "############################# THIS IS A GENERATED FILE #############################\n"
            "#############################        DO NOT EDIT       #############################\n"
            "####################################################################################\n\n"
        )

        yaml.dump(LOCKFILE, yml, allow_unicode=True)