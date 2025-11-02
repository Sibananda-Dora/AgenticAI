from typing import TypedDict,Annotated
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from IPython.display import display,Image

load_dotenv()
os.environ["GOOGLE_API_KEY"]=os.getenv("GEMINI_API_KEY")

llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")
# llm.invoke("hello")
# result=llm.invoke("hello")
# print(result.content)

class State(TypedDict):
    messages:Annotated[list,add_messages]

def chatbot(state:State):
    return {"messages":[llm.invoke(state['messages'])]}

graph=StateGraph(State)

graph.add_node("chatbot",chatbot)

graph.add_edge(START,"chatbot")
graph.add_edge("chatbot",END)

graph_builder=graph.compile()
# display(Image(graph_builder.get_graph().draw_mermaid_png()))


for event in graph_builder.stream({"messages":{"role":"user","message":"Hey there"}}):
    print(event)