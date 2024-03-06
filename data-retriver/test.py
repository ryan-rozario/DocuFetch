import chromadb

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain

llm = Ollama(model="llama2")

prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:
<context>
{context}
</context>
Question: {input}""")

document_chain = create_stuff_documents_chain(llm, prompt)


embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="./vector-db/chromadb/persistent_storage")
# load it into Chroma
langchain_chroma = Chroma(
    client=client,
    collection_name="document-store",
    embedding_function = embeddings
)

from langchain.chains import create_retrieval_chain

retriever = langchain_chroma.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.001})
#retrieval_chain = create_retrieval_chain(retriever, document_chain)
docs = retriever.get_relevant_documents("who isryan rozario")
print(docs)

#response = retrieval_chain.invoke({"input": "ryan rozario]"})
#print(response["answer"])

