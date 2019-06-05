from collections import defaultdict
from collections import UserDict
from collections.abc import Iterable
from collections.abc import Hashable
from itertools import filterfalse


class MultivaluedDictError(Exception):
    pass

class KeyValuePairsError(MultivaluedDictError):
    def __init__(self, list_of_not_kv_pair):
        self.list_of_not_kv_pair = list_of_not_kv_pair

    def __repr__(self):
        return f'{list_of_not_kv_pair} these items do not form key-value pairs. '

class HashError(MultivaluedDictError):
    def __init__(self, list_of_not_hash):
        self.list_of_not_hash = list_of_not_hash

    def __repr__(self):
        return f'{list_of_not_hash} these are unhashable. '

class multivalued_dict(UserDict):
    START = 'S'
    END = 'E'

    @classmethod
    def __is_multivalued_dict__(cls, x):
        return (isinstance(x, multivalued_dict) or ((True if x.default_factory == type([]) else False) if isinstance(x, defaultdict) else False))

    def __init__(self, initial_items):
        self.data = defaultdict(list)
        if multivalued_dict.__is_multivalued_dict__(initial_items):
            self.__mvdict_init__(initial_items)
        else:
            self.update(initial_items)

    def __mvdict_init__(self, multivalued_init_items):
        if multivalued_dict.__is_multivalued_dict__(multivalued_init_items):
            self.data = multivalued_init_items
        else:
            raise TypeError(f"{type(multivalued_init_items)}  objects are not multivalued_dict or defaultdict(<class 'list'>) objects. ")

    def __repr__(self):
        return f'multivalued_dict({dict(self.data)})'

    def __lenvalue__(self, key = None):
        if key == None:
            return sum(map(len, self.data.values()))
        else:
            return len(self.data[key])

    def __matchkv__(self, key, value):
        return value in self.data[key]

    def __delkv__(self, key, value, allkv = True, direction = START):
        assert allkv in (True, False), '"allkv" can only be True or False.'
        assert direction in (self.START, self.END), '"direction" can only be START or END.'

        if allkv:
            while value in self.data[key]:
                self.data[key].remove(value)
        else:
            if direction == self.START:
                self.data[key].remove(value)
            elif direction == self.END:
                value_len = len(self.data[key])
                for i in range(value_len):
                    if self.data[key][-1 - i] == value:
                        self.data[key].__delitem__(-1 - i)
                        break

    def count(self, key, value):
        return self.data[key].count(value)

    def update(self, update_items):
        if isinstance(update_items, Iterable):
            if isinstance(update_items, dict):
                for _key, _value in update_items.items():
                    self.data[_key].append(_value)
            else:
                list_of_not_kv_pair = list(filterfalse(lambda item: len(item) == 2, update_items))  #找出不是两个元素的项，也就是无法构成键值对的项
                if list_of_not_kv_pair == []:
                    list_of_not_hash = list(filterfalse(lambda _key: isinstance(_key, Hashable), (item[0] for item in update_items)))
                    if list_of_not_hash == []:  #检测所有键必须可散列
                        for _key, _value in update_items:
                            self.data[_key].append(_value)
                    else:
                        raise HashError(list_of_not_hash)
                else:
                    raise KeyValuePairsError(list_of_not_kv_pair)
        else:
            raise TypeError(f'{type(update_items)} object is not iterable. ')

    def reverse(self, key):
        self.data[key].reverse()

    def copy(self):
        return multivalued_dict(self.data)

    def items(self):
        return self.data.items()

    def keys(self):
        return self.data.keys()

    def values(self):
        return self.data.values()

    @classmethod
    def fromkeys(cls, initial_keys, value = None):
        dict_var = dict.fromkeys(initial_keys, value)
        return multivalued_dict(dict_var)
