import os
from gensim import utils
from simserver import SessionServer

def buildCorpus():
    
    corpus = []
    for d in os.listdir('data'):
        if not d == '0':
            continue
        cnt = os.listdir('data/'+d)
        i = 0
        for f in os.listdir('data/'+d):
            document = open('data/'+d+'/'+f).read()
            pmcid = f.split('.')[0]
            docin = {'id' : pmcid,
                     'tokens' : utils.simple_preprocess(document)
            }
            corpus.append(docin)
    return corpus

corpus = buildCorpus()

server = SessionServer('myserver')

#server.train(corpus,method='lsi')
server.index(corpus)
