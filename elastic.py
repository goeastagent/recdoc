from elasticsearch import Elasticsearch


import pandas as pd
from os import listdir

class ElasticIndexing:
    def __init__(self):
        self.es = Elasticsearch([{'host':'localhost','port':9200}])

    def doIndex(self,directory):
        cnt = 0
        
        for f in os.listdir(directory):
            doc = pd.read_csv(f,sep='\n',columns=['title','abstract','body'])
            
            docin = {'title' : doc['title'],
                     'pmcid' : pmcid,
                     'document' : doc['document']
                     }
            
            res = self.es.index(index='recdoc',doc_type="article",id=pmcid,body=docin)
            print res['created'],str(i) + "/" + str(cnt)
        
