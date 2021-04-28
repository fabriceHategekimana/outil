Instructions:

# Foreword:

## Installation:
Just download the project and it is ready to use.  

This project isn't complete and is still purelly written in python. You will need to install some dependency with pip:  

```bash
pip install pyvis
pip install click
pip install ply
```

you can install additional package the same way if needed.  

# Getting started
The files have just the extention ".fa" but you can also open txt files if it contains the right code.   

## Structure
The code is divided in two part:  

### 1) The rule declaration part:
As mentionned, this is the part where a user can defin his own rules.    
It has the same structure as the rule withe premises and conclution.  

### 2) The program part:
Here you can write your own program according to what you hav previousely written in the rule declaration part.    
It must begin withe a "Program{...}" and you can simply write your code.  

Minimal file content you need to have:    
```scala
Program{ 

}
```

For more example you can finde some ".fa" file in the data folder of the project.  

## Run your code
This process is a tad bit complicated but still affordable. All you need is in the file "outil.py". There are the main commandes you can do:  

### Help
You can consult the help option to get some information about how to run your code.    
```bash
python outil.py --help
```

### Run the code normally
This is the basic methode to do so.    
```bash
python outil.py [path and name of the file to run]
```

### Run the code in verbose mode
Just add a -v. Sorry the informations are in french.  
```bash
python outil.py -v [path and name of the file to run]
```
You can also si the last execution in the file "log.txt".    

### Run the code in debug mode
The debug mode is a interactiv shell that help you to see more precisely how your code run.  
```bash
python outil.py -d [path and name of the file to run]
```
There are special commandes:  

- step: execute the next step (rule selection or rule application)
- state: display the actual state of the execution (still ugly and need to be improved)
- display: show with a graph (in your browser) the execution of the rules.
- end: execute the code until the end (warning, if there is an infinit loop, it won't stop util you press ctrl+c)
- set exp: set a new expression to be executed.
- set state: set a new state to be executed.

