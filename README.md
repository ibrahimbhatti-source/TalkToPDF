It's UI is built using Streamlit and unfortunately streamlit apps cannot be hosted natively on Vercel. well this is a simple RAG based application. it can be further improved by adding the chat history so that user can do multiple conversations at a single session. 

## Tech Stack

<table>
  <tr>
    <td align="center" width="150">
      <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" width="65" height="65" alt="Python"/>
      <br><b>Python</b>
      <br>Core Language
    </td>
    <td align="center" width="150">
      <img src="https://raw.githubusercontent.com/lobehub/lobe-icons/master/packages/static-svg/icons/langchain-color.svg" width="65" height="65" alt="LangChain"/>
      <br><b>LangChain</b>
      <br>AI Framework
    </td>
    <td align="center" width="150">
      <img src="https://cdn.jsdelivr.net/gh/homarr-labs/dashboard-icons/svg/chroma.svg" width="65" height="65" alt="ChromaDB"/>
      <br><b>ChromaDB</b>
      <br>Vector Database
    </td>
  </tr>
</table>

<br>
</div>

Let's discuss some technical details of the project
1. Document Loader (PyPDFLoader) used to load the pdf. PyPDFLoader can handle simple pdfs only.
2. Vector Store (ChromaDB) it is perfect choice because it gives us vector database features while being vector store it is friendly for local development.
3. Retriver (VectorStore Retriever of ChromaDB)

Runnables:
1. RunnableParallel
2. RunnableSequence

The user pdf is automatically deleted when the response is generated.

Workflow:
Query only --> General Response | 
Query + PDF --> Response from User PDF
