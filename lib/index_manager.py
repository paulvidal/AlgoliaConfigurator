import collections

from lib.Setting import AlgoliaSetting
from lib.client import ALGOLIA_CLIENT

"""
Settings as explained in Algolia API doc
https://www.algolia.com/doc/api-reference/settings-api-parameters/
"""


def get_index_settings(options):
    forward_to_replicas = options.get('forwardToReplicas') if options.get('forwardToReplicas') else False
    settings = options.get('settings')

    algolia_settings = [
        # attributes
        AlgoliaSetting('searchableAttributes', settings, default=[]),
        AlgoliaSetting('attributesForFaceting', settings, default=[]),
        AlgoliaSetting('unretrievableAttributes', settings, default=[]),
        AlgoliaSetting('attributesToRetrieve', settings, default=['*']),

        # # ranking
        AlgoliaSetting('ranking', settings, default=["typo", "geo", "words", "filters", "proximity", "attribute", "exact"]),
        AlgoliaSetting('customRanking', settings, default=[]),
        AlgoliaSetting('replicas', settings, default=[]),

        # faceting
        AlgoliaSetting('maxValuesPerFacet', settings, default=100),
        AlgoliaSetting('sortFacetValuesBy', settings, default='count'),

        # highlighting-snippeting
        AlgoliaSetting('attributesToHighlight', settings, default=['null']),
        AlgoliaSetting('attributesToSnippet', settings, default=[]),
        AlgoliaSetting('highlightPreTag', settings, default="<em>"),
        AlgoliaSetting('highlightPostTag', settings, default="</em>"),
        AlgoliaSetting('snippetEllipsisText', settings, default='...'),
        AlgoliaSetting('restrictHighlightAndSnippetArrays', settings, default=False),

        # pagination
        AlgoliaSetting('hitsPerPage', settings, default=20),
        AlgoliaSetting('paginationLimitedTo', settings, default=1000),

        # typos
        AlgoliaSetting('minWordSizefor1Typo', settings, default=4),
        AlgoliaSetting('minWordSizefor2Typos', settings, default=8),
        AlgoliaSetting('typoTolerance', settings, default=True),
        AlgoliaSetting('allowTyposOnNumericTokens', settings, default=True),
        AlgoliaSetting('disableTypoToleranceOnAttributes', settings, default=[]),
        AlgoliaSetting('disableTypoToleranceOnWords', settings, default=[]),
        AlgoliaSetting('separatorsToIndex', settings, default=""),

        # languages
        AlgoliaSetting('ignorePlurals', settings, default=False),
        AlgoliaSetting('removeStopWords', settings, default=False),
        AlgoliaSetting('camelCaseAttributes', settings, default=[]),
        AlgoliaSetting('decompoundedAttributes', settings, default={}),
        AlgoliaSetting('keepDiacriticsOnCharacters', settings, default=""), # Not in settings refresh ye
        AlgoliaSetting('queryLanguages', settings, default=[]),

        # query-rules
        AlgoliaSetting('enableRules', settings, default=True),

        # query-strategy
        AlgoliaSetting('queryType', settings, default="prefixLast"),
        AlgoliaSetting('removeWordsIfNoResults', settings, default="none"),
        AlgoliaSetting('advancedSyntax', settings, default=False),
        AlgoliaSetting('optionalWords', settings, default=[]),
        AlgoliaSetting('disablePrefixOnAttributes', settings, default=[]),
        AlgoliaSetting('disableExactOnAttributes', settings, default=[]),
        AlgoliaSetting('exactOnSingleWordQuery', settings, default='atribute'),
        AlgoliaSetting('alternativesAsExact', settings, default=["ignorePlurals", "singleWordSynonym"]),

        # performance
        AlgoliaSetting('numericAttributesForFiltering', settings, default=['null']), # Not in settings refresh ye
        AlgoliaSetting('allowCompressionOfIntegerArray', settings, default=False),

        # advanced
        AlgoliaSetting('attributeForDistinct', settings, default='null'),
        AlgoliaSetting('distinct', settings, default=0),
        AlgoliaSetting('replaceSynonymsInHighlight', settings, default=True),
        AlgoliaSetting('minProximity', settings, default=1),
        AlgoliaSetting('responseFields', settings, default=['*']),
        AlgoliaSetting('maxFacetHits', settings, default=10),
    ]

    # Create the dictionary required by the API
    algolia_settings_dic = {}

    for algolia_setting in algolia_settings:
        algolia_setting.add_itself_to_settings(algolia_settings_dic)

    return algolia_settings_dic, forward_to_replicas


def apply_index_settings(name, algolia_settings_dic, forward_to_replicas):
    index = ALGOLIA_CLIENT.get_index(name)
    index.set_settings(algolia_settings_dic, forward_to_replicas=forward_to_replicas)


def delete_index(name):
    ALGOLIA_CLIENT.delete_index(name)