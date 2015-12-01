# !/bin/bash

host="http://localhost:9200";

bm25="bm25"

curl -XPOST ${host}/$bm25/ -d @setting_BM25.json
