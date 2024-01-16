#Requires SampleMiniFat.fs
#Description: This program uses a while loop to continuously prompt the user for input like in a terminal window. Upon the user entering command,
#the program will organize the entry into the actual command and the argument for the command (if applicable). Based on the command, it will execute
#the appropriate actions: ls will display the files based on the argument, mkfile will create a file in the file system, delete will delete a file 
# from the file system, read will read in a file from the file system, and quit will exit the program.
#If an improper command is given, too many arguments are given, or not enough arguments are given (based on what the command requires), the program
#will print an error message describing the error for the user.

import os
import math
import sys

currentDirectory = "root?>"
userInput = ""
command = ""
argument = ""
inputList = []
all = []
fileLocation = []
fileSize = []
curr = []
deleted = []


with open(sys.argv[2], mode='rb') as file:
    x = 0
    i = 0
    while x < 1024:
        file.seek(2**8+x)
        if file.read(2) != b'~~':
            file.seek(2**8+x)
            all.append(file.read(5).decode())
            fileLocation.append(int.from_bytes(file.read(1), 'big'))
            fileSize.append(int.from_bytes(file.read(2), 'big'))
        x += 8
        i += 1

    for x in all:
        if x[0:1] == '~':
            deleted.append(x)
        else:
            curr.append(x)

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

    elif command == "ls":
        if argument == "all":
            print(all)
        elif argument == "curr":
            print(curr)
        elif argument == "del":
            print(deleted)
        else:
            print("argument must be provided")

    elif command == "mkfile":
        exists = False
        for x in curr:
            if x == argument:
                exists = True
        if exists != True:
            curr.append(argument)
            all.append(argument)
            #os.mkdir(argument)
        else:
            print("a directory with this name already exists")

    elif command == "delete":
        exists = False
        for x in curr:
            if x == argument:
                exists = True
                #os.rmdir(x)
                curr.remove(x)
                deleted.append(argument)
        if exists != True:
            print("file or directory does not exist and cannot be deleted")

    #file argument must give absolute or relative path if not in current directory
    #or if this file is in a folder
    elif command == "read":
        exists = False
        for x in curr:
            if x == argument:
                exists = True
                with open(sys.argv[2], mode='rb') as file:
                    fileStart = fileLocation[all.index(argument)]
                    leftToRead = fileSize[all.index(argument)]
                    clustersRead = 0
                    filePath = []
                    filePath.append(fileStart)
                    clustersNeeded = (math.ceil(leftToRead / 2**10))
                    while len(filePath) <= clustersNeeded:
                        file.seek(filePath[len(filePath)-1])
                        filePath.append (int.from_bytes(file.read(1), 'big'))

                    while leftToRead > 0:
                       file.seek(2**8 + 2**10 + filePath[clustersRead]*(2**10))
                       if leftToRead >= 2**10:
                           print(file.read(2**10))
                       else:
                           print(file.read(leftToRead))
                       leftToRead -= 2**10
                       clustersRead += 1

        if (exists != True):
            print("file not found")

    #keeps error from printing when quit is the command
    elif command == "quit":
        break

    else:
        print(command + ": command not found")