import click
from interface_debug import *
from interface_reader import *
from interface_cli_grammaire import *

@click.command()
@click.option('-g', '--grammar', is_flag= True, help='(do not use) lauch the interactive interface for grammar testing.')
@click.option('-d', '--debug', is_flag=True, help='lauch the interactive interface for debuging.')
@click.option('-v', '--verbose', is_flag=True, help='display explicitely the history of the code execution.')
@click.argument("name")
def outil(name: str, debug: bool, verbose: bool, grammar: bool):
    """A CLI wrapper for the API of Public APIs."""
    if debug == True and grammar == False:
        f= open("res.txt", "w")
        f.write(name)
        f.close()
        Debug().cmdloop()
    elif debug == False and grammar == True:
        CliGrammaire().cmdloop()
    else:
        startReading(name, verbose)

if __name__ == '__main__':
    outil(prog_name='outil')
