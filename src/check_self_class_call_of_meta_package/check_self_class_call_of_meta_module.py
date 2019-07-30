'''
check_self_class_call_of_meta - This is the metaclass that adds the check self method when the class name is called.
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

from inspect import isfunction
from functools import wraps

__all__ = ['check_self_class_call_of_meta']

class check_self_class_call_of_meta(type):
    '''Check the class name pattern of the class instance method called the self.'''
    @staticmethod
    def __class_function_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            first_arg = args[0]
            class_of_first_arg = type(first_arg)
            func_of_module = func.__module__
            func_of_class = func.__qualname__.rpartition('.')[0]
            exec('from '+func_of_module+' import '+func_of_class)
            original_class = eval(func_of_class)
            if issubclass(class_of_first_arg, original_class):
                return func(*args, **kwargs)
            else:
                raise TypeError(f"descriptor '{func.__name__}' requires a '{original_class.__name__}' object but received a '{class_of_first_arg.__name__}'")
        return wrapper
    
    def __new__(cls, name, bases, namespace, **kwargs):
        for key, value in namespace.items():
            if isfunction(value):
                namespace.__setitem__(key, cls.__class_function_wrapper(value))
        return type.__new__(cls, name, bases, namespace)
    
    def __call__(self, *args, **kwargs):
        self.__instance = super().__call__(*args, **kwargs)
        return self.__instance
