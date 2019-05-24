def get_file_contents(fpath):
    f = open(fpath, 'r')
    try:
        res = f.read()
    except:
        raise
    finally:
        f.close()
    return res