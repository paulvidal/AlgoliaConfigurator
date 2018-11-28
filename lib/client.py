from algoliasearch import algoliasearch

class AlgoliaClient:

    def __init__(self):
        self.client = None

    def init(self, app_id, api_key):
        self.client = algoliasearch.Client(app_id, api_key)

    def get_index(self, name):
        return self.client.init_index(name)

    def delete_index(self, name):
        return self.client.delete_index(name)

    def rename_index(self, old, new):
        return self.client.move_index(old, new)

    def get_all_indices(self):
        return self.client.list_indexes()

    def get_all_indice_names(self):
        return [i['name'] for i in self.get_all_indices()['items']]


ALGOLIA_CLIENT = AlgoliaClient()