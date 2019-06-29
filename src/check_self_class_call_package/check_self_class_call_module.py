'''
check_self_class_call - This is a package of self when the validation class is called.
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

import inspect

class check_self_class_call(object):
    '''Check the class name pattern of the class instance method called the self.'''
    def __init__(self, original_class):
        self.__original_class = original_class
    def __call__(self, *args, **kwargs):
        return self.__original_class(*args, **kwargs)
    def __getattribute__(self, name):
        if name == '_check_self_class_call__original_class':
            return object.__getattribute__(self, '_check_self_class_call__original_class')
        elif name == '_check_self_class_call__class_function_wrapper':
            return object.__getattribute__(self, '_check_self_class_call__class_function_wrapper')
        else:
            original_class = object.__getattribute__(self, '_check_self_class_call__original_class')
            original_class_attribute = getattr(original_class, name)
            if inspect.isfunction(original_class_attribute):
                return self.__class_function_wrapper(original_class_attribute)
            else:
                return original_class_attribute
    def __class_function_wrapper(self, func):
        def is_self(original_class, first_arg):
            if isinstance(first_arg, original_class):
                return True
            else:
                return False
        def wrapper(*args, **kwargs):
            original_class = self.__original_class
            first_arg = args[0]
            if is_self(original_class, first_arg):
                return func(*args, **kwargs)
            else:
                raise TypeError(f"descriptor '{func.__name__}' requires a '{original_class.__name__}' object but received a '{first_arg.__class__.__name__}'")
        return wrapper
