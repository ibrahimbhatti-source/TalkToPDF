from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from dotenv import load_dotenv
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import streamlit as st
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

model = ChatGroq(model="openai/gpt-oss-120b")

parser = StrOutputParser()

user_query = st.chat_input("Chat with Your PDF: ", accept_file=True, file_type="pdf")


if user_query:
        if user_query.text and user_query.files:

            uploded_pdf = user_query.files[0]
            try:
                with open("user_pdf.pdf", "wb") as file:
                    file.write(uploded_pdf.getvalue())
                
                # Step 1 - Indexing     

                # Loading Document and Auto Spliting
                loader = PyPDFLoader(file_path="user_pdf.pdf")
                st.write("Uploaded PDF", uploded_pdf.name)
                docs = loader.load_and_split()

                gemini_embeddings = GoogleGenerativeAIEmbeddings(
                    model="models/gemini-embedding-2"
                )
            
                # Vector Store
                chroma_vector_store = Chroma.from_documents(
                    documents=docs,
                    embedding=gemini_embeddings,
                    collection_name="ChatWithPDF",
                )

                # Step 2 - Retrieval
                retriver = chroma_vector_store.as_retriever(search_type="similarity", search_kwargs={"k":1})

                # Step 3 -  Augmentation 
                prompt = PromptTemplate(template="""Answer the user query from the provided context. 
                The context includes metadata with a 'page' number (0-indexed). 
                Cite the page number (add 1 to the page index) in your answer like [Page X].
                
                Context: {context}
                User Query: {user_query}""", input_variables=["context","user_query"])

                # Step 4 - Generation 

                ParallelChain = RunnableParallel(
                {"context":retriver,
                "user_query": RunnablePassthrough()})

                chain = ParallelChain | prompt | model | parser
                response = chain.invoke(user_query.text)
                with st.chat_message("ai"):
                    st.write(response)
                    chroma_vector_store.delete_collection()

            finally:
                if os.path.exists("user_pdf.pdf"):
                    os.remove("user_pdf.pdf")

        elif user_query.text:
            general_prompt = PromptTemplate(template="Greet the user, and ask him that you are a ai assistant that helps users to chat with their pdf's, here is the query. {user_query}")

            general_chain = general_prompt | model | parser
            general_response = general_chain.invoke({"user_query":user_query.text})
            with st.chat_message("ai"):
                st.write(general_response)
else:       
     st.write("please upload a pdf to continue")