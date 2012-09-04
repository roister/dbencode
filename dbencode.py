def decode_integer(text,i):
    e = text.index('e', 1)
    return int(text[1:e]), i+e+1

def decode_string(text,i):
    c = text.index(':',1)
    l = int(text[:c])
    return text[c+1:c+l+1], i+c+l+1

def decode_each(text,i=0):
    if text[i] == 'i':
        r,j = decode_integer(text[i:], i)
    elif text[i] == 'l':
        r,j = decode(text[i+1:], i, True)
        j=j+i
    elif text[i] == 'd':
        r,j = decode(text[i+1:], i, True)
        j=j+i
    elif text[i].isdigit():
        r,j = decode_string(text[i:], i)
        
    return r,j

def decode(text, i=0, recursive=False):
    j, data = 0, []
    
    while j+1 < len(text):
        if text[j] == 'l':
            r = []
            while text[j] != 'e':
                list_item,j = decode_each(text, j)
                r += list_item
            j = j+1
        elif text[j] == 'd':
            l, r = 0, {}
            items,j = decode_each(text, j)
            
            while l < len(items):
                r[items[l]] = items[l+1]
                l+=2
                
            j = j+1
        elif text[j] == 'e':    # need this to stop dicts and lists
            j+=1
            break
        else:   # string or int
            r,j = decode_each(text, j)
            
        data.append(r)
    
    if recursive: return data,j
    if len(data) > 1:
        raise ValueError('Data present at end of bencoded string.')
    return data[0] 
