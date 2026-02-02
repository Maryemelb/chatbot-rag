from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
import os 
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv() 

loader = PyPDFLoader("./core/dataset/data_pdf.pdf")
documents = loader.load()  

splitter = RecursiveCharacterTextSplitter(
    chunk_size=250,
    chunk_overlap=30,
    separators=["\n\n", "\n", ".", " "]
)

# 3. Découper en chunks en conservant les métadonnées
chunks = splitter.split_documents(documents)

#affichage
for c in chunks[:3]:
    print(f"PAGE: {c.metadata['page']} | TEXTE: {c.page_content}\n")

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#Embuding

# client = chromadb.HttpClient(
#     host="localhost",
#     port=8005
# )

#added
db_path = os.getenv("CHROMA_PATH", "./core/dataset/chroma_data")

# Initialize the PersistentClient
client = chromadb.PersistentClient(
    path=db_path,
    settings=Settings(allow_reset=True)
)
#create a collection
collection = client.get_or_create_collection(
    name="pdf_collection"
)
#save shunks
#add data to collection

collection.add(
    documents=[c.page_content for c in chunks],
    metadatas=[c.metadata for c in chunks],
    ids=[f"doc_{i}" for i in range(len(chunks))]
)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


print(f"Added {len(chunks)} chunks to chroma db")
print(collection.count())

# chroma_client = chromadb.HttpClient(host=os.getenv("CHROMA_HOST"), port=int(os.getenv("CHROMA_PORT")), settings=Settings())
data = collection.get(limit=2)  # fetch first 10 documents
for i, (doc, meta) in enumerate(zip(data["documents"], data["metadatas"])):
    print(f"Document {i+1}")
    print("PAGE:", meta.get("page"))
    print("TEXT:", doc[:300])  # first 300 chars
    print("-"*50)


#transform chuncks to vector and save it in chromadb
collection_vect = client.get_or_create_collection(
    name="pdf_vectors2"
)

batch_size = 50
for i in range(0, len(chunks), batch_size):
    batch = chunks[i:i+batch_size]
    vectors = embeddings.embed_documents([c.page_content for c in batch])
    collection_vect.add(
        documents=[c.page_content for c in batch],
        metadatas=[c.metadata for c in batch],
        ids=[f"doc_{i+j}" for j, c in enumerate(batch)],
        embeddings=vectors
    )
    print(f'batch {i} added')
     # Display only the first document of this batch
    first_doc = batch[0]
    print(f"Added doc ID: doc_{i}")
    print("PAGE:", first_doc.metadata.get('page'))
    print("TEXT (first 100 chars):", first_doc.page_content[:100])
    print("Vector length:", len(vectors[0]))
    print("-"*50)
    print("Vector sample (first 10 dimensions):", vectors[0][:10])

    
    print(f"Batch {i} added \n")

