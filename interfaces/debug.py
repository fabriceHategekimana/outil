from cmd import Cmd
from interfaces.modules.compile import *
from interfaces.modules.rules import *
from interfaces.modules.network import *
import re

class Debug(Cmd):
    prompt = 'debug>'
    use_raw_input= False
    state= ""
    exp= ""
    STATIC_RULES= []
    RULES= []
    STACK= []
    ERROR= False

    def preloop(self): 
        f= open("res.txt", "r")
        path= f.readlines()[0]
        f.close()
        Program, error= importRules(path)
        if error == False:
            self.state, self.exp= getStateAndExp(Program) 
            #On ne prend que la première expression
            self.exp= self.exp.split(";;")[0]
        else:
            print("Error: rules not correctly imported")

    def do_exit(self, inp):
        return True

    def do_append(self, inp):
        tab= d.sqlQuery("select * from links;")
        print(tab)

    def do_display(self, inp):
        tab= d.sqlQuery("select * from links;")
        displayNetwork(tab)

    def do_step(self, inp):
        if self.RULES == []:
           print("rules selection")
           self.RULES= getSelection(self.state+self.exp)
           self.STATIC_RULES= self.RULES.copy()
        else:
           r= self.RULES.pop(0)
           #newExp= applyRule2(self.exp, r) 
           stateexp= evaluateInstruction(self.state+self.exp)
           print("state/exp: ", stateexp)
           if stateexp != "error": #if there is no error
               self.ERROR= False
               self.RULES= []
               if stateexp.find("<") > -1: #if it's a state
                   self.state= stateexp
               else:
                   self.exp= stateexp
           else:
               self.ERROR= True

    def do_run(self, inp):
       prog= inp.split(";;") 
       print("prog", prog)
       while(len(prog) > 0):
         self.exp= prog.pop()
         self.do_step("")
         self.do_step("")

    def do_state(self, inp):
        print("--------------------------------------")
        print("selected_rules:", self.STATIC_RULES)
        if self.RULES != []:
            print("next rule:", self.RULES[0])
        else:
            print("next rule:")
        print("expression:", self.exp)
        print("state:", self.state)
        print("--------------------------------------")

    def do_apply(self, inp):
        if isNumber(inp):
            inp= int(inp)
            if inp <= self.STATIC_RULES:
                rule= self.STATIC_RULES[inp]
            else:
                rules= "unknow"
        else:
            rule= formatRule(inp)
            tempRULES= sefl.STATIC_RULES.copy()
            tempRULES.append(rule)
            print("tempRULES: ", tempRULES)

    def do_rules(self, inp):
        r= getRules()
        print(r)

    def do_set(self, inp):
        self.RULES= []
        tab= inp.split(" ")
        if len(tab) == 2:
            d.sqlModify("delete from links;")
            self.STACK= [tab[1]]
            if tab[0] == "exp":
                self.exp= tab[1]
            if tab[0] == "state":
                self.state= tab[1]

    def do_import(self, inp):
        try:
            importRules(inp)
            if error == False:
                self.state, self.exp= getStateAndExp(Program) 
                print("%s imported!" % inp)
        except:
            print("can't find the file '%s'" % inp)

    def do_end(self, inp):
        while(True):
            self.do_step("")
            if (self.ERROR == True and self.RULES == []) or isTerminal(self.exp):
                break

    def default(self, inp):
        print("action inconnue")

    def createLink(self):
        goal= self.STACK.pop()
        subject= self.STACK.pop()
        d.sqlModify("insert into links(subject,link,goal) values ('%s','%s','%s')" % (subject, " ", goal))
        self.STACK.append(subject)
        self.STACK.append(goal)

