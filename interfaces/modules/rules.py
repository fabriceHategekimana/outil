from interfaces.modules.evaluation import *
from interfaces.modules.db import *

d = Data()

#The basic rules with a security (to avoid a problem when the user put some undevelopped expressions)
RULES= [
        ['add(N;O)', 'N->P;O->Q', 'add(P;Q)'],
        ['sub(N;O)', 'N->P;O->Q', 'sub(P;Q)'],
        ['mul(N;O)', 'N->P;O->Q', 'mul(P;Q)'],
        ['div(N;O)', 'N->P;O->Q', 'div(P;Q)'],
        ['get(L,N)', 'L->Lp;N->Np', 'get(Lp,Np)'],
        ['set(L,N,V)', 'Li->Lp;N->Np;V->Vp', 'set(Lp;Np;Vp)'],
        ['append(L,N)', 'L->Lp;N->Np', 'append(Lp;Np)'],
        ['insert(L,N)', 'L->Lp;N->Np', 'insert(Lp;Np)'],
        ['remove(L,N)', 'L->Lp;N->Np', 'remove(Lp;Np)'],
        ['removeLast(L)', 'L->Lp', 'removeLast(Lp)']
        ]

def formatRule(exp):
    res= syntaxChecking(exp)
    if res[0] == "&":
        res= "error"
    else:
        res= res.replace(" ", "")
        res= decompose(res)
    return res

def syntaxChecking(exp):
    parser.parse("check "+exp, debug=False)
    f = open("res.txt", "r")
    res= f.readline()
    f.close()
    return res

def decompose(exp):
    tab= exp.split("--")
    entete= tab[1].split(symbol(tab[1]))[0]
    return [entete, tab[0], tab[1]]

def getRules():
    return d.sqlQuery("select header, premises, conclusion from exp_rules union select header, premises, conclusion from state_rules;")

def insertRule(rule):
    if rule[0][0] == "<":
        #rule[0]= rule[0][rule[0].find(">")+1:]
        table= "state_rules"
    else:
        table= "exp_rules"
    d.sqlModify("insert into "+table+"(header, premises, conclusion) values('%s','%s','%s');" % tuple(rule))

def insertDefaultRules():
    for rule in RULES:
        insertRule(rule)

def deleteComment(line):
    while(line.find("/*") != -1):
        line= line[:line.find("/*")]+line[line.find("*/")+2:] #delete comments
    return line

def importRules(name):
    VERBOSE= verbose
    #we delete the content of each table of the database
    d.sqlModify("delete from exp_rules")
    d.sqlModify("delete from state_rules")
    d.sqlModify("delete from links")
    insertDefaultRules()
    error= False
    #On ouvre le fichier
    f = open(name, "r")
    #a list of each statements
    sentences= f.read().replace("\n","").split(".")
    Program= deleteComment(sentences.pop())
    if Program[:7] != "Program":
        print("Error: Missing the Program section at the bottom of the page (after the rulses)")
        error= True
    if error == False:
        #Pour chaque ligne on test si la règle est juste puis on continue
        for line in sentences:
            if line.find("/*") != -1:
                line= deleteComment(line)
            res= syntaxChecking(line)
            if res[0] == "&":
                print("Error : '"+line[:-1]+"' \n"+res[1:])
                error= True
                break
            else:
                rule= decompose(res)
                insertRule(rule)
    return Program, error

def deleteFirstWhiteSpaces(program):
    i= 0
    while(program[i]==' '): 
        i += 1
    return program[i:]

def getStateAndExp(Program):
    program= Program[Program.find("{")+1:Program.find("}")].replace("\t", "")
    separationPoint= program.find(">")
    if separationPoint != -1: #if there is a state
        state= program[1:separationPoint+1] #we delete the uselesse first character " "
        exp= program[separationPoint+1:]
    else:
        state= ""
        exp= deleteFirstWhiteSpaces(program) #we delete the uselesse first character " "
    return state, exp
