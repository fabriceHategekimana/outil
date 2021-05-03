from interfaces.modules.compile import parser
from interfaces.modules.db import *
import re

d= Data()

def linkCreation(subject, goal, relation):
    if isinstance(subject, list):
        subject= subject[1]+"--"+subject[2]
    if isinstance(goal, list):
        goal= goal[1]+"--"+goal[2]
    elif goal.find("->") > -1:
        goal= goal[:goal.find("->")]
        relation += "2" #we append 2 to specify it's a premise that will call a recursion
    if subject.find("<") == 0: #if it's a state
        subject= subject[:subject.find(">")+1]
    if goal.find("<") == 0: #if it's a state
        goal= goal[:goal.find(">")+1]
    d.sqlModify("insert into links(subject,link,goal) values ('%s','%s','%s')" % (subject, relation, goal))

def verbose(txt, act="a"):
    f = open("log.txt", act)
    f.write(txt+"\n")
    f.close()

def evaluateInstruction(exp):
    verbose("", "w")
    if exp[0] == "<":
        verbose("evaluate state")
        res= evaluateState(exp).replace(";",",")
    else:
        verbose("evaluate expression")
        res= evaluateExpression(exp)
    return res

def evaluateState(state): # state stand for state+exp (= <....>name(...))
    verbose("------------------------EE")
    verbose("expression: %s" % state)
    final= "Error: instruction non developpable"
    selection= getSelection(state)
    for rule in selection:
        res= applyRule(state, rule)
        verbose("expression après application de la règle '%s': '%s'" % (rule, res))
        if res != "error":
            final= res
            break
    return final

def symbol(statement):
    res= ""
    if statement.find("->") > -1:
        res="->"
    elif statement.find("&in&") > -1:
        res="&in&"
    elif statement.find("==") > -1:
        res="=="
    elif statement.find(">=") > -1:
        res=">="
    elif statement.find("<=") > -1:
        res="<="
    elif statement.find("=") > -1:
        res= "="
    elif statement.find(">") > -1:
        res=">"
    elif statement.find("<") > -1:
        res="<"
    return res

def test(expression, substitution, rule):
    res= False
    expression= complete(expression, substitution)
    verbose("expression à tester: %s" % expression)
    linkCreation(rule, expression, "rule->premise")
    sym= symbol(expression)
    tab= expression.split(sym)
    left= evaluateExpression(tab[0])
    if sym in ["==",">",">=","<","<="]: # if its conditionnal test
        val= subEval(left+sym+tab[1])
        verbose("résultat du test de comparaison: %s" % val)
        if val == "True":
            res = substitution
    elif sym == "&in&": # if its a type test
        val= evalNativeType(left+" in "+tab[1])
        verbose("résultat du test in 1: %s" % val)
        if val == False:
            verbose("on continue")
            pass
        else:
            res= substitution
    elif sym == "->": # if it's an evaluation
        verbose("résultat du test -> : %s" % left)
        substitution.append([tab[1], left])
        res= substitution
    return res

def evalNativeType(exp):
    res= False
    if exp.find("in number") > 0:
        res= isNumber(exp.replace(" in number", ""))
    elif exp.find("in list") > 0:
        res= isList(exp.replace(" in list", ""))
    return res

def evaluateExpression(expression):
    verbose("------------------------EVAL")
    verbose("subEval de l'expression: %s" % expression)
    res= subEval(expression) 
    if not isTerminal(res):
        #res= pseudoEval(expression, data)
        res= evaluateExpressionHelper(expression)
        if not isTerminal:
            res= "error"
    return res

def evaluateExpressionHelper(expression):
    verbose("------------------------EE")
    verbose("expression: %s" % expression)
    final= "Error: instruction non developpable"
    selection= getSelection(expression)
    for rule in selection:
        res= applyRule(expression, rule)
        if res != "error":
            final= res
            break
    return final

