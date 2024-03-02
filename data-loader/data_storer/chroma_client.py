import chromadb
from typing import List, Dict

class ChromaDb:

    def __init__(self):
        #self.client = chromadb.HttpClient(host='localhost', port=8000)
        self.client = chromadb.PersistentClient(path="./vector-db/chromadb/persistent_storage")
        self.collection = self.client.get_or_create_collection("document-store")
        
    def add(self, text: List[str], id: List[str], metadata: List[Dict]):
        self.collection.add(
        documents=text, # we handle tokenization, embedding, and indexing automatically. You can skip that and add your own embeddings as well
        metadatas=metadata, # filter on these!
        ids=id, # unique for each doc
        )

    def query(self, query_text: str, num_result: int):
        results = self.collection.query(
            query_texts=["This is a query document"],
            n_results=2,
            # where={"metadata_field": "is_equal_to_this"}, # optional filter
            # where_document={"$contains":"search_string"}  # optional filter
        )
