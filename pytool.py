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
    def __init__(self,alpha=1,beta=0,filename='qrels-treceval-2014.txt'):
        self.alpha = alpha
        self.beta = beta
        self.build_map(filename)
        
    # This function is static function
    # returnining two number of map data structure.
    # One is to access cluster information by pmcid,
    # and the other is to access pmcid by cluster.
    def build_map(self,filename):
        self.clusterToId = {}
        self.idToCluster = {}

        data = pd.read_csv(filename,sep='\t')
    
        for index,elm in data.iterrows():
            if elm['relevancy'] == 2 or elm['relevancy'] == 1:
                if not elm['question'] in self.clusterToId: 
                    self.clusterToId[elm['question']] = []
                self.clusterToId[elm['question']].append(elm['pmcid'])
                
                if not elm['pmcid'] in self.idToCluster:
                    self.idToCluster[elm['pmcid']] = []
                self.idToCluster[elm['pmcid']].append(elm['question'])

        return (self.clusterToId,self.idToCluster)


    # This function provides the method to calculate similarity between two different documents.
    # TF-IDF, IB, LMD, and so on will be used in calculating document similarity.
    # return the cosine score.
    def get_document_document_similarity(self,pmcid1,pmcid2):
        pass

    # This function provides the method to calculate similarity between document1 and clique
    # that contains document2
    def get_document_clique_similarity(self,pmcid1,pmcid2):
        pass

    # Obtaining Term Vector of document whose pmcid id is 'pmcid'
    def get_term_vector(self,pmcid):
        pass

    # 
    def merge_terms(self,pmcid):
        cluster = self.idToCluster[pmcid]
        term_vec = []
        
        for c in cluster:
            ids = self.clusterToId[c]
            for pid in ids:
                m = get_term_vector(pid)
            

    # This function calculates document similarity by counting how many nodes
    # they share
    def method1(self,pmcid1,pmcid2):
        cluster1 = self.idToCluster[pmcid1]
        cluster2 = self.idToCluster[pmcid2]

        pmcid_list1 = []
        pmcid_list2 = []

        for clu1 in cluster1:
            l = clusterToId[clu1]
            for j in l:
                if not j in pmcid_list1:
                    pmcid_list1.append(j)
        for clu2 in cluster2:
            l = clusterToId[clu2]
            for j in l:
                if not j in pmcid_list1:
                    pmcid_list2.append(j)

        cnt = 0
        for i in pmcid_list1:
            if i in pmcid_list2:
                cnt += 1

        m = min(len(pmcid_list1),len(pmcid_list2))
        return cnt

    # This function calculates document similarity by distance between two nodes
    # in the relevance network.
    def method2(self,pmcid1,pmcid2):
        pass

    #
    def method3(self,pmcid1,pmcid2):
        cluster = self.idToCluster[pmcid2]

        pmcids = []
        for clu in cluster:
            clusterToId[clu]

    # Return the score calculated by cosine similarity between doc1 and doc2
    # The score is calculated by summing up the two functions, get_document_document_similarity
    # and get_document_clique_similarity giving weights alpha and beta. 
    def get_document_similarity(self,doc1,doc2):
        return self.get_document_similarity(doc1,doc2)*alpha + self.get_document_clique_similarity(doc1,doc2)*beta
