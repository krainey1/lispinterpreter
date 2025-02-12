#!/usr/bin/python3
""" A lisp Intepreter (We hope) """
# Katelynn Rainey

import operator as op
import math
delims = [" ", "(", ")", "'", ","]
torf = ["T", "NIL"]

#cons function handling 

def cons(x, y):
        if(x[0] != delims[1]):
                y = y.replace(delims[1], "")
                n_str = delims[1] + x + y
                return n_str
        elif x[0] == delims[1] and y[0] == delims[1]:
                y = y.replace(delims[1], "")
                n_str = delims[1] + x + y
                return n_str
        else:
                return "invalid cons operation"

#base operations dicitionary -> used for lookup of functions to see if its user defined
ogdict = {
        "+": op.add,
        "-": op.sub,
        "*": op.mul,
        "/": lambda x, y: x / y if y != 0 else print("division by zero error, try again"),
        "car": lambda x: x.split()[0][1:] if x[0] == delims[1] else print("Only accepts lists"),
        "cdr": lambda x: " ".join(x.split()[1:]).replace(")", "") if x[0] == delims[1] else print("Only accepts lists"),
        "cons": lambda x, y: cons(x, y),
        ">": op.gt,
        "<": op.lt,
        "==": op.eq,
        "=": op.eq,
        "!=": op.ne,
        ">=": op.ge,
        "<=": op.le,
        "and": lambda x, y: True if (x == y and (x == torf[0]) and (y == torf[0])) else False,
        "or": lambda x, y: True if(x[0] == 'T' or y[0] == 'T') else False,
        "not": lambda x: False if (x[0] == 'T') else True,
        "sqrt": lambda x: math.sqrt(x),
        "pow": lambda x, y: x ** y }


#initializes/updates enviornment
def the_env():
        env = Env()
        env.update(vars(math))
        env.update({
        "+": op.add,
        "-": op.sub,
        "*": op.mul,
        "/": lambda x, y: x / y if y != 0 else print("division by zero error, try again"),
        "car": lambda x: x.split()[0][1:] if x[0] == delims[1] else print("Only accepts lists"),
        "cdr": lambda x: " ".join(x.split()[1:]).replace(")", "") if x[0] == delims[1] else print("Only accepts lists"),
        "cons": lambda x, y: cons(x, y),
        ">": op.gt,
        "<": op.lt,
        "==": op.eq,
        "=": op.eq,
        "!=": op.ne,
        ">=": op.ge,
        "<=": op.le,
        "and": lambda x, y: True if (x == y and (x == torf[0]) and (y == torf[0])) else False,
        "or": lambda x, y: True if(x[0] == 'T' or y[0] == 'T') else False,
        "not": lambda x: False if (x[0] == 'T') else True,
        "sqrt": lambda x: math.sqrt(x),
        "pow": lambda x, y: x ** y })
        return env


#class for environments -> a dictionary, with an out outer env (helps with user defined functions) 
#static scoping
class Env(dict):
    def __init__(self, parms=(), args=(), outer=None): #constructor
        self.update(zip(parms, args)) # zip returns iterable of tuples
        self.outer = outer 
    def find(self, var):
        #find -> implementation of static scoping, goes and checks each outer dictionary for a specified variable
        return self if (var in self) else self.outer.find(var)
    


genv = the_env()


#input expression gets put into a list
def exptolist(iexp):
        tokenized = []
        stoken = ''
        if iexp[0] == delims[3] and iexp[1] != delims[2]:
                tokenized.append(delims[3])
                tokenized.append(iexp[1:])
        else:
                for token in iexp:
                        if token in delims:
                                if token == delims[3]:
                                        tokenized.append(token)
                                if stoken.strip():  
                                        tokenized.append(stoken.strip())
                                stoken = ''  
                                if token != delims[0]:  
                                        tokenized.append(token)
                        else:
                                stoken += token
                if stoken.strip():  
                        tokenized.append(stoken.strip())
        return tokenized

       

#atoms
def atom(stoken):
        try:
                return int(stoken)
        except ValueError:
                try: 
                        return float(stoken)
                except ValueError:
                        return str(stoken)

#build sublists / get parantheses out of there (PARSES)
#an extra thing to handle cons arguments
def cons_build(tokenized):
        cons_list = []
        num = len(tokenized)
        #tokenized.pop(0)
        #tokenized.pop(num - 1)
        #print(tokenized)
        for ele in tokenized:
                cons_list.append(ele)
        cons_list.pop()
        new_list = ["cons"] 
        temp_str = ""
        for i in range(1, len(cons_list)):
                if cons_list[i] == "'":
                        new_list.append(temp_str)
                        temp_str = ""  
                else:
                        temp_str += cons_list[i] + " "
        new_list.append(temp_str.strip())       
        new_list = [x for x in new_list if x]
        return new_list

