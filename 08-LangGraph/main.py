from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI  # Use the correct import for ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from langgraph.checkpoint.mongodb import MongoDBSaver
import os

load_dotenv()

DB_URI = os.getenv("MONGO_URI") 
class State(TypedDict):
    messages: Annotated[list, add_messages]

llm = ChatOpenAI(model="gpt-4.1")

def chat_node(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}
     
graph_builder = StateGraph(State)
graph_builder.add_node("chat_node", chat_node)
graph_builder.add_edge(START, "chat_node")
#graph = graph_builder.compile()

def compile_graph_with_checkpointer(checkpointer):
    graph_with_checkpointer =  graph_builder.compile(checkpointer=checkpointer)
    return graph_with_checkpointer
#graph = compile_graph_with_checkpointer()

def main():
    
    config = {"configurable":{"thread_id":"1"}}    
    with MongoDBSaver.from_conn_string(DB_URI) as mongo_checkpoiner:
        graph_with_mongo = compile_graph_with_checkpointer(mongo_checkpoiner)
        query =input("> ")
        result = graph_with_mongo.invoke({"messages":[{"role":"user","content": query}]}, config = config)
        print(result)
    
if __name__ == "__main__":
    main()