def applyRule(expression, rule):
    linkCreation(expression, rule, "exp->rule")
    verbose("--------------------RULE")
    verbose("règle choisie: %s" % rule[1]+"--"+rule[2])
    final= "error"
    allTrue= True
    substitution= union(rule[0], expression) 
    if substitution == False: # if false the fact doesn't match go to the next rule/fact
        verbose("Le fait ne match pas, on passe à la prochaine règle")
        allTrue= False
        final= "error"
        linkCreation(rule, final,"rule->exp")
    elif substitution == True: # if true the fact match go directly to the conclusion
        verbose("Le fait match")
        pass
    else: # if this is an array of substitution, go check the premises
        if rule[1] != "":
            for premise in rule[1].split(";"): #loop: premises
                verbose("premisse obtenue: %s" % premise)
                res= test(premise, substitution, rule)
                verbose("res de %s: %s" % (premise,res))
                if res == False: #if a premise is false, we drop the rule
                    verbose("règle non accomplie")
                    linkCreation(rule, "error","rule->exp")
                    allTrue= False
                    break
                else:
                    verbose("règle accomplie")
                    substitution= res
    if allTrue == True:
        if substitution != True: # on fait les dernière substitutions si le tableau n'est pas vide
            sym= symbol(rule[2])
            if sym == "->": # if it's a custom rule
                conclusion= complete(rule[2].split(sym)[1],substitution)
            else: # if it's a builtin rule
                conclusion= subEval(complete(rule[2],substitution))
        else:
            conclusion= rule[2].split(symbol(rule[2]))[1] # on prend la partie de droite (qui n'a pas besoin d'être complêtée)
        verbose("conclusion: %s" % conclusion)
        linkCreation(rule, conclusion,"rule->exp")
        if conclusion[0] == "<":
            final= subEvalState(conclusion)
        else:
            final= evaluateExpression(conclusion)
    #verbose("final applyRule: %s" % final)
    return final

def subEvalState(exp):
    final= []
    tab= splitByExpression(exp.replace("<","").replace(">",""))
    for t in tab:
        final.append(evaluateExpression(t))
    return "<"+";".join(final)+">"

def applyRule2(expression, rule):
    final= "error"
    linkCreation(expression, rule,"exp->rule")
    conclusion= "error"
    allTrue= True
    substitution= union(rule[0], expression) 
    if substitution == False: # if false the fact doesn't match go to the next rule/fact
        allTrue= False
        final= "error"
        linkCreation(rule, final,"rule->exp")
    elif substitution == True: # if true the fact match go directly to the conclusion
        pass
    else: # if this is an array of substitution, go check the premises
        if rule[1] != "":
            for premise in rule[1].split(";"): #loop: premises
                res= test(premise, substitution, rule)
                if res == False: #if a premise is false, we drop the rule
                    allTrue= False
                    linkCreation(rule, "error","rule->exp")
                    break
                else:
                    substitution= res
    if allTrue == True:
        verbose("substitution: %s" % substitution)
        if substitution != True: # on fait les dernière substitutions si le tableau n'est pas vide
            sym= symbol(rule[2])
            if sym == "->":
                conclusion= complete(rule[2].split(sym)[1],substitution)
            else:
                conclusion= subEval(complete(rule[2],substitution))
            verbose("conclusion: %s" % conclusion)
        else:
            conclusion= rule[2].split(symbol(rule[2]))[1] # on prend la partie de droite (qui n'a pas besoin d'être complêtée)
        final= conclusion
        linkCreation(rule, conclusion,"rule->exp")
    return final

def getSelection(exp):
    if exp.find("<") == 0: #si on a un état
        if exp.find("(") > -1: # si on a une exp avec parenthèse
            newExp= exp[exp.find(">")+1:exp.find("(")]
        else:#sinon
            newExp= exp[exp.find(">")+1:]
        table= "state_rules"
        final= d.sqlQuery("select header,premises,conclusion from "+table+" where header like '%"+newExp+"%'")
    else: # si on a seulement une expression
        newExp= exp[0:exp.find("(")]
        table= "exp_rules"
        final= d.sqlQuery("select header,premises,conclusion from "+table+" where header like '"+newExp+"%'")
    return final

