
#this is using DataClasses state. for graph visualisation you can use the jupyterNotebook(.ipynb) extention.

from dataclasses import dataclass
from typing import Literal
import random
from langgraph.graph import StateGraph,START,END

@dataclass
class DataClassState:
    name: str
    game:Literal['cricket','badminton']

def start_play(state:DataClassState):
    print("Node Called.")
    return {"name":state.name+ " wants to play"}

def badminton(state:DataClassState):
    print("Badminton node Called.")
    return {"name":state.name,"game":" badminton."}

def cricket(state:DataClassState):
    print("Cricket node Called.")
    return {"name":state.name,"game":" cricket."}

def decide_play(state:DataClassState)-> Literal['badminton','cricket']:
    if random.random() < 0.5:
        return "badminton"
    else:
        return "cricket"


graph=StateGraph(DataClassState)

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
result=graph_builder.invoke(DataClassState(name="Sibananda",game=decide_play))
print(result)


# #view
# display(Image(graph_bulider.get_graph().draw_mermaid_png()))