import ply.lex as lex
import ply.yacc as yacc
import sys

            #_ _   _                    _   _      
  #__ _ _ __(_) |_| |__  _ __ ___   ___| |_(_) ___ 
 #/ _` | '__| | __| '_ \| '_ ` _ \ / _ \ __| |/ __|
#| (_| | |  | | |_| | | | | | | | |  __/ |_| | (__ 
 #\__,_|_|  |_|\__|_| |_|_| |_| |_|\___|\__|_|\___|
                                                  #
  #__                  _   _                 
 #/ _|_   _ _ __   ___| |_(_) ___  _ __  ___ 
#| |_| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
#|  _| |_| | | | | (__| |_| | (_) | | | \__ \
#|_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
                                            
function_dict= {"add": "%s+%s", "sub":"%s-%s", "mul":"%s*%s", "div":"%s/%s", "concat":"concat(%s,%s)", "set":"set(%s,%s,%s)", "get": "get(%s,%s)", "insert":"insert(%s,%s)", "append":"append(%s,%s)", "remove":"remove(%s,%s)", "removeLast":"removeLast(%s)", "pop":"%s.pop()", "print":"display(%s)", "len":"len(%s)"}


def get(l,i):
    res= l[i]
    if isinstance(res,str):
        res= "'"+res+"'"
    return res

def display(a):
    print(a)
    return a

def removeLast(l):
    l.pop()
    return l

def remove(l, p):
    del l[p]
    return l

def append(gauche, droite):
    if not isinstance(droite, list) and isinstance(gauche, list):
        gauche.append(droite)
    else:
        gauche= None
    return gauche

def insert(gauche, droite):
    if not isinstance(gauche, list) and isinstance(droite, list):
        droite.insert(0,gauche)
    else:
        droite= None
    return droite

def concat(gauche, droite):
    if not isinstance(gauche, list):
        gauche= [gauche]
    if not isinstance(droite, list):
        droite= [droite]
    return gauche+droite

def set(tab, index, value):
    tab[index]= value
    return tab

def func(f,i):
    res=""
    try:
        res= str(eval(f%i))
    except:
        res= "error"
    return res

def write(content):
    f = open("res.txt", "w")
    f.write(content)
    f.close()


# _                       
#| |    _____  _____ _ __ 
#| |   / _ \ \/ / _ \ '__|
#| |__|  __/>  <  __/ |   
#|_____\___/_/\_\___|_|   

reserved = {
        "in" : "IN",
        "calc" : "CALC",
        "check" : "CHECK",
        "split" : "SPLIT",
        "isList" : "ISLIST",
        "isNumber" : "ISNUMBER",
        "isString" : "ISSTRING",
        "token" : "TOKEN",
        "state" : "STATE",
        "True" : "TRUE",
        "False" : "FALSE"
        }

tokens = [
    'NUM',
    'STRING',
    'OP',
    'CP',
    'OSB',
    'CSB',
    'COMA',
    'SEMICOLON',
    'EQUAL',
    'INF',
    'SUP',
    'MINUS',
    'VAR',
    'NAME',
    'EXC'
        ]+list(reserved.values())

t_OP= r'\('
t_CP= r'\)'
t_OSB= r'\['
t_CSB= r'\]'
t_COMA= r'\,'
t_SEMICOLON= r'\;'
t_INF= r'\<'
t_SUP= r'\>'
t_MINUS= r'\-'
t_EQUAL= r'\='
t_EXC= r'\!'

t_ignore = r' '

def t_NUM(t):
    r'-?\d+(\.\d+)?'
    t.value = str(t.value)
    return t

def t_NAME(t):
    r'[a-z_][a-zA-Z_0-9]+'
    t.type = reserved.get(t.value,'NAME')
    return t

def t_VAR(t):
    r'[A-Z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'VAR')
    return t

def t_STRING(t):
    r'("[^"\n]*"|\'[^\'\n]*\')'
    return t

def t_error(t):
    t.lexer.skip(1)

lexer= lex.lex()

#----------------------------------

#____                          
#|  _ \ __ _ _ __ ___  ___ _ __ 
#| |_) / _` | '__/ __|/ _ \ '__|
#|  __/ (_| | |  \__ \  __/ |   
#|_|   \__,_|_|  |___/\___|_|   

def p_start(p):
    '''
    start : CALC calc
          | CHECK check
          | SPLIT split
          | TOKEN token
          | ISNUMBER isnumber
          | ISSTRING isstring
          | STATE state
    '''
    p[0]= "okay"

def p_lang(p):
    '''
    lang : premises MINUS MINUS conclusion
         | MINUS MINUS conclusion
    '''
    res= "".join(p[1:])
    write(res)
    p[0]= res

def p_premises(p):
    '''
    premises : statement
    '''
    p[0]= p[1]

def p_statement1(p):
    '''
    statement : statement COMA statement
    '''
    res= p[1]+";"+p[3]
    p[0]= res

