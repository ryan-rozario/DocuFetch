
from langchain_community.llms import Ollama
llm = Ollama(model="llama2")

from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are world class technical documentation writer."),
    ("user", "{input}")
])

chain = prompt | llm 

from langchain_core.output_parsers import StrOutputParser

output_parser = StrOutputParser()

chain = prompt | llm | output_parser

from langchain.chains.combine_documents import create_stuff_documents_chain

prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

document_chain = create_stuff_documents_chain(llm, prompt)

from langchain_community.vectorstores import Chroma

import chromadb
from langchain_community.embeddings import SentenceTransformerEmbeddings
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="./vector-db/chromadb/persistent_storage")
# load it into Chroma
langchain_chroma = Chroma(
    client=client,
    collection_name="collection_name",
    embedding_function = embeddings
)

from langchain.chains import create_retrieval_chain

retriever = langchain_chroma.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

response = retrieval_chain.invoke({"input": "what is hyperloglog]"})
print(response["answer"])

