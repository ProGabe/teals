'''
    Class that provides the ability to show a menu. A menu is comprised
    of a dictionary with string keys (used to make up a command) with end
    nodes either being an IFunction instance or an actual function 
    (callable(fn) == True)

    Commands are printed out, in order found in the application dictionary
    in first found order. 

    Additionally, IFunction instances will also have the accepted argument
    list printed out with it. 

    The application menu is comprised of a dictionary that
    1. Has strings as keys and is organized to define the commands that a user will enter to perform actions in your program. 
    2. Has node values that are either:
        - An IFunction implementation. These can and do accept additional arguments to define the function execution. 
        - A standard python function. These cannot accept any additional arguments. 

    This menu structure can be re-used in any application you wish as the implementation of it is separated, through code, from any specific Forumula One activity. 

    A menu would be described in your code as follows:

    app_functions = {
        "get" : {
            "stats" : {
                "constructor" : DummyFunction(dataset),
                "driver" : DummyFunction(dataset)
            }
        },
        "quit" : quit
    }
'''
from multi_command_utils.interface import IFunction

class MenuUtils:
    MENU_TITLE = "F1 App"
    def __init__(self):
        pass

    @staticmethod
    def _menu_recurse(dictionary, command_list):
        '''
            This function is a recursive funciton if a dictionary
            contains a dictionary called by display_menu_help
        '''
        for sub_command in dictionary:
            '''
                If the next item is a 
                    dictionary - recurse
                    IFunction - print with acceptable arguments list
                    callable() - Standard function, print path to it 
                                 but no arg are not supported

                    Both IFunction and callable() require us to add the 
                    sub command to commands_list to print, then remove it
                    as it was an end node (cannot be further iterated.)
            '''
            action_taken = False
            if isinstance(dictionary[sub_command], dict):
                command_list.append(sub_command)
                MenuUtils._menu_recurse(dictionary[sub_command], command_list)
                action_taken = True
            elif isinstance(dictionary[sub_command], IFunction):
                command_list.append(sub_command)
                print("%s : %s" % (" ".join(command_list).ljust(21), dictionary[sub_command].get_arguments()) )
                action_taken = True
            elif callable(dictionary[sub_command]):
                command_list.append(sub_command)
                print("%s :" % (" ".join(command_list).ljust(21)) )
                action_taken = True

            if action_taken:
                command_list = command_list[:command_list.index(sub_command)]
    
    @staticmethod
    def display_menu_help(menu_dictionary, args = None):
        '''
            This function starts the process of iterating over the 
            dictionary menu. A dictionary can only contain 
                1. Keys that identify another dictionary
                2. Keys that identify actual functions.
        '''
        print("{}:".format(MenuUtils.MENU_TITLE))
        print("%s" % ("-".ljust(35,'-') ))
        print("%s | %s" % ("Command".ljust(21), "Arguments") )
        print("%s" % ("-".ljust(35,'-') ))

        # If args is a string, this was an incomplete call
        if isinstance(args, str):
            print("*** Incomplete Command - ", args, "*** type help")

        for command in menu_dictionary.keys():
            '''
                If the next item is a 
                    dictionary - recurse
                    IFunction - print with acceptable arguments list
                    callable() - Standard function, print path to it 
                                 but no arg are not supported

            '''
            if isinstance(menu_dictionary[command], dict):
                MenuUtils._menu_recurse(menu_dictionary[command], [command])
            elif isinstance(menu_dictionary[command], IFunction):
                print("%s : %s" % (command.ljust(21), menu_dictionary[command].get_arguments()) )
            elif callable(menu_dictionary[command]):
                print("%s :" % (command.ljust(21)) )
        print('')
