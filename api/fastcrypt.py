alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/="

import base64, os

def encrypt(string, encryption_key):
    encoded = base64.b64encode(string.encode("utf-8"))
    
    encoded = str(encoded, "utf-8")
    newstr = ""
    index = 0
    for c in encoded:
        ci = alphabet.index(c)
        ki = alphabet.index(encryption_key[index])
        new = (ci + ki) % len(alphabet)
        newstr = newstr + alphabet[new]
        index = (index + 1) % len(encryption_key)
    return newstr

def decrypt(encoded, encryption_key):
    index = 0
    newstr = ""
    for c in encoded:
        ci = alphabet.index(c)
        ki = alphabet.index(encryption_key[index])
        new = ci - ki
        newstr = newstr + alphabet[new]
        index = (index + 1) % len(encryption_key)
    try:
        return str(base64.b64decode(newstr.encode("utf-8")), "utf-8")
    except:
        return None
    