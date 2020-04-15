'''
    Abstraction over data/drivers.csv

    Functionlity not complete, enough to get driver history.
'''

import os,sys,inspect

if __name__ == '__main__':
    # Fix path so we can import readers/base
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    base_directory = os.path.dirname(currentdir)
    os.chdir(base_directory)
    sys.path.insert(0,base_directory)

from custom.Driver import *
from custom.Races import *
from custom.Results import *
from custom.Status import *
from custom.Constructor import *
from app.utils.menuutils import MenuUtils
from app.functions.interface import IFunction
from app.functions.dummy import DummyFunction
from app.functions.driver_stats import DriverStats
from app.functions.driver_search import DriverSearch

f1_datasets = {
    IFunction.DRIVER_DATA : DriverDataFile() ,
    IFunction.RACE_DATA : RacesDataFile(),
    IFunction.RESULTS_DATA : ResultsDataFile(),
    IFunction.STATUS_DATA : StatusDataFile(),
    IFunction.CONSTRUCTOR_DATA : ConstructorsDataFile()
}

def help():
    '''
        Top level help function
    '''
    MenuUtils.display_menu_help(app_functions)

def clear():
    '''
        Clear the screen
    '''
    os.system('cls')

def my_name():
    '''
        Who knows the reference?
    '''
    print("Heisenberg")


'''
    Menu selections with functionality
'''
app_functions = {
    "get" : {
        "driver" : {
            "stats" : DriverStats(f1_datasets)
        },
        "constructor" : {
            "stats" : DummyFunction(f1_datasets)
        }
    },
    "list" : {
        "drivers" : DriverSearch(f1_datasets),
        "constructors" : DummyFunction(f1_datasets),
        "races" : DummyFunction(f1_datasets)
    },
    "say" : {
        "my" : {
            # Hahahahahahaha
            "name" : my_name
        }
    },
    "clear" : clear,
    "help" : help,
    "quit" : quit
}

'''
    Application loop
'''
while True:   
    user_input = input("F1 : > ")
    inputs = user_input.split(' ')

    if len(inputs) > 0 and inputs[0] in app_functions.keys():
        current_action = app_functions
        last_command_index = 0

        for next_input in inputs:
        
            next_input = next_input.strip()
            if len(next_input) == 0 :
                continue

            last_command_index += 1
            '''
                Note that on an invalid command, a high level function, or 
                an instance of IFunction, we want to break the loop once
                we execute that if/elif segment as there are no more items 
                to parse. 
            '''
            if next_input not in current_action.keys():
                print("Invalid Command : ", " ".join(inputs))
                MenuUtils.display_menu_help(app_functions)
                break
            elif callable(current_action[next_input]):
                # Top level functions, typically quit and help
                current_action[next_input]()
                break
            elif isinstance(current_action[next_input], IFunction):
                # IFunction instance
                current_action[next_input].execute(inputs[last_command_index:])
                break
            else:
                current_action = current_action[next_input]
    else:
        print("Invalid Command : ", " ".join(inputs))
        display_menu_help(menu_options, None)
