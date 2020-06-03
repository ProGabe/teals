import importlib
import json
import sys
import argparse

def get_test_definition(definition_file):
    '''
        Load the definition file for this assingment.

        It has to take the form of hw1:
            {
                Name : Assignment Name
                Functions[
                    list of functions
                ]
            }

            Function:
                {
                    "name" : actual name of function to call
                    "params" : Dictionary of params based on 
                               function parameter name and value
                    "expected_output" : Value function returns.
                }
    '''
    test_definition = None
    with open(test_def_file) as input_def:
        def_data = input_def.readlines()
        def_data = "\n".join(def_data)
        test_definition = json.loads(def_data)
    return test_definition

def load_student_module(module_name):
    '''
        Module name is a pythong file without the .py extension
        that holds the functions to be tested as defined by the 
        definition file.
    '''
    return importlib.import_module(module_name)

def parse_doc_string(assingment_doc_string):
    return_data = {"Student" : None, "Assignment" : None}

    lines = assingment_doc_string.split("\n")
    for line in lines:
        if len(line) and (':' in line):
            line = line.strip().split(':')
            for key in return_data:
                if key == line[0]:
                    return_data[key] = line[1].strip()

    return return_data

def parse_program_args(prog_args):
    '''
        Parse out optional parameters -mod and -config from any command line
        input. If none is provided, the user will be promtped for an answer. 
    '''
    parser = argparse.ArgumentParser(description='Automated Python Tester')
    parser.add_argument("-mod", required=False, type=str, default=None,  help="Student module (without .py extension)")
    parser.add_argument("-config", required=True, type=str, default=None,   help="JSON configuration file")

    return parser.parse_args(prog_args)

'''
    Get the student module name (python file without .py) and 
    the definition file to test.
'''
program_arguments = parse_program_args(sys.argv[1:])
module_name = program_arguments.mod
test_def_file = program_arguments.config 
if not module_name:
    module_name = input('Student Module: ')
if not test_def_file:
    test_def_file = input("Test Definition: ")

test_definition = get_test_definition(test_def_file)
student_lib = load_student_module(module_name)

'''
    Output some useful information
'''
print("Test Definition : ".ljust(25), test_def_file)
print("Student Module File: ".ljust(25), module_name)
print("Current Test : ".ljust(25) , test_definition['Name'])


'''
    Get the file doc string and parse it looking for student name
    and assignment name.
'''
student_info = parse_doc_string(student_lib.__doc__)

'''
    Create an array to store results in and then iterate over each 
    function definition and attempt to call it in the student module.
'''
function_tests = []
for function in test_definition["Functions"]:

    print("\nFunction Under Test : ".ljust(25) , function['name'])
    print("Test Input : ".ljust(25) , function['params'])
    print("Expected Output : ".ljust(25) , function['expected_output'])

    
    '''
        Now call it whether it takes input or not.
    '''
    student_return = None

    try:
        '''
            We can load a function from the module that was imported
            by useing getattr with the name of the function.

            We also grab the params dictionary as we can pass that directy
            into the function to run it.
        '''
        student_function = getattr(student_lib, function['name'])
        function_input = function['params']
        
        if len(function_input):
            student_return = student_function(** function_input)
        else:
            student_return = student_function()
    except Exception as ex:
        student_return = "Exception: " + str(ex)

    '''
        Print out the results
    '''
    function_tests.append(function['expected_output'] == student_return)
    print("    Student Results:" , student_return)
    print("    Pass: ", function_tests[-1])


##
## TODO : Automate grading somewhere?
##
print('\n\n', '*' * 30)
print(" Official Test: ", test_definition['Name'])
print(" Student Name: ", student_info['Student'])
print(" Student Assignment: ", student_info['Assignment'])
correct_answers = function_tests.count(True)
print(" Questions: {} Correct : {} Percentage: {} %".format( 
    len(function_tests),
    correct_answers,
    (correct_answers / len(function_tests) ) *100 )
    )
print('','*' * 30)
