product_mapping = {
    "settings": {
        "number_of_shards": 2,
        "number_of_replicas": 2,
        "analysis": {
            "analyzer": {
                "edge_analyzer": {
                    "tokenizer": "edge_tokenizer"
                },
                "std_analyzer": {
                    "type": "standard"
                }
            },
            "tokenizer": {
                "edge_tokenizer": {
                    "type": "edge_ngram",
                    "min_gram": 2,
                    "max_gram": 10,
                    "token_chars": [
                        "letter",
                        "digit"
                    ]
                }
            }
        }
    },
    "mappings": {
        "properties": {
        "ProductID":{
            "type":"long"
        },
        "ProductName":{
            "type":"text"
        },
        "ProductBrand":{
            "type":"text"
        },
        "Gender":{
            "type":"text"
        },
        "Price (INR)":{
            "type":"long"
        },
        "NumImages":{
            "type":"long"
        },
        "Description":{
            "type":"text"
        },
        "PrimaryColor":{
            "type":"text"
        },
        "DescriptionVector":{
            "type":"dense_vector",
            "dims": 384,  # Updated size
            "index": True,
            "similarity": "l2_norm"        }
        }
    }
}