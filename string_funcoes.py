#********************************************************************************#    
def padl(s, width, fillchar=' '):
    if len(s) >= width:
        return s
    else:
        padding = fillchar * (width - len(s))
        return padding + s
    
#********************************************************************************#    
def padr(s, width, fillchar=' '):
    if len(s) >= width:
        return s
    else:
        padding = fillchar * (width - len(s))
        return s + padding

#********************************************************************************#    
def replicate(value, times):
    return value * times
    
#********************************************************************************#    
def unserscore_invertido():
    underbar_invertido = "\u203E"
    print(underbar_invertido)