class GeoTree:
    def __init__(self, g_ln=9):
        self.tree = dict()
        self.count = 0
        self.g_ln = g_ln

    def flush(self):
        self.tree = dict()
        self.count = 0

    def insert_geohash(self, geohash, row):
        self.count += 1
        geohash = geohash[:self.g_ln]
        self.fill_hlp(self.tree, geohash, row)

    def fill_hlp(self, tmp, geohash, row):
        if 'ls' in tmp:
            tmp['ls'].append(row)
        else:
            tmp.update({'ls': [row]})

        if len(geohash) == 1:
            if geohash[0] in tmp:
                tmp[geohash[0]].append(row)
            else:
                tmp.update({geohash[0]: [row]})
        else:
            head, *tail = geohash
            if head in tmp:
                self.fill_hlp(tmp[head], tail, row)
            else:
                tmp[head] = dict()
                self.fill_hlp(tmp[head], tail, row)

    def print_tree(self):
        print(self.tree)

    def entire(self):
        return self.tree['ls']

    def find(self, geohash, ls=True):
        if len(geohash) < self.g_ln:
            return self.find_hlp(geohash, self.tree, ls)
        else:
            return self.find_hlp(geohash[:self.g_ln], self.tree, False)

    def find_hlp(self, geohash, tmp, ls=False):
        if len(geohash) == 0:
            if ls:
                return tmp['ls']
            return tmp
        head, *tail = geohash
        if head in tmp:
            return self.find_hlp(tail, tmp[head], ls)
        return []

    def range_find(self, geohash, start=None, end=4):
        if start is None:
            start = self.g_ln
        res = []
        while not res and start > end:
            res = self.find(geohash[0:start])
            start -= 1
        return res
