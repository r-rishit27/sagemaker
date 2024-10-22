from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import Chroma
import os

llm=ChatGoogleGenerativeAI(model="gemini-pro")
embeddings=GoogleGenerativeAIEmbeddings(model="models/embedding-001")
#load and split pdf into multiple pages
loader=PyPDFLoader("item_list.pdf")
pages=loader.load_and_split()

#initialize VectorDB and Retriever
#this step converts pages into embedding
vectordb=Chroma.from_documents(pages,embeddings)
#retriever
retriever=vectordb.as_retriever(search_kwargs={"k":2})
#we want to retrieve 2 nearest chunks

#defining the retrieval chain
template = """
You are a helpful AI assistant.
Your work is to give the link of input
In the pdf format is 
input1**input1_link**
input2**input2_link**
and so on
input: {input}
Context:{context}
Please provide only the link associated with the input:
answer:
"""

prompt= PromptTemplate.from_template(template)
#chain that wires llm and prompt and then vector db(retriever)
combine_docs_chain=create_stuff_documents_chain(llm,prompt)
retrival_chain=create_retrieval_chain(retriever,combine_docs_chain)

#invoking chain
response=retrival_chain.invoke({"input":"item"})

#Print the answer to the question
print(response["answer"])






