_porn_collection_site_names = ['xvideos', 'pornhub', 'my boobsMyBoobs',
                               'premiumbukkake', 'xxx', 'kinkvrKinkVR', 'nf bustyNF Busty', 'behappy2dayBeHappy2day', 'streamrayStreamRay',
                               'xraresXRares', 'tubev']


def _get_site_name(url):
    url = url.split('//')[1].split('.')
    if (url[0] == 'www'):
        url = url[1]
    else:
        url = url[0]
    return url


def _get_porn_collection():
    collection = []
    for i in _porn_collection_site_names:
        line = i.lower()
        line = line.strip()
        line = line.replace(' ', '')
        collection.append(line)
        # print(collection)

    return collection
