def check(x: str, file: str):
    book = {}
    list_strs = x.split()
    f=open(file, 'w')
    for s in list_strs:
        s = s.lower()
        if s in book:
            book[s] += 1
        else:
            book[s] = 1
    for s in sorted(book.keys()):
        print(s, book[s], file=f)
