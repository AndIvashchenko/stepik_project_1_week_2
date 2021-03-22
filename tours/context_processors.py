from tours.data import departures


def departures_context(request):
    return {'departures': departures, }
