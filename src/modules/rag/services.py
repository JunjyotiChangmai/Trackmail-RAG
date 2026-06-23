import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from src.config import settings

class RAGService:
    def __init__(self):
        self.chain = None

    def _format_docs(self, docs):
        return "\n".join(doc.page_content for doc in docs)

    async def initialize_pipeline(self):
        os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY or ""
        
        # Load and Chunk Documents
        loader = Docx2txtLoader(settings.DATASET_PATH)
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
        splits = text_splitter.split_documents(docs)
        
        # Vector Store Setup
        vectorstore = Chroma(
            collection_name=settings.COLLECTION_NAME, 
            embedding_function=OpenAIEmbeddings()
        )
        vectorstore.add_documents(splits)
        retriever = vectorstore.as_retriever()
        
        # Build Prompt & Chain
        prompt = PromptTemplate.from_template("""
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise. GIve only whats asked no addition information. When some one greet then you also greet and say who you are and how you acn help the user
Question: {question}
Context: {context}
Answer:
""")
        llm = ChatOpenAI()
        
        self.chain = (
            {"context": retriever | self._format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

    async def get_answer(self, question: str) -> str:
        if not self.chain:
            raise ValueError("RAG pipeline has not been initialized.")
    
        return self.chain.invoke(question)

rag_service = RAGService()