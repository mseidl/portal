import re


def get_stats(html):
    results = []
    fail = False
    tmp = re.search('\d{1,4}\sscenarios.*\)";', html).group()
    list = re.sub(r'[^a-zA-Z0-9]', ' ', tmp).split()
    list.remove('br')
    if 'failed' in list:
        fail = True
    results.append(list[0])
    if fail:
        results.append(list[2])
        results.append(list[4])
    else:
        results.append(0)
        results.append(list[2])
    if fail:
        results.append(list[6])
        results.append(list[8])
        results.append(list[10])
    else:
        results.append(list[4])
        results.append(0)
        results.append(list[6])
    return results


