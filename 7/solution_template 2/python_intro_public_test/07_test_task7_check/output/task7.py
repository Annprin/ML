def find_modified_max_argmax(L, f):
    L = [f(i) for i in L if type(i) is int]
    return (max(L), L.index(max(L))) if L else ()