import collections
import yaml
import emoji

from lib.config_generator import LOCKFILE_NAME, LOCKFILE


def display_change(name, new, old, depth=0):
    new = new if new is not None else emoji.emojize(':no_entry_sign:', use_aliases=True)
    old = old if old is not None else emoji.emojize(':no_entry_sign:', use_aliases=True)

    prGreen(" " * depth + 'NEW ' + name + ':', new)
    prRed(" " * depth + 'OLD ' + name + ':', old)
    print()


def display_rename(name, new, old, depth=0):
    new = new if new is not None else emoji.emojize(':no_entry_sign:', use_aliases=True)
    old = old if old is not None else emoji.emojize(':no_entry_sign:', use_aliases=True)

    prGreen(" " * depth + 'RENAMED ' + name + ':', new)
    prRed(" " * depth +   'OLD ' + name + ':    ', old)
    print()


def display_add(name, new, depth=0):
    prGreen(" " * depth + 'ADD ' + name + ':', new)
    print()


def display_delete(name, old, depth=0):
    prRed(" " * depth + 'DELETE ' + name + ': ', old)
    print()



def prGreen(p, skk): print("{}\033[92m {}\033[00m" .format(p, skk))
def prRed(p, skk): print("{}\033[91m {}\033[00m" .format(p, skk))


def print_diff(differences, operations, changes):
    if not changes:
        print('No changes detected!')
        return

    print('\nComparing changes\n')

    diff = differences.get('ALGOLIA_APP_ID')

    if diff:
        display_change('ALGOLIA_APP_ID', diff[0], diff[1])

    for indice in differences['indices']:
        print_indice = True
        indice_options = differences['indices'].get(indice)

        if isinstance(indice_options, tuple):
            new, old = indice_options
            action = False

            for o in operations:
                if o[0] == 'delete' and o[1] == old:
                    display_delete('indice', old)
                    action = True
                elif o[0] == 'rename' and o[2] == new:
                    display_rename('indice', o[2], o[1])
                    action = True

            if not action:
                # must be an add
                display_add('indice', new)


        else:
            forwardToReplicas = indice_options.get('forwardToReplicas')
            settings = indice_options['settings']

            if forwardToReplicas:
                if print_indice:
                    print('MODIFY indice: {}'.format(indice))
                    print_indice = False
                display_change('forwardToReplicas', forwardToReplicas[0], forwardToReplicas[1], depth=2)

            print_settings = True

            for s in settings:
                if s:
                    if print_indice:
                        print('MODIFY indice: {}'.format(indice))
                        print_indice = False
                    if print_settings:
                        print('  Settings:')
                        print_settings = False

                    display_change(s, settings[s][0], settings[s][1], depth=4)


# Determine the indices to remove compare to the previous file, and check for renames
def compute_operations(differences, changes, lockfile_index_names, previous_lockfile):
    if not changes:
        return []

    operations = []

    for indice in differences['indices']:
        indice_options = differences['indices'].get(indice)

        if isinstance(indice_options, tuple):
            new, old = indice_options

            if new is None and old is not None:
                new_name = None

                # Check if a deletion or a rename
                for name in lockfile_index_names:
                    if are_indices_same(name, old, LOCKFILE, previous_lockfile):
                        new_name = name
                        break

                if new_name is not None:
                    operations.append(('rename', old, new_name))
                else:
                    operations.append(('delete', old))

    return operations


def compare_with_previous_lockfile(previous_lockfile):
    changes = False
    differences = collections.OrderedDict()

    # Compare lockfiles
    if LOCKFILE['ALGOLIA_APP_ID'] != previous_lockfile['ALGOLIA_APP_ID']:
        differences['ALGOLIA_APP_ID'] = (LOCKFILE['ALGOLIA_APP_ID'], previous_lockfile['ALGOLIA_APP_ID'])
        changes = True

    differences['indices'] = collections.OrderedDict()

    # Check additions
    for indice in LOCKFILE['indices']:
        changes = compare_indice(indice, LOCKFILE, previous_lockfile, differences) or changes

    # Check for deletions
    for indice in previous_lockfile['indices']:
        if indice in LOCKFILE['indices']:
            continue

        changes = compare_indice(indice, LOCKFILE, previous_lockfile, differences) or changes

    return differences, changes


def compare_indice(indice, lockfile, previous_lockfile, differences):
    changes = False
    indice_options = lockfile['indices'].get(indice)
    old_indice_options = previous_lockfile['indices'].get(indice)

    if not old_indice_options:
        differences['indices'][indice] = (indice, None)
        return True
    elif not indice_options:
        differences['indices'][indice] = (None, indice)
        return True

    differences['indices'][indice] = collections.OrderedDict()

    forwardToReplicas = indice_options.get('forwardToReplicas')
    old_forwardToReplicas = old_indice_options.get('forwardToReplicas')

    settings = indice_options['settings']
    old_settings = old_indice_options['settings']

    if forwardToReplicas != old_forwardToReplicas:
        differences['indices'][indice]['forwardToReplicas'] = (forwardToReplicas, old_forwardToReplicas)
        changes = True

    differences['indices'][indice]['settings'] = collections.OrderedDict()

    for s in settings:
        setting = settings.get(s)
        old_setting = old_settings.get(s)

        if setting != old_setting:
            differences['indices'][indice]['settings'][s] = (setting, old_setting)
            changes = True

    return changes


def are_indices_same(indice_lockfile, indice_previous_lockfile, lockfile, previous_lockfile):
    is_same = True
    indice_options = lockfile['indices'].get(indice_lockfile)
    old_indice_options = previous_lockfile['indices'].get(indice_previous_lockfile)

    forwardToReplicas = indice_options.get('forwardToReplicas')
    old_forwardToReplicas = old_indice_options.get('forwardToReplicas')

    settings = indice_options['settings']
    old_settings = old_indice_options['settings']

    if forwardToReplicas != old_forwardToReplicas:
        is_same = False

    for s in settings:
        setting = settings.get(s)
        old_setting = old_settings.get(s)

        if setting != old_setting:
            is_same = False

    return is_same