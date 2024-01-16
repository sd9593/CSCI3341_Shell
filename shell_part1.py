#Description: This program uses a while loop to continuously prompt the user for input like in a terminal window. Upon the user entering command,
#the program will organize the entry into the actual command and the argument for the command (if applicable). Based on the command, it will execute
#the appropriate actions: pwd will print current directory, cd will navigate to a new directory (simulated), ls will display the files and directories
#based on the argument, mkdir will create a folder in the current directory (wherever the program is), delete will delete a folder from the current 
#directory (wherever the program is), read will read in a file from the current directory (wherever the program is), and quit will exit the program.
#If an improper command is given, too many arguments are given, or not enough arguments are given (based on what the command requires), the program
#will print an error message describing the error for the user.

import os

currentDirectory = "root?>"
userInput = ""
command = ""
argument = ""
inputList = []
directories = []
deletedDirectories = []
files = []
deletedFiles = []

#loops until user quits: takes in their command, performing the relevant action or 
#notifying of failure to do so
while userInput != 'quit':

    #solves error of previous data being stored
    argument = ""
    command = ""

    userInput = input(currentDirectory)
    inputList = userInput.split()
    command = inputList[0]
    if len(inputList) > 1:
        argument = inputList[1]
        
    if len(inputList) > 2:
        print("too many arguments provided")

    elif command == "pwd":
        print (currentDirectory)

    elif command == "cd":
        if argument == "":
            print("argument must be provided")
        else:
            currentDirectory = "root" + argument +"?>"

    elif command == "ls":
        if argument == "all":
            print("directories: ", directories)
            print("deleted directories: ", deletedDirectories)
            print("files: ", files)
            print("deleted files: ", deletedFiles)
        elif argument == "curr":
            print("directories: ", directories)
            print("files: ", files)
        elif argument == "del":
            print("deleted directories: ", deletedDirectories)
            print("deleted files: ", deletedFiles)
        else:
            print("argument must be provided")

    elif command == "mkdir":
        exists = False
        for x in directories:
            if x == argument:
                exists = True
        for x in files:
            if x == argument:
                exists = True
        if exists != True:
            directories.append(argument)
            os.mkdir(argument)
        else:
            print("a directory with this name already exists")

    elif command == "delete":
        exists = False
        for x in directories:
            if x == argument:
                exists = True
                os.rmdir(x)
                directories.remove(x)
                deletedDirectories.append(argument)
        for x in files:
            if x == argument:
                exists = True
                os.rmdir(x)
                files.remove(x)
                deletedFiles[len(deletedFiles)] = argument
        if exists != True:
            print("file or directory does not exist and cannot be deleted")

    #file argument must give absolute or relative path if not in current directory
    #or if this file is in a folder
    elif command == "read":
        if os.path.exists(argument):
            f = open(argument, "r")
            lines = f.read()
            print(lines)
            f.close()
        else:
            print("file not found")

    #keeps error from printing when quit is the command
    elif command == "quit":
        break

    else:
        print(command + ": command not found")