def p_statement2(p):
    '''
    statement : exp symb term
              | exp symb VAR
    '''
    res= "".join(p[1:])
    p[0]= res

def p_statement3(p):
    '''
    statement : exp IN NAME
    '''
    res= p[1]+"&in&"+p[3]
    p[0]= res

def p_exp1(p):
    '''
    exp : exp COMA exp
        | exp SEMICOLON exp
    '''
    res= "".join(p[1:])
    p[0]= res

def p_exp2(p):
    '''
    exp : NAME OP exp CP
    '''
    res= "".join(p[1:])
    p[0]= res

def p_exp3(p):
    '''
    exp : term
        | VAR
    '''
    res= "".join(p[1:])
    p[0]= res
    
def p_term(p):
    '''
    term : NUM
        | STRING
        | boolean
        | list
    '''
    res= "".join(p[1:])
    p[0]= res

def p_list1(p):
    '''
    list : OSB exp CSB
         | INF exp SUP
    '''
    res= "".join(p[1:])
    p[0]= res

def p_list2(p):
    '''
    list : OSB CSB
    '''
    res= "".join(p[1:])
    p[0]= res

def p_symb(p):
    '''
    symb : EQUAL EQUAL
         | EXC EQUAL
         | INF EQUAL
         | SUP EQUAL
         | INF
         | SUP
         | MINUS SUP
    '''
    res= "".join(p[1:])
    p[0]= res

def p_conclusion1(p):
    '''
    conclusion : exp MINUS SUP exp
    '''
    res= "".join(p[1:])
    p[0]= res

def p_conclusion2(p):
    '''
    conclusion : list ins_exp MINUS SUP list
    '''
    res= "".join(p[1:])
    p[0]= res

def p_ins_exp(p):
    '''
    ins_exp : NAME
            | exp
    '''
    res= "".join(p[1:])
    p[0]= res

def p_boolean(p):
    '''
    boolean : TRUE
            | FALSE
    '''
    res= "".join(p[1:])
    p[0]= res

#      _               _    
#  ___| |__   ___  ___| | __
# / __| '_ \ / _ \/ __| |/ /
#| (__| | | |  __/ (__|   < 
# \___|_| |_|\___|\___|_|\_\
                           
def p_check(p):
    '''
    check : lang
    '''
    write(p[1])
    p[0]= "okay"

#           _ _ _   
# ___ _ __ | (_) |_ 
#/ __| '_ \| | | __|
#\__ \ |_) | | | |_ 
#|___/ .__/|_|_|\__|
#    |_|            

def p_split(p):
    '''
    split : s_exp
    '''
    write(p[1])
    p[0]= "okay"

def p_s_exp1(p):
    '''
    s_exp : s_exp COMA s_exp
          | s_exp SEMICOLON s_exp
    '''
    res= p[1]+"&&"+p[3]
    p[0]= res

def p_s_exp2(p):
    '''
    s_exp : NAME OP exp CP
    '''
    res= "".join(p[1:])
    p[0]= res

def p_s_exp3(p):
    '''
    s_exp : term
          | VAR
    '''
    res= "".join(p[1:])
    p[0]= res

 #_        _              
#| |_ ___ | | _____ _ __  
#| __/ _ \| |/ / _ \ '_ \ 
#| || (_) |   <  __/ | | |
 #\__\___/|_|\_\___|_| |_|
                         
#token
def p_token(p):
    '''
    token : t_exp
          | t_list
          | t_statement
          | t_state_ins
    '''
    write(p[1])

def p_t_exp1(p):
    '''
    t_exp : t_exp COMA t_exp
          | t_exp SEMICOLON t_exp
    '''
    res= "&&".join(p[1:])
    p[0]= res

def p_t_exp2(p):
    '''
    t_exp : NAME OP t_exp CP
    '''
    res= "&&".join(p[1:])
    p[0]= res

def p_t_exp3(p):
    '''
    t_exp : t_term
          | VAR
    '''
    res= "".join(p[1:])
    p[0]= res

def p_t_term(p):
    '''
    t_term : NUM
           | boolean
           | t_list
           | STRING
    '''
    res= "".join(p[1:])
    p[0]= res

def p_t_list1(p):
    '''
    t_list : OSB t_exp CSB
           | INF t_exp SUP
    '''
    res= "&&".join(p[1:])
    p[0]= res

def p_t_list2(p):
    '''
    t_list : OSB CSB
           | INF SUP
    '''
    res= "&&".join(p[1:])
    p[0]= res

def p_t_statement1(p):
    '''
    t_statement : t_statement COMA t_statement
    '''
    res= "&&".join(p[1:])
    p[0]= res

def p_t_statement2(p):
    '''
    t_statement : t_exp symb term
                | t_exp symb VAR
    '''
    res= "&&".join(p[1:])
    p[0]= res

def p_t_statement3(p):
    '''
    t_statement : t_exp IN NAME
    '''
    res= p[1]+"&&&in&&&"+p[3]
    p[0]= res

