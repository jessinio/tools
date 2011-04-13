def rreadlines(f, lines, remain=''):
    '''从文件后面读取指定行数的数据
    '''
    retval = ''
    while True:
        current = f.tell()
        # 向前的数据已经不够
        if current < 1024:
            if current == 0:
                retval = retval + remain
            else:
                f.seek(-current, 1)
                data = f.read(current)
                retval = data + remain
                f.seek(-current, 1)
        else:
            f.seek(-1024, 1)
            data = f.read(1024)
            if remain:
                retval = data + remain
                remain = ''
            else:
                retval = data + retval
            f.seek(-1024, 1)
        # 是否取得足够的行数, 或者已经读到文件开头
        if retval.count("\n") >= lines or current == 0:
            l = retval.split("\n")
            return l[-lines:], "\n".join(l[:-lines])
