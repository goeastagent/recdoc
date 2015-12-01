from elasticsearch import Elasticsearch


import pandas as pd
from os import listdir

class ElasticIndexing:
    def __init__(self):
        self.es = Elasticsearch([{'host':'localhost','port':9200}])

    def doIndex(self,directory='data'):
        cnt = 0
        
        for d in os.listdir(directory): # data directory
            for f in d:                 # 0,1,2 directories
                doc = pd.read_csv(f,sep='\n',columns=['title','abstract','body'])
                docin = {'title' : doc['title'],
                         'pmcid' : pmcid,
                         'document' : doc['document']
                }
                
                res = self.es.index(index='recdoc',doc_type="article",id=pmcid,body=docin)
                print res['created']
        
