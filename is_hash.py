def is_hash(x) -> bool:
    '''
    用法：在用的程序里先导入
    from is_hash import is_hash
    需要测试对象是否可散列就用is_hash(被测试对象)
    '''
    try:
        hash(x)
        return True
    except TypeError:
        return False