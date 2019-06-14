from collections import defaultdict
from collections import UserDict
from collections.abc import Iterable
import inspect

START_POS = 'S'
END_POS = 'E'
    
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
        
        >>> multivalued_dict([['a', 'test-1']], [['b', 'test-2']])
        Traceback (most recent call last):
        TypeError: multivalued_dict expected at most 1 arguments, got 2
    '''
    
    __marker = object()
    
    @staticmethod
    def __is_self(v_self):
        if not multivalued_dict.__is_multivalued_dict__(v_self):
            raise TypeError(f"descriptor '{inspect.currentframe().f_back.f_code.co_name}' requires a 'multivalued_dict' object but received a '{v_self.__class__.__name__}'")
    
    @classmethod
    def __is_multivalued_dict__(cls, x):
        '''
            >>> mv_d = multivalued_dict()
            >>> multivalued_dict.__is_multivalued_dict__(mv_d)
            True
        '''
        return (isinstance(x, cls) or ((True if x.default_factory == type([]) else False) if isinstance(x, defaultdict) else False))
    
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
            
            >>> mv_d.__init__({'a': 'test-6'})
            >>> mv_d
            multivalued_dict({'a': ['test-1', 'test-6'], 'b': ['test-2'], 'c': ['test-3'], 'd': ['test-4'], 'e': ['test-5']})
            
            >>> multivalued_dict.__init__('x')
            Traceback (most recent call last):
            TypeError: descriptor '__init__' requires a 'multivalued_dict' object but received a 'str'
        '''
        multivalued_dict.__is_self(self)
        len_of_args = len(args)
        if len_of_args > 1:
            raise TypeError(f'multivalued_dict expected at most 1 arguments, got {len_of_args}')
        else:
            if not hasattr(self, 'data'):
                self.data = defaultdict(list)
            if len_of_args == 1:
                initial_items = args[0]
                self.update(initial_items)
        if kwargs != dict():
            self.update(kwargs)
    
    def __repr__(self):
        multivalued_dict.__is_self(self)
        return f'multivalued_dict({dict(self.data)})'
    
    def __iter__(self):
        multivalued_dict.__is_self(self)
        return self.data.__iter__()
    
    def __len__(self):
        '''
            >>> mv_d = multivalued_dict([['a', 'test-1'], ['a', 'test-2'], ['a', 'test-3'], ['b', 'test-4']])
            >>> mv_d.__len__()
            2
        '''
        multivalued_dict.__is_self(self)
        return self.data.__len__()
    
    def __lenvalue__(self, key = __marker):
        '''
            >>> mv_d = multivalued_dict([['a', 1], ['a', 2], ['a', 3], ['b', 1], ['b', 2], ['c', 1]])
            >>> mv_d.__lenvalue__()
            6
            >>> mv_d.__lenvalue__('a')
            3
        '''
        multivalued_dict.__is_self(self)
        if key is self.__marker:
            return sum(map(len, self.data.values()))
        else:
            return len(self.data[key])
    
    def __getitem__(self, key):
        '''
            >>> mv_d = multivalued_dict({'a': 'test-1', 'b': 'test-2', 'c': 'test-3'})
            >>> mv_d['a']
            ['test-1']
            
            >>> mv_d['d']
            Traceback (most recent call last):
            KeyError: 'd'
        '''
        multivalued_dict.__is_self(self)
        if key in self.data:
            return self.data[key]
        else:
            raise KeyError(key)
    
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
        multivalued_dict.__is_self(self)
        return value in self.data[key]
    
    def __eq__(self, other):
        '''
            >>> mv_d = multivalued_dict({'a': 'test-1', 'b': 'test-2', 'c': 'test-3'})
            >>> mv_d
            multivalued_dict({'a': ['test-1'], 'b': ['test-2'], 'c': ['test-3']})
            >>> mv_d == {'a': ['test-1'], 'b': ['test-2'], 'c': ['test-3']}
            True
            >>> mv_d == {'a': ['test-1'], 'b': ['test-2'], 'c': ['test-0']}
            False
        '''
        multivalued_dict.__is_self(self)
        return self.data.__eq__(other)
    
    def __contains__(self, key):
        '''
            >>> mv_d = multivalued_dict({'a': 'test-1', 'b': 'test-2', 'c': 'test-3'})
            >>> mv_d
            multivalued_dict({'a': ['test-1'], 'b': ['test-2'], 'c': ['test-3']})
            >>> 'a' in mv_d
            True
            >>> 'd' in mv_d
            False
        '''
        multivalued_dict.__is_self(self)
        return self.data.__contains__(key)
    
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
        multivalued_dict.__is_self(self)
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
    
    def __delitem__(self, key):
        '''
            >>> mv_d = multivalued_dict({'a': 'test-1', 'b': 'test-2', 'c': 'test-3'})
            >>> mv_d.__delitem__('b')
            >>> mv_d
            multivalued_dict({'a': ['test-1'], 'c': ['test-3']})
        '''
        multivalued_dict.__is_self(self)
        self.data.__delitem__(key)
        
    def __setitem__(self, key, item):
        '''
            >>> mv_d = multivalued_dict([['a', 'test-1'], ['a', 'test-2'], ['a', 'test-3'], ['b', 'test-4']])
            >>> mv_d
            multivalued_dict({'a': ['test-1', 'test-2', 'test-3'], 'b': ['test-4']})
            
            >>> mv_d.__setitem__('c', 'test-5')
            >>> mv_d
            multivalued_dict({'a': ['test-1', 'test-2', 'test-3'], 'b': ['test-4'], 'c': ['test-5']})
            
            >>> mv_d.__setitem__('a', 'test-0')
            >>> mv_d
            multivalued_dict({'a': ['test-0'], 'b': ['test-4'], 'c': ['test-5']})
        '''
        multivalued_dict.__is_self(self)
        self.data.__setitem__(key, [item])
    
    def get(self, key, default = None):
        '''
            >>> mv_d = multivalued_dict({'a': 'test-1', 'b': 'test-2', 'c': 'test-3'})
            >>> mv_d.get('a')
            ['test-1']
            >>> mv_d.get('d')
            [None]
        '''
        multivalued_dict.__is_self(self)
        return self.data.get(key, [default])
    
    def count(self, key, value):
        '''
            >>> mv_d = multivalued_dict([['a', 'x'], ['a', 'y'], ['a', 'y'], ['a', 'z'], ['a', 'z'], ['a', 'z']])
            >>> mv_d.count('a', 'y')
            2
        '''
        multivalued_dict.__is_self(self)
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

            >>> mv_d.update([['a', 'test-1']], [['b', 'test-2']])
            Traceback (most recent call last):
            TypeError: multivalued_dict expected at most 1 arguments, got 2

            >>> mv_d.update(1)
            Traceback (most recent call last):
            TypeError: 'int' object is not iterable
            
            >>> mv_d.update([1])
            Traceback (most recent call last):
            TypeError: cannot convert dictionary update sequence element #0 to a sequence
            
            >>> mv_d.update([['1', '2', '3']])
            Traceback (most recent call last):
            ValueError: dictionary update sequence element #0 has length 3; 2 is required
            
            >>> multivalued_dict.update('x')
            Traceback (most recent call last):
            TypeError: descriptor 'update' requires a 'multivalued_dict' object but received a 'str'
        '''
        multivalued_dict.__is_self(self)
        len_of_args = len(args)
        if len_of_args > 1:
            raise TypeError(f'multivalued_dict expected at most 1 arguments, got {len_of_args}')
        if len_of_args == 1:
            update_items = args[0]
            if not isinstance(update_items, Iterable):
                raise TypeError(f"'{update_items.__class__.__name__}' object is not iterable")
            if multivalued_dict.__is_multivalued_dict__(update_items):
                for _key, _value in update_items.items():
                    self.data[_key].extend(_value)
            elif isinstance(update_items, dict):
                for _key, _value in update_items.items():
                    self.data[_key].append(_value)
            else:
                i = 0
                for item in update_items:
                    if not isinstance(item, Iterable):
                        raise TypeError(f'cannot convert dictionary update sequence element #{i} to a sequence')
                    if len(item) != 2:
                        raise ValueError(f'dictionary update sequence element #{i} has length {len(item)}; 2 is required')
                    _key, _value = item
                    self.data[_key].append(_value)
                    i += 1
        if kwargs != dict():
            self.update(kwargs)
    
    def setdefault(self, key, default = None):
        '''
            >>> mv_d = multivalued_dict({'a': 'test-1', 'c': 'test-3'})
            >>> mv_d.setdefault('a')
            ['test-1']
            >>> mv_d.setdefault('b')
            [None]
            >>> mv_d
            multivalued_dict({'a': ['test-1'], 'c': ['test-3'], 'b': [None]})
            >>> mv_d.setdefault('d', 'test=4')
            ['test=4']
            >>> mv_d
            multivalued_dict({'a': ['test-1'], 'c': ['test-3'], 'b': [None], 'd': ['test=4']})
        '''
        multivalued_dict.__is_self(self)
        return self.data.setdefault(key, [default])
        
    def pop(self, key, default=__marker):
        '''
            
        '''
        multivalued_dict.__is_self(self)
        if default is self.__marker:
            return self.data.pop(key)
        else:
            return self.data.pop(key, [default])
    
    def popitem(self):
        '''
            >>> mv_d = multivalued_dict({'a': 'test-1', 'b': 'test-2', 'c': 'test-3'})
            >>> mv_d
            multivalued_dict({'a': ['test-1'], 'b': ['test-2'], 'c': ['test-3']})
            >>> mv_d.popitem()
            ('c', ['test-3'])
        '''
        multivalued_dict.__is_self(self)
        return self.data.popitem()
    
    def copy(self):
        '''
            >>> mv_d_a = multivalued_dict([['a', 1], ['a', 2], ['a', 3]])
            >>> mv_d_b = mv_d_a.copy()
            >>> mv_d_a
            multivalued_dict({'a': [1, 2, 3]})
            >>> mv_d_b
            multivalued_dict({'a': [1, 2, 3]})
            >>> mv_d_a['a'][1] = 99
            >>> mv_d_a
            multivalued_dict({'a': [1, 99, 3]})
            >>> mv_d_b
            multivalued_dict({'a': [1, 2, 3]})
        '''
        multivalued_dict.__is_self(self)
        return multivalued_dict(self.data)
    
    def items(self):
        '''
            >>> mv_d = multivalued_dict({'a': 'test-1', 'b': 'test-2', 'c': 'test-3'})
            >>> for k, v in mv_d.items():
            ...     print(f'key = {k}, value = {v}')
            ...
            key = a, value = ['test-1']
            key = b, value = ['test-2']
            key = c, value = ['test-3']
        '''
        multivalued_dict.__is_self(self)
        return self.data.items()
    
    def keys(self):
        '''
            >>> mv_d = multivalued_dict({'a': 'test-1', 'b': 'test-2', 'c': 'test-3'})
            >>> for k in mv_d.keys():
            ...     print(f'key = {k}')
            ...
            key = a
            key = b
            key = c
        '''
        multivalued_dict.__is_self(self)
        return self.data.keys()
    
    def values(self):
        '''
            >>> mv_d = multivalued_dict({'a': 'test-1', 'b': 'test-2', 'c': 'test-3'})
            >>> for v in mv_d.values():
            ...     print(f'value = {v}')
            ...
            value = ['test-1']
            value = ['test-2']
            value = ['test-3']
        '''
        multivalued_dict.__is_self(self)
        return self.data.values()
    
    def clear(self):
        '''
            >>> mv_d = multivalued_dict({'a': 'test-1', 'b': 'test-2', 'c': 'test-3'})
            >>> mv_d
            multivalued_dict({'a': ['test-1'], 'b': ['test-2'], 'c': ['test-3']})
            >>> mv_d.clear()
            >>> mv_d
            multivalued_dict({})
        '''
        multivalued_dict.__is_self(self)
        self.data.clear()
    
    def reverse(self, key):
        '''
            >>> mv_d = multivalued_dict([['a', 1], ['a', 2], ['a', 3]])
            >>> mv_d
            multivalued_dict({'a': [1, 2, 3]})
            >>> mv_d.reverse('a')
            >>> mv_d
            multivalued_dict({'a': [3, 2, 1]})
        '''
        multivalued_dict.__is_self(self)
        self.data[key].reverse()