def p_t_state_ins(p):
    '''
    t_state_ins : t_list t_ins_exp
    '''
    res= "&&".join(p[1:])
    p[0]= res

def p_t_ins_exp(p):
    '''
    t_ins_exp : t_ins
              | t_exp
    '''
    res= "".join(p[1:])
    p[0]= res

def p_t_ins(p):
    '''
    t_ins : NAME
    '''
    res= "".join(p[1:])
    p[0]= res

 #_                           _               
#(_)___ _ __  _   _ _ __ ___ | |__   ___ _ __ 
#| / __| '_ \| | | | '_ ` _ \| '_ \ / _ \ '__|
#| \__ \ | | | |_| | | | | | | |_) |  __/ |   
#|_|___/_| |_|\__,_|_| |_| |_|_.__/ \___|_|   
                                             
#isnumber

def p_isnumber(p):
    '''
    isnumber : NUM
    '''
    write("True")
    p[0]= "okay"

# _         _        _             
#(_)___ ___| |_ _ __(_)_ __   __ _ 
#| / __/ __| __| '__| | '_ \ / _` |
#| \__ \__ \ |_| |  | | | | | (_| |
#|_|___/___/\__|_|  |_|_| |_|\__, |
#                            |___/ 

#isstring

def p_isstring(p):
    '''
    isstring : STRING
    '''
    write("True")
    p[0]= "okay"

           #_      
  #___ __ _| | ___ 
 #/ __/ _` | |/ __|
#| (_| (_| | | (__ 
 #\___\__,_|_|\___|
                  
#calc

def p_calc(p):
    '''
    calc : c_exp
    '''
    write(str(p[1]))
    p[0]= "okay"
    
def p_calc2(p):
    '''
    calc : c_condition
    '''
    write(str(eval(p[1])))
    p[0]= "calc"

def p_condition(p):
    '''
    c_condition : c_exp comparator c_exp
    '''
    p[0] = " ".join(p[1:])

def p_comparator(p):
    '''
    comparator : EQUAL EQUAL
               | EXC EQUAL
               | SUP
               | SUP EQUAL
               | INF
               | INF EQUAL
    '''
    p[0]= "".join(p[1:])

def p_exp_operator(p):
    '''
    c_exp : NAME OP c_exp CP
    '''
    mt= tuple(p[3].split(";"))
    p[0] = func(function_dict.get(p[1], None), mt)

def p_exp_more(p):
    '''
    c_exp : c_exp COMA c_exp
          | c_exp SEMICOLON c_exp
    '''
    p[0] = p[1]+";"+p[3]

def p_exp_int(p):
    '''
    c_exp : NUM
          | boolean
          | STRING
    '''
    p[0] = str(p[1])

def p_exp_list(p):
    '''
    c_exp : list
    '''
    p[0] = str(p[1])

def p_exp_list1(p):
    '''
    c_list : OSB c_morelist CSB
    '''
    p[0] = str("["+p[2]+"]")

def p_exp_list2(p):
    '''
    c_morelist : NUM COMA c_morelist
               | NUM SEMICOLON c_morelist
    '''
    p[0] = str(p[1]+","+p[3])

def p_exp_list3(p):
    '''
    c_morelist : NUM
    '''
    p[0] = str(p[1])

def p_exp_list4(p):
    '''
    c_list : OSB CSB
    '''
    p[0] = "[]"

def p_exp_list5(p):
    '''
    c_list : INF c_morelist SUP
    '''
    p[0] = str("["+p[2]+"]")

     #_        _       
 #___| |_ __ _| |_ ___ 
#/ __| __/ _` | __/ _ \
#\__ \ || (_| | ||  __/
#|___/\__\__,_|\__\___|
                      
#state
def p_state(p):
    '''
    state : st_list st_ins_exp
    '''
    res= p[1]+"&&"+p[2]
    write(res.replace("&&,&&","&&"))
    p[0] = "state"

def p_st_ins_exp1(p):
    '''
    st_ins_exp : st_ins
    '''
    p[0]= ""

def p_st_ins_exp2(p):
    '''
    st_ins_exp : st_exp
    '''
    res= p[1]
    p[0]= res

def p_st_ins(p):
    '''
    st_ins : NAME
    '''
    res= p[1]
    p[0]= res

def p_st_exp(p):
    '''
    st_exp : NAME OP t_exp CP
    '''
    p[0]= p[3]

#def p_st_state(p):
    #'''
    #st_state : st_list
    #'''
    #p[0] = p[1]

def p_st_list(p):
    '''
    st_list : OSB s_exp CSB
            | INF s_exp SUP
    '''
    res= p[2]
    p[0]= res

# error

def p_error(p):
    if p:
        tok = parser.token()
        if tok:
            write("&Error near "+p.value+" "+tok.value)
        else:
            write("&Error near "+p.value)
    else:
        write("&Syntax error at EOF")

parser= yacc.yacc(start='start')
