from langchain_community.embeddings import HuggingFaceEmbeddings

#embeddings = HuggingFaceEmbeddings()
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
text = "This is a test document."

text_embedding = embeddings.embed_query(text)

print(len(text_embedding)) # 768
print("hello")
print(text_embedding)