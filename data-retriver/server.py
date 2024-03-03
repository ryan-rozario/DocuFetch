from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import chromadb
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

app = FastAPI()

class QueryRequest(BaseModel):
    input: str

llm = Ollama(model="llama2")

prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:
<context>
{context}
</context>
Question: {input}""")

document_chain = create_stuff_documents_chain(llm, prompt)

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="./vector-db/chromadb/persistent_storage")
langchain_chroma = Chroma(
    client=client,
    collection_name="collection_name",
    embedding_function=embeddings
)

retriever = langchain_chroma.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

@app.post('/query')
def query(query_request: QueryRequest):
    input_text = query_request.input
    response = retrieval_chain.invoke({"input": input_text})
    return response
