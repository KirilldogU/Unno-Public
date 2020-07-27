#!/usr/bin/env python

"""This example retrieves keywords that are related to a given keyword.

The LoadFromStorage method is pulling credentials and properties from a
"googleads.yaml" file. By default, it looks for this file in your home
directory. For more information, see the "Caching authentication information"
section of our README.

"""


fileWrite = open("onlinegym.txt", "a")
from googleads import adwords


# Optional AdGroup ID used to set a SearchAdGroupIdSearchParameter.
AD_GROUP_ID = 'INSERT_AD_GROUP_ID_HERE'
PAGE_SIZE = 1000                    #number of results
rows = []

import csv


# data rows of csv file
# rows = [['Nikhil', 'COE', '2', '9.0'],
#         ['Sanchit', 'COE', '2', '9.1'],
#         ['Aditya', 'IT', '2', '9.3'],
#         ['Sagar', 'SE', '1', '9.5'],
#         ['Prateek', 'MCE', '3', '7.8'],
#         ['Sahil', 'EP', '2', '9.1']]

def ideasByKeywords(client, queries):
    # Initialize appropriate service.
    targeting_idea_service = client.GetService( 'TargetingIdeaService', version='v201809')
    count = 0

    # Construct selector object and retrieve related keywords.
    selector = {
            'ideaType': 'KEYWORD',
            'requestType': 'IDEAS'
    }

    selector['requestedAttributeTypes'] = [
            'KEYWORD_TEXT', 'SEARCH_VOLUME', 'CATEGORY_PRODUCTS_AND_SERVICES',
                'COMPETITION', 'EXTRACTED_FROM_WEBPAGE', 'SEARCH_VOLUME', 'AVERAGE_CPC',
        'TARGETED_MONTHLY_SEARCHES'
    ]

    offset = 0
    selector['paging'] = {
            'startIndex': str(offset),
            'numberResults': str(PAGE_SIZE)
    }

    selector['searchParameters'] = [{
            'xsi_type': 'RelatedToQuerySearchParameter',
            'queries': queries
    }]

    # Language setting (optional).
    selector['searchParameters'].append({
            # The ID can be found in the documentation:
            # https://developers.google.com/adwords/api/docs/appendix/languagecodes
            'xsi_type': 'LanguageSearchParameter',
            'languages': [{'id': '1000'}]
    })
    #
    # #homemade location addition
    selector['searchParameters'].append({
        'xsi_type': 'LocationSearchParameter',
        'locations': [{'id': '2048'}]
    })

    # Network search parameter (optional)
    selector['searchParameters'].append({
            'xsi_type': 'NetworkSearchParameter',
            'networkSetting': {
                    'targetGoogleSearch': True,
                    'targetSearchNetwork': False,
                    'targetContentNetwork': False,
                    'targetPartnerSearchNetwork': False
            }
    })

    more_pages = True
    while more_pages:
        page = targeting_idea_service.get(selector)

            # Display results.
        if 'entries' in page:
            for result in page['entries']:
                count += 1
                attributes = {}
                for attribute in result['data']:
                    attributes[attribute['key']] = getattr(
                        attribute['value'], 'value', '0')
                cpc = attributes['AVERAGE_CPC']
                if cpc != None:
                    cpc = "$" + str(int(cpc['microAmount']) / 1000000)
                else:
                    cpc = "None"
                print('Keyword: "%s", average monthly search volume '
                      '"%s" CPC: "%s." competition (ranked 0-1): %s '
                      % (attributes['KEYWORD_TEXT'],
                         attributes['SEARCH_VOLUME'],
                         cpc,
                         attributes['COMPETITION']))
                fileWrite.write('Keyword: "%s", average monthly search volume '
                                '"%s" CPC: "%s." competition (ranked 0-1): %s '
                                % (attributes['KEYWORD_TEXT'],
                                   attributes['SEARCH_VOLUME'],
                                   cpc,
                                   attributes['COMPETITION']) + '\n')
                rows.append([attributes['KEYWORD_TEXT'], str(attributes['SEARCH_VOLUME']), cpc, str(attributes['COMPETITION'])])
            print
        else:
            print('No related keywords were found.')
        offset += PAGE_SIZE
        selector['paging']['startIndex'] = str(offset)
        more_pages = offset < int(page['totalNumEntries'])
    print(count)

