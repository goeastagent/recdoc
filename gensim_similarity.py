import os
from gensim import utils
from simserver import SessionServer

server = SessionServer('myserver')
w = open('data/1/549518.txt').read()

docin = {'id': '549518', 'tokens' : utils.simple_preprocess(w)}

print server.find_similar(docin)
