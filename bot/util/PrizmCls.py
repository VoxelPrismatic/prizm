class PrizmList(list):
    def __le__(self, item):
        self.append(item)
    def __ge__(self, item):
        self.remove(item)
    def __invert__(self):
        self = self[::-1]
    def __isub__(self, data):
        for item in data:
            self => item
    def __iadd__(self, data):
        for item in data:
            self <= item

class PrizmDict(dict):
    def __le__(self, other_dict):
        key_val = [(key, other_dict[key]) for key in other_dict]
        for key, val in key_val:
            self[key] = val
    def __ge__(self, key):
        del self[key]
