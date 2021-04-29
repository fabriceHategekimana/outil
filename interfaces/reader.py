from interfaces.modules.rules import *

def evaluateProgram(state, prog):
    tab= prog.split(";;")
    if tab[len(tab)-1] == "":
        tab.pop()
    for inst in tab:
        state= evaluateInstruction(state+inst)
    print("return>", state)

def startReading(filePath, verbose=False):
    #EVALUATION DU PROGRAMME
    Program, error= importRules(filePath)
    if error == False: #execute the program if no error
        state, exp= getStateAndExp(Program) 
        evaluateProgram(state, exp)
    else:
        print("Abort file importation")
    if verbose == True:
        f= open("log.txt", "r")
        print(f.read())
        f.close()
        f= open("log.txt", "w")
        f.write("")
        f.close()

