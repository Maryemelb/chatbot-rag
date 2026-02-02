from langchain_community.embeddings import HuggingFaceEmbeddings
import chromadb
from chromadb.config import Settings
import os
import asyncio
async def retriever(query: str,embedding,collection_vect,db_path, nbr_results=3):
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
  return result['documents'][0],metadatas, query_vector, pages, pages_label


db_path = os.getenv("CHROMA_PATH", "./core/dataset/chroma_data")
# Initialize the PersistentClient
client = chromadb.PersistentClient(
    path=db_path,
    settings=Settings(allow_reset=True)
)
collection_vect= client.get_or_create_collection('pdf_vectors2')
embedding= HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
res,metadatas,vect, page,pages_label= asyncio.run(retriever('what is the suject of this book',embedding,collection_vect,db_path, nbr_results=3))
print(res)
print('hi')
print(vect)
print(metadatas)
print(page)
print(pages_label)
