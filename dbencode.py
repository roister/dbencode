def decode_integer(text, i=0):
    e = text.index('e', 1)
    return int(text[1:e]), i+e+1

def decode_string(text, i=0):
    c = text.index(':', 1)
    l = int(text[:c])
    return text[c+1:c+l+1], i+c+l+1

def decode_list(text, i=0):
    items, i = decode_item(text, i)
    
    if items[-1] != 'e':
        raise TypeError
    items = items[:-1]
    
    return items, i+1

def decode_dict(text, i=0):
    j, d = 0, {}
    items, i = decode_item(text, i)
    
    if items[-1] != 'e':
        raise TypeError
    items = items[:-1]
    
    while j < len(items):
        d[items[j]] = items[j+1]
        j += 2
        
    return d, i+1

def decode_item(text, i=0):
    try:
        if text[i] == 'i':
            r, j = decode_integer(text[i:], i)
        elif text[i] == 'l':
            r, j = decode(text[i+1:], i, True)
            j += i
        elif text[i] == 'd':
            r, j = decode(text[i+1:], i, True)
            j += i
        elif text[i].isdigit():
            r, j = decode_string(text[i:], i)
    except:
        raise TypeError("Not a valid bencoded string.")
    
    return r, j

def decode(text, i=0, recurring=False):
    j, data = 0, []
    
    while j < len(text):
        if text[j] == 'l':
            r, j = decode_list(text, j)
        elif text[j] == 'd':
            r, j = decode_dict(text, j)
        elif text[j] == 'e':    # used to stop dicts and lists
            data.append('e')
            j += 1
            break
        else:
            r, j = decode_item(text, j)
            
        data.append(r)
    
    if recurring: 
        return data, j
    
    if len(data) > 1:
        raise TypeError('Invalid data present at end of bencoded string.')
    return data[0] 
    