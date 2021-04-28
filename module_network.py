from pyvis.network import Network
from pyvis.options import Options
import random

def getRandomColor():
    random_number = random.randint(0,16777215)
    hex_number = str(hex(random_number))
    hex_number ='#'+ hex_number[2:]
    return hex_number

def isStartNode(num):
    res= True
    if num%2 == 0:
        res= False
    return res

def isTerminal(exp):
    res= True
    #normally there shuld no be a "(" in a terminal expression
    if exp.find("(") > -1: 
        res= False
    return res

def getNodeData(node, num, explorationStack, n_type):
    n_label= node
    if n_type == "rule": #if it's a rule
        if isStartNode(num) and len(explorationStack) > 0:
            n_id= explorationStack[len(explorationStack)-1] #getLast appened element
        else:
            n_id= "r"+str(num)
        n_color= "yellow"
    elif n_type == "premise" or n_type == "premise2":
        n_id= "p"+str(num)
        n_color= "green"
    elif node == "error": #if it's an normal error
        n_id= node
        n_color= "red"
    else:
        n_id= node
        n_color= "blue"
    return [n_id, n_label, n_color, n_type]

def addAll(net, facts):
        count= 1
        linkColor= getRandomColor()
        #Data for the exploration graph:
        explorationStack= []
        lastRuleId=""
        factsLength= len(facts)
        for fact in facts:
            print("fact", fact)
            types= fact[1].split("->")
            na= getNodeData(fact[0], count, explorationStack, types[0]) # nodeType [id, label, color]
            nb= getNodeData(fact[2], count+1, explorationStack, types[1])
            net.add_node(na[0], label=na[1], color=na[2])
            net.add_node(nb[0], label=nb[1], color=nb[2])
            net.add_edge(na[0], nb[0], label=" ", color=linkColor)
            if len(explorationStack) == 0:
                explorationStack.append(na[0])
                explorationStack.append(nb[0])
            else: #else push the expression
                if nb[3] == "premise2":
                    if nb[1] == "error":
                        clr= "red"
                    else:
                        clr= "blue"
                    net.add_node(nb[1], label=nb[1], color= clr)
                    net.add_edge(nb[0], nb[1], label=" ", color=linkColor)
                else:
                    if isTerminal(nb[1]) and nb[3] != "premise":
                        explorationStack.pop()
                    else:
                        if nb[3] == "exp" or nb[3] == "rule":
                            explorationStack.append(nb[0])
            count += 2
            print("stack: ", explorationStack)

def displayNetwork(tab):
    net = Network(bgcolor='#333333', font_color='white', height='100%', width='100%', directed=True)

    addAll(net, tab)

    net.set_options('{ "manipulation": { "enabled": true }, "interaction": { "multiselect": true, "navigationButtons": true }, "configure": { "enabled": true, "filter": "layout,physics", "showButton": true }, "edges": { "smooth": { "enabled": false } }, "layout": { "hierarchical": { "enabled": true, "sortMethod": "directed" } }, "physics": { "hierarchicalRepulsion": { "centralGravity": 0, "springLength": 50, "springConstant": 0.045, "nodeDistance": 190 }, "minVelocity": 0.75, "solver": "hierarchicalRepulsion" } }')
    net.show("network.html")