def ideasByUrl(client, urls):
    # Initialize appropriate service.
    targeting_idea_service = client.GetService( 'TargetingIdeaService', version='v201809')
    count = 0

    # Construct selector object and retrieve related keywords.
    selector = {
            'ideaType': 'KEYWORD',
            'requestType': 'IDEAS'
    }

    selector['requestedAttributeTypes'] = [
            'KEYWORD_TEXT', 'SEARCH_VOLUME', 'CATEGORY_PRODUCTS_AND_SERVICES',
                'COMPETITION', 'EXTRACTED_FROM_WEBPAGE', 'AVERAGE_CPC',
        'TARGETED_MONTHLY_SEARCHES'
    ]

    offset = 0
    selector['paging'] = {
            'startIndex': str(offset),
            'numberResults': str(PAGE_SIZE)
    }

    selector['searchParameters'] = [{
            'xsi_type': 'RelatedToUrlSearchParameter',
            'urls': urls
    }]

    # Language setting (optional).
    selector['searchParameters'].append({
            # The ID can be found in the documentation:
            # https://developers.google.com/adwords/api/docs/appendix/languagecodes
            'xsi_type': 'LanguageSearchParameter',
            'languages': [{'id': '1000'}]
    })
    #
    # #homemade location addition
    selector['searchParameters'].append({
        'xsi_type': 'LocationSearchParameter',
        'locations': [{'id': '2048'}]
    })

    # Network search parameter (optional)
    selector['searchParameters'].append({
            'xsi_type': 'NetworkSearchParameter',
            'networkSetting': {
                    'targetGoogleSearch': True,
                    'targetSearchNetwork': False,
                    'targetContentNetwork': False,
                    'targetPartnerSearchNetwork': False
            }
    })

    more_pages = True
    while more_pages:
        page = targeting_idea_service.get(selector)

            # Display results.
        if 'entries' in page:
            for result in page['entries']:
                count += 1
                attributes = {}
                for attribute in result['data']:
                    attributes[attribute['key']] = getattr(
                        attribute['value'], 'value', '0')
                cpc = attributes['AVERAGE_CPC']
                if cpc != None:
                    cpc = "$" + str(int(cpc['microAmount'])/1000000)
                else:
                    cpc = "None"
                print('Keyword: "%s", average monthly search volume '
                      '"%s" CPC: "%s." competition (ranked 0-1): %s '
                      % (attributes['KEYWORD_TEXT'],
                         attributes['SEARCH_VOLUME'],
                         cpc,
                         attributes['COMPETITION']))
                fileWrite.write('Keyword: "%s", average monthly search volume '
                      '"%s" CPC: "%s." competition (ranked 0-1): %s '
                      % (attributes['KEYWORD_TEXT'],
                         attributes['SEARCH_VOLUME'],
                         cpc,
                         attributes['COMPETITION']) + '\n')
                rows.append([attributes['KEYWORD_TEXT'], str(attributes['SEARCH_VOLUME']), cpc, str(attributes['COMPETITION'])])
            print
        else:
            print('No related keywords were found.')
        offset += PAGE_SIZE
        selector['paging']['startIndex'] = str(offset)
        more_pages = offset < int(page['totalNumEntries'])
    print(count)


adwords_client = adwords.AdWordsClient.LoadFromStorage()
ideasByKeywords(adwords_client, ['home fitness club'])
print(rows)
#ideasByUrl(adwords_client, ['https://bew.marplist.com/'])
fileWrite.close()



# field names
fields = ['Keyword Text', 'Average Monthly Searches', 'CPC', 'Competition (ranked 0-1)']
# name of csv file
filename = "homefitnessclub.csv"

# writing to csv file
with open(filename, 'w', newline='') as csvfile:
	# creating a csv writer object
	csvwriter = csv.writer(csvfile)

	# writing the fields
	csvwriter.writerow(fields)

	# writing the data rows
	csvwriter.writerows(rows)