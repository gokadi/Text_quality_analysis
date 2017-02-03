def vodnost(stop_word,total_word):
    value=stop_word/total_word
    return value

def commas(grammas,total_word):
    value=grammas/total_word
    return value

def orfo(orf_err,total_word):
    value=orf_err/total_word
    return value

def tonalcy(tonal_com,tonal_words,total_word):
    value=(tonal_words+tonal_com)/total_word
    return value

def reklamnost(total_word):
    value=0
    return value

def informativnost(total_word):
    value=0
    return value