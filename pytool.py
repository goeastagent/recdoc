import pandas as pd
import numpy as np


# This function generates 2 files for data of test and training.
def cross_validation(filename):
    question = 0
    pmcid = 2
    relevancy = 3

    new_filename1='cross_validation_train_'+filename
    new_filename2='cross_validation_test_'+filename

    training = pd.DataFrame()
    test = pd.DataFrame()

    data = pd.read_csv(filename,sep='\t',header=None)
    for i in range(1,31):
        p = data[data[question] == i]
        total = len(p)
        sol_cnt = len(data[(data[question] == i) & (data[relevancy] == 0)])
        print total,sol_cnt
        cnt_not = sol_cnt*8/10
        cnt_rel = (total-sol_cnt)*8/10

        for index,j in p.iterrows():
            elm = {'question':[j[question]],'pmcid':[j[pmcid]],'relevancy':[j[relevancy]]}
            if j[relevancy] == 0:
                if not (cnt_not == 0):
                    cnt_not -= 1
                    training = training.append(pd.DataFrame(elm))
                else:
                    test = test.append(pd.DataFrame(elm))
            else:
                if not (cnt_rel == 0):
                    cnt_rel -= 1
                    training = training.append(pd.DataFrame(elm))
                else:
                    test = test.append(pd.DataFrame(elm))

        
    training.to_csv('training.csv',sep='\t')
    test.to_csv('test.csv',sep='\t')



class SimilarityCalculator:
    def __init__(self,alpha=1,beta=0):
        self.alpha = alpha
        self.beta = beta

    
    # This function is static function
    # returnining two number of map data structure.
    # One is to access cluster information by pmcid,
    # and the other is to access pmcid by cluster.
    def build_map(filename):
        clusterToId = {}
        idToCluster = {}

        data = pd.read_csv(filename,sep='\t')
    
        for index,elm in data.iterrows():
            if elm['relevancy'] == 2 or elm['relevancy'] == 1:
                if not elm['question'] in clusterToId: 
                clusterToId[elm['question']] = []
            clusterToId[elm['question']].append(elm['pmcid'])

            if not elm['pmcid'] in idToCluster:
                idToCluster[elm['pmcid']] = []
                idToCluster[elm['pmcid']].append(elm['question'])
            else:
                idToCluster[elm['pmcid']].append(elm['question'])

        return (clusterToId,idToCluster)


    # This function provides the method to calculate similarity between two different documents.
    # TF-IDF, IB, LMD, and so on will be used in calculating document similarity.
    # return the cosine score.
    def get_document_document_similarity(self,pmcid1,pmcid2):
        pass

    # This function provides the method to calculate similarity between document1 and clique
    # that contains document2
    def get_document_clique_similarity(self,pmcid1,pmcid2):
        pass

    # Return the score calculated by cosine similarity between doc1 and doc2
    # The score is calculated by summing up the two functions, get_document_document_similarity
    # and get_document_clique_similarity giving weights alpha and beta. 
    def get_document_similarity(self,doc1,doc2):
        return self.get_document_similarity(doc1,doc2)*alpha + self.get_document_clique_similarity(doc1,doc2)*beta
