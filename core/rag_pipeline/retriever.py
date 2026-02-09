from langchain_community.embeddings import HuggingFaceEmbeddings
import chromadb
from chromadb.config import Settings
import os
import asyncio
from core.services.gemini_service import unswer
from mlflow import pyfunc
import mlflow
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000"))
mlflow.set_experiment("rag_experiment")

async def retriever(query: str,embedding,collection_vect, nbr_results=8):
 with mlflow.start_run(run_name="retriever_execution"):
    mlflow.log_param("nbr_results", nbr_results)
    mlflow.log_param("query", query)
      #track time of embeding
    with mlflow.start_span('embeding') as span:
      #embed the query
      query_vector= embedding.embed_query(query)
      #search on the cllection
      span.set_attribute("embeding_vector_dim", len(query_vector))

    result= collection_vect.query(
        query_embeddings= [query_vector],
        n_results= nbr_results
      )  
      #get page number
  
    metadatas= result['metadatas'][0]
    pages= [ item.get('page') for item in metadatas]
    pages_label= [ item.get('page_label') for item in metadatas]
    
    with mlflow.start_span('chunks_retrieval') as span:
       retriever_response=result['documents'][0]
       span.set_attribute("retrieved_chunks_count", len(retriever_response))

    context_for_gemini = "\n\n---\n\n".join(retriever_response)
    #get the response val
    with mlflow.start_span('gemini_api') as span:
      gemini_response= unswer(query, context_for_gemini)
      mlflow.log_text(gemini_response, 'gemini_response.txt')
 
    return context_for_gemini,gemini_response,metadatas, query_vector, pages,retriever_response


# db_path = os.getenv("CHROMA_PATH", "./core/dataset/chroma_data2")
# # Initialize the PersistentClient
# client = chromadb.PersistentClient(
#     path=db_path,
#     settings=Settings(allow_reset=True)
# )
# collection_vect= client.get_or_create_collection('pdf_vectors2')
# embedding= HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# print("heollo")
# context_for_gemini,gemini_response,metadatas, query_vector, pages,retriever_response= asyncio.run(retriever('How did the author s early experience as a tinkerer lead to his career in IT support ',embedding,collection_vect, nbr_results=30))
# print(retriever_response)
# print('context')

# print(context_for_gemini)

# print('gemini')
# print(gemini_response)
# #How did the author s early experience as a tinkerer lead to his career in IT support 