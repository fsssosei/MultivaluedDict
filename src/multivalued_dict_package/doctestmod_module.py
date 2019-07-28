__all__ = ['doctestmod']

def doctestmod():
    from doctest import testmod
    from multivalued_dict_package import multivalued_dict_module
    testmod(multivalued_dict_module)
