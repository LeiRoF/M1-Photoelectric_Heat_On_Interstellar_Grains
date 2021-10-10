ask.py
======

This file contain several functions that check parameters given by the user. It can not be started as a main file and all functions consist in 3 steps:

- Check if the variable given in the parameter is correct and raise an error if it's not the case
- If this variable is not defined, the function will read ``argv`` list
- If there is no corresponding ``argv``, the function will ask the parameter to the user

To be more precize, here there is the global usual structure of these functions:

.. block-code::python

    # Check if the value is correct
    def check(value)
        if <condition on value>:
            return true
        else:
            return false

    # argv and user answers are only strings, so most of value needs to be treated
    def format(value):
        return <some treatment>

    # Try to get the value from different sources
    def ask(value):

        # First source: parameter
        if value is not None:
            if check(value):
                return value
            else:
                raise ValueError("Incorrect input")

        # Second source: argv
        try:
            global n # Get the argv index
            value = argv[n]
            n += 1 # Increment argv for the next call to a ask-type function
            value = format(value)

        except IndexError:
            pass # if there is no corresponding argv, the program will ask the user

        except:
            print("[Error] Incorrect value or command syntax. Correct command syntax: <command pattern>")

        
        # Third source: user answer
        while True: #infinite loop until the value is correct
            try:
                value = input("Select the value: ")
                value = format(value)
                return value # if there is no error, the function will return the value, so the loop will stop
        
            except KeyboardInterrupt:
                endProgram() # if the user press ctrl+c, the program will stop

            except:
                print("[Error] Incorrect value")




