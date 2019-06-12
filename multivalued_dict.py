from collections import defaultdict
from collections import UserDict
from collections.abc import Iterable

START_POS = 'S'
END_POS = 'E'

class MultivaluedDictError(Exception):
    pass
    
class KeyValuePairsError(MultivaluedDictError):
    def __init__(self, list_of_not_kv_pair):
        self.list_of_not_kv_pair = list_of_not_kv_pair
        
    def __repr__(self):
        return f'{list_of_not_kv_pair} does not form a key-value pair. '
    
class multivalued_dict(UserDict):
    '''
        >>> mv_d = multivalued_dict()
        >>> mv_d
        multivalued_dict({})
        
        >>> mv_d = multivalued_dict({'a': 'test-1', 'b': 'test-2', 'c': 'test-3'})
        >>> mv_d
        multivalued_dict({'a': ['test-1'], 'b': ['test-2'], 'c': ['test-3']})
        
        >>> mv_d = multivalued_dict([['a', 'test-1'], ['b', 'test-2'], ['a', 'test-3']])
        >>> mv_d
        multivalued_dict({'a': ['test-1', 'test-3'], 'b': ['test-2']})
        
        >>> mv_d = multivalued_dict(a = 'test-1', b = 'test-2', c = 'test-3')
        >>> mv_d
        multivalued_dict({'a': ['test-1'], 'b': ['test-2'], 'c': ['test-3']})
        
        >>> mv_d = multivalued_dict([['a', 'test-1'], ['c', 'test-3']], b = 'test-2')
        >>> mv_d
        multivalued_dict({'a': ['test-1'], 'c': ['test-3'], 'b': ['test-2']})
        
        >>> mv_d0 = multivalued_dict({'a': 'test-1', 'b': 'test-2', 'c': 'test-3'})
        >>> mv_d0
        multivalued_dict({'a': ['test-1'], 'b': ['test-2'], 'c': ['test-3']})
        >>> mv_d = multivalued_dict(mv_d0)
        >>> mv_d
        multivalued_dict({'a': ['test-1'], 'b': ['test-2'], 'c': ['test-3']})
    '''

    @classmethod
    def __is_multivalued_dict__(cls, x):
        '''
        >>> mv_d = multivalued_dict()
        >>> multivalued_dict.__is_multivalued_dict__(mv_d)
        True
        '''
        return (isinstance(x, cls) or ((True if x.default_factory == type([]) else False) if isinstance(x, defaultdict) else False))
    
    def __init__(self, *args, **kwargs):
        '''
            >>> mv_d = multivalued_dict({'a': 'test-1', 'b': 'test-2', 'c': 'test-3'})
            >>> mv_d
            multivalued_dict({'a': ['test-1'], 'b': ['test-2'], 'c': ['test-3']})
            
            >>> mv_d.__init__({'d': 'test-4'})
            >>> mv_d
            multivalued_dict({'a': ['test-1'], 'b': ['test-2'], 'c': ['test-3'], 'd': ['test-4']})
            
            >>> multivalued_dict.__init__(mv_d, {'e': 'test-5'})
            >>> mv_d
            multivalued_dict({'a': ['test-1'], 'b': ['test-2'], 'c': ['test-3'], 'd': ['test-4'], 'e': ['test-5']})
        '''
        if not multivalued_dict.__is_multivalued_dict__(self):
            raise TypeError(f"descriptor '__init__' requires a 'multivalued_dict' object but received a {type(self)}")
        len_of_args = len(args)
        if len_of_args > 1:
            raise TypeError(f'expected at most 1 arguments, got {len_of_args}')
        else:
            if 'data' not in self.__dict__:
                self.data = defaultdict(list)
            if len_of_args == 1:
                initial_items = args[0]
                self.update(initial_items)
        if kwargs != dict():
            self.update(kwargs)
    
    def __repr__(self):
        return f'multivalued_dict({dict(self.data)})'
    
    def __lenvalue__(self, key = None):
        '''
            >>> mv_d = multivalued_dict([['a', 1], ['a', 2], ['a', 3], ['b', 1], ['b', 2], ['c', 1]])
            >>> mv_d.__lenvalue__()
            6
            >>> mv_d.__lenvalue__('a')
            3
        '''
        if key == None:
            return sum(map(len, self.data.values()))
        else:
            return len(self.data[key])
    
    def __matchkv__(self, key, value):
        '''
            >>> mv_d = multivalued_dict([['a', 1], ['a', 2], ['a', 3], ['b', 1], ['b', 2], ['c', 1]])
            >>> mv_d.__matchkv__('b', 3)
            False
            >>> mv_d.__matchkv__('a', 2)
            True
            >>> mv_d.__matchkv__('d', 1)
            False
        '''
        return value in self.data[key]
        
    def __delkv__(self, key, value, allkv = True, direction = START_POS):
        '''
            >>> mv_d = multivalued_dict([['a', 'x'], ['a', 'y'], ['a', 'z'], ['a', 'y'], ['a', 'z'], ['a', 'y']])
            >>> mv_d
            multivalued_dict({'a': ['x', 'y', 'z', 'y', 'z', 'y']})
            
            >>> mv_d.__delkv__('a', 'y', False)
            >>> mv_d
            multivalued_dict({'a': ['x', 'z', 'y', 'z', 'y']})
            
            >>> mv_d.__delkv__('a', 'y', False, END_POS)
            >>> mv_d
            multivalued_dict({'a': ['x', 'z', 'y', 'z']})
            
            >>> mv_d.__delkv__('a', 'z')
            >>> mv_d
            multivalued_dict({'a': ['x', 'y']})
        '''
        assert allkv in (True, False), '"allkv" can only be True or False'
        assert direction in (START_POS, END_POS), '"direction" can only be START_POS or END_POS'
        
        if allkv:
            while value in self.data[key]:
                self.data[key].remove(value)
        else:
            if direction == START_POS:
                self.data[key].remove(value)
            elif direction == END_POS:
                value_len = len(self.data[key])
                for i in range(value_len):
                    if self.data[key][-1 - i] == value:
                        self.data[key].__delitem__(-1 - i)
                        break

    def count(self, key, value):
        '''
            >>> mv_d = multivalued_dict([['a', 'x'], ['a', 'y'], ['a', 'y'], ['a', 'z'], ['a', 'z'], ['a', 'z']])
            >>> mv_d.count('a', 'y')
            2
        '''
        return self.data[key].count(value)
    
    def update(self, *args, **kwargs):
        '''
            >>> mv_d = multivalued_dict()
            >>> mv_d
            multivalued_dict({})
            
            >>> mv_d.update({'a': 'test-1', 'b': 'test-2', 'c': 'test-3'})
            >>> mv_d
            multivalued_dict({'a': ['test-1'], 'b': ['test-2'], 'c': ['test-3']})
            
            >>> mv_d.update([['a', 'test-4'], ['a', 'test-5']])
            >>> mv_d
            multivalued_dict({'a': ['test-1', 'test-4', 'test-5'], 'b': ['test-2'], 'c': ['test-3']})
            
            >>> mv_d.update(c = 'test-3')
            >>> mv_d
            multivalued_dict({'a': ['test-1', 'test-4', 'test-5'], 'b': ['test-2'], 'c': ['test-3', 'test-3']})
            
            >>> mv_d.update([['b', 'test-6'], ['c', 'test-7']], a = 'test-8')
            >>> mv_d
            multivalued_dict({'a': ['test-1', 'test-4', 'test-5', 'test-8'], 'b': ['test-2', 'test-6'], 'c': ['test-3', 'test-3', 'test-7']})
            
            >>> mv_d.update(multivalued_dict({'d': 'test-9', 'e': 'test-10'}))
            >>> mv_d
            multivalued_dict({'a': ['test-1', 'test-4', 'test-5', 'test-8'], 'b': ['test-2', 'test-6'], 'c': ['test-3', 'test-3', 'test-7'], 'd': ['test-9'], 'e': ['test-10']})
        '''
        if not multivalued_dict.__is_multivalued_dict__(self):
            raise TypeError(f"descriptor 'update' requires a 'multivalued_dict' object but received a {type(self)}")
        len_of_args = len(args)
        if len_of_args > 1:
            raise TypeError(f'expected at most 1 arguments, got {len_of_args}')
        if len_of_args == 1:
            update_items = args[0]
            if not isinstance(update_items, Iterable):
                raise TypeError(f'{type(update_items)} object is not iterable ')
            if multivalued_dict.__is_multivalued_dict__(update_items):
                for _key, _value in update_items.items():
                    self.data[_key].extend(_value)
            elif isinstance(update_items, dict):
                for _key, _value in update_items.items():
                    self.data[_key].append(_value)
            else:
                for item in update_items:
                    if len(item) != 2:
                        raise KeyValuePairsError(item)
                    _key, _value = item
                    self.data[_key].append(_value)
        if kwargs != dict():
            self.update(kwargs)
    
    def reverse(self, key):
        '''
            
        '''
        self.data[key].reverse()
    
    def copy(self):
        '''
            
        '''
        return multivalued_dict(self.data)
    
    def items(self):
        '''
            
        '''
        return self.data.items()
    
    def keys(self):
        '''
            
        '''
        return self.data.keys()
    
    def values(self):
        '''
            
        '''
        return self.data.values()

    @classmethod
    def fromkeys(cls, iterable, value = None):
        '''
            >>> multivalued_dict.fromkeys(['a', 'b', 'c'])
            multivalued_dict({'a': [None], 'b': [None], 'c': [None]})
            >>> multivalued_dict.fromkeys(['a', 'b', 'c'], 'test')
            multivalued_dict({'a': ['test'], 'b': ['test'], 'c': ['test']})
        '''
        dict_var = dict.fromkeys(iterable, value)
        return cls(dict_var)
