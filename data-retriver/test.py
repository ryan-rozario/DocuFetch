import chromadb

client = chromadb.PersistentClient(path="./vector-db/chromadb/persistent_storage")
collection = client.get_collection("document-store")
result = collection.query(
            query_texts=["What is hyperLogLog"],
            n_results=2,
            # where={"metadata_field": "is_equal_to_this"}, # optional filter
            # where_document={"$contains":"search_string"}  # optional filter
        )
print(result)