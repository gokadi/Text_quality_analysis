import re
from os import read

import numpy

input = open('train_texts/seo.txt','r')
seo_texts = input.readlines()
output = open('train_texts/seo_prepared.txt','w')
seo_text_prep = numpy.array(seo_texts)
for i in range(len(seo_text_prep)):
    seo_text_prep[i] = re.sub("[\n]", "", seo_text_prep[i])
    seo_text_prep[i] = re.split("Domain", seo_text_prep[i])[1]
    seo_text_prep[i] = re.split("saving", seo_text_prep[i])[0]
    seo_text_prep[i] = re.sub(" ", "", seo_text_prep[i])
    output.write(seo_text_prep[i]+"\n")
output.close()