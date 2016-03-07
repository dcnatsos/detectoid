
from itertools import groupby


def group_by_date(users):
    """ group accounts by creation date """

    def group(elem):
        return elem.created

    users = sorted(users, key=group)
    groups = {}

    for k, g in groupby(users, group):
        groups[k] = list(g)

    return {
        date.isoformat(): len(groups[date])
        for date in sorted(groups.keys())
    }
