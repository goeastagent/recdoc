from elasticsearch import Elasticsearch
import pandas as pd
import os 

class TrecIndexing:
    def __init__(self):
        self.es = Elasticsearch([{'host':'localhost','port':9200}])
        
    def getDocument(self,pmcid):
        res = self.coll.find({"articleMeta.pmcid" : str(pmcid)}).next()

        meta = res['articleMeta']
        content = res['articleContent']


        # title
        title = meta['title']
        # abstract
        abstract = ""
        if 'sectionList' in meta['abstractText']:
            for entry in meta['abstractText']['sectionList']:
                if 'paragraphs' in entry:
                    abstract = abstract + '\n' + entry['paragraphs']

        # body
        body = ""
        for entry in content['sectionList']:
            if 'paragraphs' in entry:
                body = body + '\n' + entry['paragraphs']
        
        return (title,abstract,body)
        

    def doIndex(self):
        for d in os.listdir('data'):
            cnt = os.listdir('data/'+d)
            i = 0
            for f in os.listdir('data/'+d):
                document = open('data/'+d+'/'+f).read()
                pmcid = f.split('.')[0]
                docin = {'pmcid':pmcid,
                         'document' : document
                }

                res = self.es.index(index='bm25',doc_type='article',id=pmcid,body=docin)
                print res['created'],i,'/',cnt
                i += 1
            break
            
t = TrecIndexing()
t.doIndex()
