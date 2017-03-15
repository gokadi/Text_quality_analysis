'''from all import inp_dict as dc
from all import criteria as cr

orf_err,total_words,tonal,stop_word,tonal_words,total_errs=dc.make_dict()
gramm=total_errs-orf_err
# Вывод общей информации о тексте
print("Слов с ошибками: ",orf_err)
print("Грамматических ошибок в тексте: ",total_errs-orf_err)
print("Знаков препинания, связанных с тональностью: ",tonal)
print("Стоп-слов: ",stop_word)
print("Тональных слов: ",tonal_words)
print("Всего слов: ",total_words)
print("Значения критериев:")
# Критерии. Формирование
vodnost=cr.vodnost(stop_word,total_words)
grammatic=cr.commas(gramm,total_words)
orph=cr.orfo(orf_err,total_words)
ton=cr.tonalcy(tonal,tonal_words,total_words)
# Критерии. Вывод
print("Водность текста: ",vodnost)
print("Грамматические ошибки: ",grammatic)
print("Орфографические ошибки: ",orph)
print("Тональность: ",ton)
'''