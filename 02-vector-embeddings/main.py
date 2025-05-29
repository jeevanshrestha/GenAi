from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

text = "The quick brown fox jumps over the lazy dog."
response = client.embeddings.create(
    input=text,
    model="text-embedding-ada-002"
)
print(response)
embeddings = response.data[0].embedding
print(f"Text: {text}")
print(f"Embeddings: {embeddings[:10]}...")  # Print first 10 dimensions for brevity