#build sublists / get parantheses out of there (PARSES)
def build(tokenized):
        if(len(tokenized) == 0):
                return "Expression Error"
        if(len(tokenized)) == 2 and tokenized[0] == delims[3]:
                aq = []
                aq.append(delims[3])
                aq.append(tokenized)
                return aq
        token = tokenized.pop(0)
        if token == delims[1]:
                slist = []
                while tokenized[0] != delims[2]:
                        slist.append(build(tokenized))
                tokenized.pop(0)
                return slist
        elif token == delims[2]:
                return "Unexpected )"
        elif token == delims[3]: #additional handling for quotations
                #print(tokenized)
                quoted = ""
                token = ''
                while tokenized and tokenized[0] != delims[2]:
                        token = tokenized.pop(0)
                        if(token == delims[1]):
                                quoted += delims[1]
                        if(token != delims[1] and token != delims[3]):
                                quoted += token + " "
                if(quoted[0] == delims[1]):
                        quoted = quoted[0:-1]
                        quoted += delims[2]
                return quoted.strip()
               
        else:
                if(token == "cons"):
                        return cons_build(tokenized)
                return atom(token)







#isinstance takes type or tuple as second arg

#used to construct user defined functions 
class Procedure(object):
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env
    def __call__(self, *args): 
        return evaluate(self.body, Env(self.parms, args, self.env))

strchecklist = []


#goes through the parsed expression and evaulates
def evaluate(buildparse, operationsdict=genv):
        if isinstance(buildparse, str): #variable reference and T/NIL contant literal handling
                if buildparse in torf:
                        return buildparse  
                else:
                        if buildparse in strchecklist:
                                return buildparse
                        try:
                                return operationsdict.find(buildparse)[buildparse]
                        except:
                                return "Syntax Error"
        elif not isinstance(buildparse, list): #constant literals
                return buildparse
        elif buildparse[0] == "defun":
                if(len(buildparse) != 4):
                        print('Invalid syntax: need (defun fooname (params) (body))')
                        return None
                fname = buildparse[1] #get name of function to be defined
                params = buildparse[2]
                #bodyarg = ' '.join(map(str, buildparse[3]))
                bodyarg = buildparse[3]
                nlist = ["lambda"]
                nlist.append(buildparse[2])
                nlist.append(buildparse[3])
                #print(nlist)
                #print(bodyarg)
                operationsdict[fname] = evaluate(nlist, operationsdict)
                #print(buildparse[2])
                #ofuncsdict[fname] = lambda params: evaluate(buildparse[3], operationsdict)
                return fname #returns the function name
        elif isinstance(buildparse[0], list) and (buildparse[0][0] == "cons"):
                 v = evaluate(buildparse[0], operationsdict)
                 return v
        elif buildparse[0] == "if":
                cond = buildparse[1]
                ifcond = buildparse[2]
                elsecond = buildparse[3]
                nexp = (ifcond if evaluate(cond, operationsdict) else elsecond)
                #print(type(nexp))
                return evaluate(nexp, operationsdict)
        elif buildparse[0] == "define": #handles variable defintions
                var = buildparse[1] # gets variable name for key
                strchecklist.append(buildparse[2])
                operationsdict[var] = evaluate(buildparse[2], operationsdict) #creates key/value in dictionary 
                return buildparse[1] #returns value
        elif buildparse[0] == "lambda":
                params = buildparse[1]
                body = buildparse[2]
                return Procedure(params, body, operationsdict)
        elif buildparse[0] == "set!":
                var = evaluate(buildparse[2], operationsdict)
                if(buildparse[1] in operationsdict.keys()):
                        operationsdict[buildparse[1]] = var 
                        return buildparse[1]
                else:
                        print("Var argument has not been previously defined")
        elif isinstance(buildparse, list) and buildparse[0] == delims[3]: #handles Quotations
                if isinstance(buildparse[1], list):
                        ostring = delims[0].join(buildparse[1:][0][1:])
                        return ostring
                jstring = delims[0].join(str(atom) for atom in (buildparse[1:]))
                #print(jstring)
                return  delims[1] + jstring + delims[2]
        elif isinstance(buildparse, list): #handles function calls
                if buildparse[0] in ogdict:
                        if(buildparse[0] == "car" or buildparse[0] == "cdr"):
                                if buildparse[1] not in operationsdict:
                                        strchecklist.append(buildparse[1])
                        if(buildparse[0] == "cons"):
                                if buildparse[1] not in operationsdict:
                                        strchecklist.append(buildparse[1])
                                if buildparse[2] not in operationsdict:
                                        strchecklist.append(buildparse[2])
                        v = evaluate(buildparse[0], operationsdict)
                        args = [evaluate(arg, operationsdict) for arg in buildparse[1:]]  
                        return v(*args) #unpacks args from list
                else:
                        alist = []
                        v = evaluate(buildparse[0], operationsdict)
                        for arg in buildparse[1:][0]:
                                alist.append(arg)
                        nargs = [evaluate(narg, operationsdict) for narg in alist]
                        return v(*nargs)


#the main loop -> handles input/evaluation/writing to file
def main():
        f = open("output.txt", "a+")
        while True: #main loop, stops when (quit) entered
                print("Enter a Lisp Expression")
                iexp = input()
                if(iexp) == "(quit)":
                        f.write("(quit)")
                        break
                tokenized = exptolist(iexp)
                #print(tokenized) testing
                
                buildparse = build(tokenized)
                #print(buildparse) testing
                
               
                
                #print(type(buildparse)
                
                val = evaluate(buildparse)
                #if(len(val) == 1):
               #         print(operationsdict[val])
                if(val != None):
                        if(val == True):
                                val = 'T'
                                f.write(str(val) + "\n")
                                print(val)
                        elif(val == False):
                                f.write(str(val) + "\n")
                                val = "NIL"
                                print(val)
                        else:
                                f.write(str(val) + "\n")
                                print(val)
                
                
        f.close()       

main()