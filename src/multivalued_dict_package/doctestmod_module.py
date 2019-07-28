from doctest import testmod

__all__ = ['doctestmod']

def doctestmod():
    from multivalued_dict_package import multivalued_dict_module
    testmod(multivalued_dict_module)
