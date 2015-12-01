# !/bin/bash

host="http://localhost:9200";

bm25="bm25"

#curl -XPOST ${host}/$bm25/ -d @setting_BM25.json #
#curl -XGET http://localhost:9200/bm25/article/3586697/_termvector?pretty=true -d @termvector.json

curl -XGET http://localhost:9200/bm25/article/3586697/_termvector?pretty=true&fields=document
