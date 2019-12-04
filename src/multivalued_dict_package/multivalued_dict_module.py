'''
multivalued_dict - This is a multi-valued dictionary package.
Copyright (C) 2019  sosei

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from check_self_class_call_of_meta_package import check_self_class_call_of_meta
from abc import ABCMeta
from collections import UserDict

__all__ = ['multivalued_dict', 'START_POS', 'END_POS']

START_POS = 'S'
END_POS = 'E'

class __eliminate_metaclass_conflicts(check_self_class_call_of_meta, ABCMeta):
    pass

class multivalued_dict(UserDict, metaclass = __eliminate_metaclass_conflicts):  #lgtm [py/missing-call-to-init]
    '''
        multivalued_dict() -> new empty dictionary
        multivalued_dict(mapping) -> new dictionary initialized from a mapping object's
            (key, value) pairs
        multivalued_dict(iterable) -> new dictionary initialized as if via:
            d = {}
            for k, v in iterable:
                d[k].append(v)
        multivalued_dict(**kwargs) -> new dictionary initialized with the name=value pairs
            in the keyword argument list.  For example:  dict(one=1, two=2)
        
        >>> mv_d = multivalued_dict()
        >>> mv_d
        multivalued_dict({})
        
        >>> mv_d = multivalued_dict({'a': 'test-1', 'b': 'test-2', 'c': 'test-3'})
        >>> mv_d
        multivalued_dict({'a': ['test-1'], 'b': ['test-2'], 'c': ['test-3']})
        
        >>> mv_d = multivalued_dict({'a': ['test-1', 'test-2', 'test-3'], 'b': 'test-4'})
        >>> mv_d
        multivalued_dict({'a': ['test-1', 'test-2', 'test-3'], 'b': ['test-4']})
        
        >>> mv_d = multivalued_dict([['a', 'test-1'], ['b', 'test-2'], ['a', 'test-3']])
        >>> mv_d
        multivalued_dict({'a': ['test-1', 'test-3'], 'b': ['test-2']})
        
        >>> mv_d = multivalued_dict(a = 'test-1', b = 'test-2', c = 'test-3')
        >>> mv_d
        multivalued_dict({'a': ['test-1'], 'b': ['test-2'], 'c': ['test-3']})
        
        >>> mv_d = multivalued_dict(a = ['test-1', 'test-2', 'test-3'])
        >>> mv_d
        multivalued_dict({'a': ['test-1', 'test-2', 'test-3']})
        
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
    
    from collections import defaultdict
    from collections.abc import Iterable
    
    version = '1.7.3'
    
    __marker = object()
    
    @classmethod
    def __is_multivalued_dict__(cls, x):
        '''
            >>> mv_d = multivalued_dict()
            >>> multivalued_dict.__is_multivalued_dict__(mv_d)
            True
        '''
        
        return (isinstance(x, cls) or ((True if x.default_factory == type([]) else False) if isinstance(x, cls.defaultdict) else False))
    
    @classmethod
    def fromkeys(cls, iterable, value = None):
        '''
            Create a new dictionary with keys from iterable and values set to value.
            
            >>> multivalued_dict.fromkeys(['a', 'b', 'c'])
            multivalued_dict({'a': [None], 'b': [None], 'c': [None]})
            >>> multivalued_dict.fromkeys(['a', 'b', 'c'], 'test')
            multivalued_dict({'a': ['test'], 'b': ['test'], 'c': ['test']})
        '''
        
        dict_var = dict.fromkeys(iterable, value)
        return cls(dict_var)
    
    def __init__(self, *args, **kwargs):
        '''
            Initialize self.  See help(type(self)) for accurate signature.
            
            >>> mv_d = multivalued_dict({'a': 'test-1', 'b': 'test-2', 'c': 'test-3'})
            >>> mv_d
            multivalued_dict({'a': ['test-1'], 'b': ['test-2'], 'c': ['test-3']})
            
            >>> mv_d.__init__({'d': 'test-4'})
            >>> mv_d
            multivalued_dict({'a': ['test-1'], 'b': ['test-2'], 'c': ['test-3'], 'd': ['test-4']})
            
            >>> multivalued_dict.__init__(mv_d, {'e': 'test-5'})
            >>> mv_d
            multivalued_dict({'a': ['test-1'], 'b': ['test-2'], 'c': ['test-3'], 'd': ['test-4'], 'e': ['test-5']})
            
            >>> mv_d.__init__({'a': ['test-6', 'test-7']})
            >>> mv_d
            multivalued_dict({'a': ['test-1', 'test-6', 'test-7'], 'b': ['test-2'], 'c': ['test-3'], 'd': ['test-4'], 'e': ['test-5']})
            
            >>> multivalued_dict.__init__('x')
            Traceback (most recent call last):
            TypeError: descriptor '__init__' requires a 'multivalued_dict' object but received a 'str'
        '''
        
        len_of_args = len(args)
        if len_of_args > 1:
            raise TypeError(f'multivalued_dict expected at most 1 arguments, got {len_of_args}')
        else:
            if not hasattr(self, 'data'):
                self.data = self.defaultdict(list)
            if len_of_args == 1:
                initial_items = args[0]
                if isinstance(initial_items, dict):
                    for _key, _value in initial_items.items():
                        if isinstance(_value, (tuple, list)):
                            self.data[_key].extend(_value)
                        else:
                            self.data[_key].append(_value)
                else:
                    self.update(initial_items)
        if kwargs != dict():
            self.__init__(kwargs)
    
    def __repr__(self):
        '''
            Return repr(self).
        '''
        
        return f'multivalued_dict({dict(self.data)})'
    
    def __iter__(self):
        '''
            Implement iter(self).
            
            >>> multivalued_dict(multivalued_dict({'a': 'test-1'}))
            multivalued_dict({'a': ['test-1']})
            
            >>> mv_d = multivalued_dict({'a': 'test-1', 'b': 'test-2', 'c': 'test-3'})
            >>> multivalued_dict(mv_d.__iter__())
            multivalued_dict({'a': [['test-1']], 'b': [['test-2']], 'c': [['test-3']]})
        '''
        
        return iter(self.data.items())
    
    def __len__(self):
        '''
            Return len(self).
            
            >>> mv_d = multivalued_dict([['a', 'test-1'], ['a', 'test-2'], ['a', 'test-3'], ['b', 'test-4']])
            >>> mv_d.__len__()
            2
        '''
        
        return self.data.__len__()
    
    def __lenvalue__(self, key = __marker):
        '''
            >>> mv_d = multivalued_dict([['a', 1], ['a', 2], ['a', 3], ['b', 1], ['b', 2], ['c', 1]])
            >>> mv_d.__lenvalue__()
            6
            >>> mv_d.__lenvalue__('a')
            3
        '''
        
        if key is self.__marker:
            return sum(map(len, self.data.values()))
        else:
            return len(self.data[key])
    
    def __getitem__(self, key):
        '''
            x.__getitem__(y) <==> x[y]
            
            >>> mv_d = multivalued_dict({'a': 'test-1', 'b': 'test-2', 'c': 'test-3'})
            >>> mv_d['a']
            ['test-1']
            
            >>> mv_d['d']
            Traceback (most recent call last):
            KeyError: 'd'
        '''
        
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
        
        return value in self.data[key]
    
    def __eq__(self, other):
        '''
            Return self==value.
            
            >>> mv_d = multivalued_dict({'a': 'test-1', 'b': 'test-2', 'c': 'test-3'})
            >>> mv_d
            multivalued_dict({'a': ['test-1'], 'b': ['test-2'], 'c': ['test-3']})
            >>> mv_d == {'a': ['test-1'], 'b': ['test-2'], 'c': ['test-3']}
            True
            >>> mv_d == {'a': ['test-1'], 'b': ['test-2'], 'c': ['test-0']}
            False
        '''
        
        return self.data.__eq__(other)
    
    def __contains__(self, key):
        '''
            True if the dictionary has the specified key, else False.
            
            >>> mv_d = multivalued_dict({'a': 'test-1', 'b': 'test-2', 'c': 'test-3'})
            >>> mv_d
            multivalued_dict({'a': ['test-1'], 'b': ['test-2'], 'c': ['test-3']})
            >>> 'a' in mv_d
            True
            >>> 'd' in mv_d
            False
        '''
        
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
            Delete self[key].
            
            >>> mv_d = multivalued_dict({'a': 'test-1', 'b': 'test-2', 'c': 'test-3'})
            >>> mv_d.__delitem__('b')
            >>> mv_d
            multivalued_dict({'a': ['test-1'], 'c': ['test-3']})
        '''
        
        self.data.__delitem__(key)
    
    def __setitem__(self, key, item):
        '''
            Set self[key] to value.
            
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
        
        self.data.__setitem__(key, [item])
    
    def get(self, key, default = None):
        '''
            Return the value for key if key is in the dictionary, else default.
            
            >>> mv_d = multivalued_dict({'a': 'test-1', 'b': 'test-2', 'c': 'test-3'})
            >>> mv_d.get('a')
            ['test-1']
            >>> mv_d.get('d')
            [None]
        '''
        
        return self.data.get(key, [default])
    
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
        
        len_of_args = len(args)
        if len_of_args > 1:
            raise TypeError(f'multivalued_dict expected at most 1 arguments, got {len_of_args}')
        if len_of_args == 1:
            update_items = args[0]
            if not isinstance(update_items, self.Iterable):
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
                    if not isinstance(item, self.Iterable):
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
        
        return self.data.setdefault(key, [default])
    
    def pop(self, key, default=__marker):
        '''
            >>> mv_d = multivalued_dict({'a': 'test-1', 'b': 'test-2', 'c': 'test-3'})
            >>> mv_d.pop('b')
            ['test-2']
            >>> mv_d
            multivalued_dict({'a': ['test-1'], 'c': ['test-3']})
            
            >>> mv_d.pop('d')
            Traceback (most recent call last):
            KeyError: 'd'
            
            >>> mv_d.pop('d', 'test-0')
            ['test-0']
            >>> mv_d
            multivalued_dict({'a': ['test-1'], 'c': ['test-3']})
        '''
        
        if default is self.__marker:
            return self.data.pop(key)
        else:
            return self.data.pop(key, [default])
    
    def popitem(self):
        '''
            D.popitem() -> (k, v), remove and return some (key, value) pair as a 2-tuple; but raise KeyError if D is empty.
            
            >>> mv_d = multivalued_dict({'a': 'test-1', 'b': 'test-2', 'c': 'test-3'})
            >>> mv_d
            multivalued_dict({'a': ['test-1'], 'b': ['test-2'], 'c': ['test-3']})
            >>> mv_d.popitem()
            ('c', ['test-3'])
        '''
        
        return self.data.popitem()
    
    def copy(self):
        '''
            D.copy() -> a shallow copy of D
            
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
        
        return multivalued_dict(self.data)
    
    def items(self):
        '''
            D.items() -> a set-like object providing a view on D's items
            
            >>> mv_d = multivalued_dict({'a': 'test-1', 'b': 'test-2', 'c': 'test-3'})
            >>> for k, v in mv_d.items():
            ...     print(f'key = {k}, value = {v}')
            ...
            key = a, value = ['test-1']
            key = b, value = ['test-2']
            key = c, value = ['test-3']
        '''
        
        return self.data.items()
    
    def keys(self):
        '''
            D.keys() -> a set-like object providing a view on D's keys
            
            >>> mv_d = multivalued_dict({'a': 'test-1', 'b': 'test-2', 'c': 'test-3'})
            >>> for k in mv_d.keys():
            ...     print(f'key = {k}')
            ...
            key = a
            key = b
            key = c
        '''
        
        return self.data.keys()
    
    def values(self):
        '''
            D.values() -> an object providing a view on D's values
            
            >>> mv_d = multivalued_dict({'a': 'test-1', 'b': 'test-2', 'c': 'test-3'})
            >>> for v in mv_d.values():
            ...     print(f'value = {v}')
            ...
            value = ['test-1']
            value = ['test-2']
            value = ['test-3']
        '''
        
        return self.data.values()
    
    def clear(self):
        '''
            D.clear() -> None.  Remove all items from D.
            
            >>> mv_d = multivalued_dict({'a': 'test-1', 'b': 'test-2', 'c': 'test-3'})
            >>> mv_d
            multivalued_dict({'a': ['test-1'], 'b': ['test-2'], 'c': ['test-3']})
            >>> mv_d.clear()
            >>> mv_d
            multivalued_dict({})
        '''
        
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
        
        self.data[key].reverse()
