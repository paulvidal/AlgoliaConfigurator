import emoji

from lib import config_generator, config_comparator, index_manager
from lib.client import ALGOLIA_CLIENT
from lib.config_generator import LOCKFILE_NAME
from lib.helper import get_env_var
from lib.index_manager import get_index_settings
from lib import parser

CONFIG_FILE_NAME = 'algolia.yaml'

CONFIG = parser.read_yaml(CONFIG_FILE_NAME)
PREVIOUS_LOCK_FILE = parser.read_yaml(LOCKFILE_NAME)

if not CONFIG:
    exit(1)

# Read config variables
APP_ID = CONFIG.get('ALGOLIA_APP_ID') if CONFIG.get('ALGOLIA_APP_ID') else get_env_var('ALGOLIA_APP_ID')
API_KEY = CONFIG.get('ALGOLIA_API_KEY') if CONFIG.get('ALGOLIA_API_KEY') else get_env_var('ALGOLIA_API_KEY')

# Init the client
ALGOLIA_CLIENT.init(APP_ID, API_KEY)

# Init the lockfile
config_generator.init_lockfile(APP_ID)

# Manage each index
indexes = CONFIG.get('indices') if CONFIG.get('indices') else []
index_names = [k for i in indexes for k in i]

for index in indexes:
    for name in index:
        settings, forward_to_replicas = get_index_settings(index[name])
        config_generator.add_indice_to_lockfile(name, settings, forward_to_replicas)

# Check the differences between previous and new LOCKFILE
operations = []

if PREVIOUS_LOCK_FILE:
    diff, changes = config_comparator.compare_with_previous_lockfile(PREVIOUS_LOCK_FILE)
    operations = config_comparator.compute_operations(diff, changes, index_names, PREVIOUS_LOCK_FILE)
    config_comparator.print_diff(diff, operations, changes)
else:
    changes = True
    print('As {} does not exist, a new configuration will be applied.'.format(LOCKFILE_NAME))
    print('It is strongly recommended to keep the LOCKFILE, and to only edit {}\n'.format(CONFIG_FILE_NAME))

if not changes:
    exit(0)

input = input("Do you want to continue? (y) - Only 'y' will be accepted\n")

if input != 'y':
    exit(0)

# Apply the changes to indexes
print('Applying changes...')

for index in indexes:
    for name in index:
        settings, forward_to_replicas = get_index_settings(index[name])
        index_manager.apply_index_settings(name, settings, forward_to_replicas)

# Perform the operations
for op in operations:
    if op[0] == 'delete':
        ALGOLIA_CLIENT.delete_index(op[1])
    elif op[0] == 'rename':
        ALGOLIA_CLIENT.rename_index(op[1], op[2])

# Generate the lockfile
config_generator.generate_lockfile()

# Confirmation message
print('Changes applied successfully ' + emoji.emojize(':white_check_mark:', use_aliases=True))