def getName(exp):
    name= re.findall("\w+\(", exp)
    if name == []:
        name = [""]
    return name[0]
        
def union(exp1, exp2):
    if exp1[0] == "<":
        res= unionState(exp1, exp2)
    else:
        res= unionExpression(exp1, exp2)
    return res

def unionState(exp1, exp2):
    exp1= toTuple(exp1)
    exp2= toTuple(exp2)
    tab1= exp1.split("&&")
    tab2= exp2.split("&&")
    verbose("tab1 %s" % tab1)
    verbose("tab2 %s" % tab2)
    return unionFinal(tab1, tab2)

def toTuple(exp):
    return myParser("state "+exp)

def unionExpression(exp1,exp2):
    #exp1 is the rule union, exp2 is the user union
    res= False
    exp1= exp1[exp1.find("(")+1:exp1.rfind(")")] #on enlève les parenthèses en trop
    exp2= exp2[exp2.find("(")+1:exp2.rfind(")")]
    tab1= splitByExpression(exp1)
    tab2= splitByExpression(exp2)
    return unionFinal(tab1, tab2)

def unionFinal(tab1,tab2):
    final= []
    if len(tab1) == len(tab2): #si les tables font la même longueur
        for i in range(len(tab1)): #on explore
            if isTerminal(tab1[i]): #si si l'élément à gauche est fini
                res1= subEval(tab1[i])
                res2= subEval(tab2[i])
                if res1 != res2:
                    final= False
                    break
            else:
                final.append([tab1[i], tab2[i]])
        if final == []: # si on est tombé que sur des terminaux égaux
            final = True
    #verbose("résultat de l'union:  %s" % final)
    return final

def splitByExpression(exp):
    return myParser("split "+exp).split("&&")

def isNumber(exp):
    res= myParser("isNumber "+exp)
    if res == "True":
        res = True
    else:
        res = False
    return res

def isList(exp):
    res = False
    try:
        if eval("isinstance(%s, list)" % (exp)):
            res = True
    except:
        pass
    return res

def isBoolean(exp):
    res= False
    if exp in ["True", "False"]:
        res = True
    return res

def isTerminal(exp):
    res= False
    if isNumber(exp) or isList(exp) or isBoolean(exp):
        res= True
    return res

def check(exp, dico):
    tab= exp.split(",")
    for t in tab:
        sub= complete(t,dico)
        res, dico = verifiable(sub,dico)
        if res == False:
           return False, dico 
    return True,dico

def verifiable(exp,dico):
    res= False
    if exp.find("->") > -1:
        #évaluation
        tab= exp.split("->")
        state= evaluate(tab[0])
        if state != False:
            newdico= union(state,tab[1])
            dico += newdico
            res = True
    else:
        #égalité
        tab= exp.split("=")
        for i in range(len(tab)):
            t[i]= myeval(t[i])
        if tab in dico:
            res= True
    return res, dico

def complete(exp, tab):
    dico= tabToDic(tab)
    sym= symbol(exp)
    #if sym == "->": # si c'est une expressison de conclusion
        #exp= exp.split(sym)[1]
    tokens= getToken(exp) #token est un tableau des différentes partie de l'expression
    for i in range(len(tokens)):
        tokens[i]= dico.get(tokens[i], tokens[i]) #On remplace si'il y a un moyen de remplacer
    if "in" in tokens:
        tokens = ['&in&' if i=='in' else i for i in tokens] # pour que le "in" ne soit pas collé aux voisins
    exp= "".join(tokens)
    return exp

def tabToDic(tab):
    dico= {}
    for t in tab:
        dico[t[0]]= t[1]
    return dico

def getToken(exp):
    tokens= myParser("token "+exp).split("&&")
    return tokens

def subEval(exp):
    res= myParser("calc "+exp)
    if res == "error":
        verbose("subEval a échoué")
        res= exp
    return res

def myParser(exp):
    parser.parse(exp)
    f = open("res.txt", "r")
    res= f.readline()
    f.close()
    if res[0] == "&":
        res= "error"
    return res
