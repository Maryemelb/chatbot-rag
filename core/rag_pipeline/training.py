from langchain_chroma import Chroma
import os 
import sys
import pickle
from sklearn.datasets import make_blobs
project_root = os.path.abspath(os.path.join(os.getcwd(), '..'))
sys.path.append(project_root)
import matplotlib.pyplot as plt
from app.db.database import sessionLocal
from app.models.question import Question
from app.models.user import User     
from app.models.query import Query    
from app.models.question import Question # Load Question
from app.dependencies.dependencies import embedding
from dotenv import load_dotenv
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import chromadb
import numpy as np
#from chromadb.config import Setting
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
load_dotenv() 

#embed
def training():
  embuding_function= SentenceTransformerEmbeddings(model_name= "all-MiniLM-L6-v2")
  print(type(embuding_function))
  db= sessionLocal()
  try:
    questions = db.query(Question).all()
    all_questions= []
    for c in questions:
        q_vector= embedding.embed_query(c.question)
        all_questions.append(q_vector)
    np_question= np.array(all_questions)
    best_k= 5

    #PCA transform

    pca= PCA(n_components=0.95)
    X= np_question
    X_pca = pca.fit_transform(X)
    #train
    kmeans_model = KMeans(n_clusters=best_k, n_init='auto', random_state=42)
    kmeans_model.fit(X_pca)

    
    try:
        os.makedirs('saved_model', exist_ok=True)
        with open('core/saved_model/kmeans.pkl', 'wb') as f:
            pickle.dump(kmeans_model, f)
        with open('core/saved_model/pca.pkl', 'wb') as f:
            pickle.dump(pca, f)
    except IOError as e:
        print(f"Could not save model. Disk error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
  finally:
     db.close()

#kmeans metrics
print('hi')
training()
print('hello')
"""
# 1. Define your new question
new_question_text = "How do I reset my password?"

# 2. Embed the new question using the same embedding function
new_embedding = embedding.embed_query(new_question_text)
new_embedding_np = np.array([new_embedding]) # Reshape for sklearn (1, N)

# 3. Transform using the EXISTING PCA model
# Note: Use .transform(), NOT .fit_transform()
new_X_pca = pca.transform(new_embedding_np)

# 4. Predict the cluster
predicted_cluster = kmeans_model.predict(new_X_pca)

print(f"The question belongs to cluster: {predicted_cluster[0]}")

"""