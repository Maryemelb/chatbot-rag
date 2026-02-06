from langchain_community.embeddings import HuggingFaceEmbeddings
import chromadb
from chromadb.config import Settings
import os
import asyncio
from core.services.gemini_service import unswer
async def retriever(query: str,embedding,collection_vect, nbr_results=8):
  #embed the query
  query_vector= embedding.embed_query(query)
  #search on the cllection

  result= collection_vect.query(
    query_embeddings= [query_vector],
    n_results= nbr_results
  )  
  #get page number
  metadatas= result['metadatas'][0]
  pages= [ item.get('page') for item in metadatas]
  pages_label= [ item.get('page_label') for item in metadatas]
  retriever_response=result['documents'][0]
  context_for_gemini = "\n\n---\n\n".join(retriever_response)
  
  gemini_response= unswer(query, context_for_gemini)
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