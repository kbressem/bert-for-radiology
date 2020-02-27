import spacy
from spacy.lang.de import German
import pandas as pd
import time

nlp = German()
nlp.add_pipe(nlp.create_pipe('sentencizer')) 

texts = pd.read_csv('../data/cleaned-text-dump.csv', low_memory=False) 

def sentencizer(raw_text, nlp):
    doc = nlp(raw_text)
    sentences = [sent.string.strip() for sent in doc.sents]
    return(sentences)

def fix_wrong_splits(sentences): 
    i=0
    
    while i < (len(sentences)-2): 
        if sentences[i].endswith(('Z.n.','V.a.','v.a.', 'Vd.a.' 'i.v', ' re.', 
                                  ' li.', 'und 4.', 'bds.', 'Bds.', 'Pat.', 
                                  'i.p.', 'i.P.', 'b.w.', 'i.e.L.', ' pect.', 
                                  'Ggfs.', 'ggf.', 'Ggf.',  'z.B.', 'a.e.'
                                  'I.', 'II.', 'III.', 'IV.', 'V.', 'VI.', 'VII.', 
                                  'VIII.', 'IX.', 'X.', 'XI.', 'XII.')):
            sentences[i:i+2] = [' '.join(sentences[i:i+2])]

        elif len(sentences[i]) < 10: 
            sentences[i:i+2] = [' '.join(sentences[i:i+2])]

        i+=1
    return(sentences)
    
loggingstep = []
for i in range(1000): 
    loggingstep.append(i*10000)
    
    
tic = time.clock()
for i in range(len(texts)):
    text = texts.TEXT[i]
    sentences = sentencizer(text, nlp)
    sentences = fix_wrong_splits(sentences)
    with open('../data/report-dump.txt', 'a+') as file:
        for sent in sentences:
            file.write(sent + '\n')
        file.write('\n')   
    if i in loggingstep:
        toc = time.clock()
        print('dumped the ' + str(i) + "th report. " + str(toc - tic) + "seconds passed.")
toc = time.clock()
