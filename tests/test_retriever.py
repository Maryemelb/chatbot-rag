import sys
import os
# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest 
from langchain_community.embeddings import HuggingFaceEmbeddings
from core.rag_pipeline.data_injection import data_injuction

# @pytest.fixture
# def embedding():
#   embedding= HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#   return embedding

def test_retriever():
  chunks= data_injuction()
  assert chunks is not None

