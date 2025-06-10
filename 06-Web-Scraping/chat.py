from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
load_dotenv()  # Load environment variables from .env file 

embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_vectors",
    embedding=embedding_model
)
query = input(">> ")

search_results = vector_db.similarity_search(query, k=3)  # Search for similar documents 
#for result in search_results:
 #   print(result.page_content)  # Print the content of each result
#    print(result.metadata)  # Print the metadata of each result

context = "\n\n".join([f"Page {result.metadata['page_label']  }: {result.page_content}" for result in search_results])

#print(context)
SYSTEM_PROMPT = """
You are a helpful AI assistant that answers user questions based on the provided context retrieved from web scraped json file along with page_contents and page_number.

You should only answer the user based on the following context and navigate the user to open the right page number to know more

about the topic. If the context does not provide enough information, you should politely inform the user that you cannot answer the question based on the provided context.
Your response should be concise and directly related to the user's query. 

Important: All your responses must be formatted as a JSON object.

Context:
{context}



"""
client = OpenAI()

messages = [
    {"role": "system", "content": SYSTEM_PROMPT.format(context=context)},
    {"role": "user", "content": query}
]

chat_completion = client.chat.completions.create(
    model="gpt-4.1",
    messages=messages,
    response_format={"type": "json_object"},
    max_tokens=1000,
    temperature=0.2
)

print(chat_completion.choices[0].message.content)

while True:  # chat user query
    query = input(">> ")
    if query.lower() in ["exit", "quit"]:
        break
    messages.append({"role": "user", "content": query})  # Add user query to messages
    # Call the OpenAI API to get a chat completion
    # The response will be in JSON format as specified
    chat_completion = client.chat.completions.create(
        model="gpt-4.1",
        messages=messages,
        response_format={"type": "json_object"},
        max_tokens=1000,
        temperature=0.2
    )

    print(chat_completion.choices[0].message.content)  # Print the AI's response