def decode_integer(text, i=0):
    e = text.index('e', 1)
    if text[1] == '-' and text[2] == '0':
        raise ValueError
    return int(text[1:e]), i+e+1

def decode_string(text, i=0):
    c = text.index(':', 1)
    l = int(text[:c])
    if l < 0:
        raise ValueError
    return text[c+1:c+l+1], i+c+l+1

def decode_list(text, i=0):
    l = []
    
    while text[i] != 'e':
        v, i = decode_item(text, i)
        l.append(v)
        
    return l, i

def decode_dict(text, i=0):
    d = {}
    
    while text[i] != 'e':
        k, i = decode_string(text[i:], i)
        v, i = decode_item(text, i)
        d[k] = v
        
    return d, i

def decode_item(text, i=0):
    try:
        if text[i].isdigit():
            r, i = decode_string(text[i:], i)
        elif text[i] == 'i':
            r, i = decode_integer(text[i:], i)
        elif text[i] == 'l':
            r, i = decode_list(text, i+1)
        elif text[i] == 'd':
            r, i = decode_dict(text, i+1)
    except:
        raise TypeError("Not a valid bencoded string.")
    
    return r, i

def decode(text, i=0):
    
    data, i = decode_item(text)
    return data

if __name__ == '__main__':
    from urllib2 import urlopen
    data = urlopen('http://update.utorrent.com/installoffer.php?offer=conduit').read()

    d = decode(data)
    print d
    