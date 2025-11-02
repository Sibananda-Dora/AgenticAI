#this is using typeddict state. for graph visualisation you can use the jupyterNotebook(.ipynb) extention.
# NOTHING IS ENFORCED DURING RUNTIME (suppose you give int value to name then it is acceptable here).
from typing import TypedDict,Literal
import random
from langgraph.graph import StateGraph,START,END

class TypedDictState(TypedDict):
    name: str
    game:Literal['cricket','badminton']

def start_play(state:TypedDictState):
    print("Node Called.")
    return {"name":state["name"]+ " wants to play"}

def badminton(state:TypedDictState):
    print("Badminton node Called.")
    return {"name":state["name"],"game":" badminton."}

def cricket(state:TypedDictState):
    print("Cricket node Called.")
    return {"name":state["name"],"game":" cricket."}

def decide_play(state:TypedDictState)-> Literal['badminton','cricket']:
    if random.random() < 0.5:
        return "badminton"
    else:
        return "cricket"


graph=StateGraph(TypedDictState)

graph.add_node("start_play",start_play)
graph.add_node("cricket",cricket)
graph.add_node("badminton",badminton)

graph.add_edge(START,"start_play")
graph.add_conditional_edges("start_play",decide_play)
graph.add_edge("cricket",END)
graph.add_edge("badminton",END)
from IPython.display import Image,display
#compilation
graph_builder= graph.compile()
result=graph_builder.invoke({"name":"Sibananda"})
print(result)


# #view
# display(Image(graph_bulider.get_graph().draw_mermaid_png()))