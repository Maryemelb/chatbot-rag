
import asyncio
from fastapi import APIRouter, Depends, HTTPException
from pytest import Session
from requests import request

from core.rag_pipeline.retriever import retriever
from ..schemas.user_schema import user_schema
from app.dependencies.dependencies import get_current_user, getdb
from app.models.user import User
from passlib.context import CryptContext
from app.models.query import Query
from app.schemas.query_schema import query_schema
from app.dependencies.dependencies import embedding
from app.dependencies.dependencies import client
import numpy as np
import time
import pickle
router= APIRouter(
         tags= ["query"]
)

@router.post('/query')
def register(query_schema:query_schema,  db:Session= Depends(getdb), current_user: User= Depends(get_current_user)):
    
    with open("core/saved_model/kmeans.pkl", "rb") as f:
       model = pickle.load(f)
    with open("core/saved_model/pca.pkl", "rb") as f:
       pca = pickle.load(f)
    
    start_time= time.time()
    #vectorize question
    new_embedding = embedding.embed_query(query_schema.question)
    new_embedding_np = np.array(new_embedding).reshape(1, -1)
    q_pca= pca.transform(new_embedding_np)

    predicted_cluster= model.predict(q_pca)
    cluster_id = int(predicted_cluster[0])
    end_time= time.time()
    latency_ms= (end_time - start_time) * 1000

    collection_vect= client.get_or_create_collection('pdf_vectors2')

    context_for_gemini,gemini_response,metadatas, query_vector, pages,retriever_response= asyncio.run(retriever(query_schema.question ,embedding,collection_vect, nbr_results=30))
     
    insert_query= Query(
       question= query_schema.question,
       userid= current_user.id,
       answer= gemini_response,
       cluster= cluster_id,
       latency_ms= latency_ms
    )
    db.add(insert_query)
    db.commit()
    db.refresh(insert_query)

    
    return insert_query