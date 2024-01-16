#Description: This program uses a while loop to continuously prompt the user for input like in a terminal window. Upon the user entering command,
#the program will organize the entry into the actual command and the argument for the command (if applicable). Based on the command, it will execute
#the appropriate actions: ls will display the files based on the argument, mkfile will create a file in the file system, delete will delete a file 
# from the file system, read will read in a file from the file system (including deleted files), and quit will exit the program.
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
rootEntryLocation = []
fileLocation = []
fileSize = []
curr = []
deleted = []

if (sys.argv[1] == "-new"):
    fileSystem = open(sys.argv[2], 'wb')
    for x in range (0, 256 + 256 * 1024):
        fileSystem.write(b'\x00')
    fileSystem.seek(0)
    fileSystem.write(b'\xff')
    fileSystem.seek(255)
    fileSystem.write(b'\xff')
    fileSystem.seek(256)
    x = 0
    while x < 1024:
        fileSystem.seek(256 + x)
        fileSystem.write(b'\x7e\x7e\x7e\x7e\x7e')
        x = x+8

with open(sys.argv[2], mode='rb') as fileSystem:
    x = 0
    i = 0
    while x < 1024:
        fileSystem.seek(2**8+x)
        if fileSystem.read(2) != b'~~':
            fileSystem.seek(2**8+x)
            all.append(fileSystem.read(5).decode())
            fileLocation.append(int.from_bytes(fileSystem.read(1), 'big'))
            fileSize.append(int.from_bytes(fileSystem.read(2), 'big'))
            rootEntryLocation.append(2**8+x)
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
        fileName = argument.split("/")[-1]
        for x in curr:
            if x == fileName[0:5]:
                exists = True
        if exists != True:
            size = 0
            hasSpace = True
            if os.path.exists(argument):
                size = os.path.getsize(argument)
                clustersNeeded = (math.ceil(size / 2**10))
                filePath = []
                rootEntry = False
                with open(sys.argv[2], mode='r+b') as fileSystem:
                    for x in range (1, 255):
                        if (len(filePath) < clustersNeeded):
                        #finds first clustersNeeded empty entries in FAT
                            fileSystem.seek(x)
                            if (int.from_bytes(fileSystem.read(1), 'big') == 0):
                                filePath.append (x)
                    if len(filePath) < clustersNeeded:
                        hasSpace = False
                        print("not enough space to write this file")
                if (hasSpace):
                    curr.append(fileName[0:5])
                    all.append(fileName[0:5])
                    fileSize.append(size)
                    fileLocation.append(filePath[0])
                    filePath.append(int.from_bytes(b'\xff', 'big'))
                    with open(sys.argv[2], mode='r+b') as fileSystem:
                        for x in range (0, len(filePath)-1):
                            #writes filePath to FAT
                            fileSystem.seek(filePath[x])
                            fileSystem.write(filePath[x+1].to_bytes(1, 'big'))
                        x = 0
                        while x < 1024:
                            #finds first empty root directory entry
                            fileSystem.seek(2**8+x)
                            if fileSystem.read(2) == b'~~':
                                fileSystem.seek(2**8+x)
                                fileSystem.write((fileName[0:5]).encode("utf-8"))
                                fileSystem.write(filePath[0].to_bytes(1, 'big'))
                                fileSystem.write(size.to_bytes(2, 'big'))
                                rootEntry = True
                                rootEntryLocation.append(2**8+x)
                            x += 8

                        # the below doesn't account for data stored in the arrays
                        # if (rootEntry == False):
                        #     while x < 1024:
                        #         #finds first root directory deleted-file-entry to overwrite with new entry
                        #         fileSystem.seek(2**8+x)
                        #         print ("test3")
                        #         if fileSystem.read(1) == b'~':
                        #             fileSystem.seek(2**8+x)
                        #             fileSystem.write((fileName[0:5]).encode("utf-8"))
                        #             fileSystem.write(filePath[0].to_bytes(1, 'big'))
                        #             fileSystem.write(size.to_bytes(2, 'big'))
                        #             rootEntry = True
                        #             break
                        #         x += 8
                        # print (rootEntry)
                        
                        with open(argument, mode = 'rb') as readFile:
                            leftToRead = size
                            clustersRead = 0
                            while leftToRead > 0:
                                fileSystem.seek(2**8 + 2**10 + filePath[clustersRead]*(2**10))
                                if leftToRead >= 2**10:
                                    fileSystem.write(readFile.read(2**10))
                                else:
                                    fileSystem.write(readFile.read(leftToRead))
                                leftToRead -= 2**10
                                clustersRead += 1
            else:
                print("cannot access to write this file")
        else:
            print("a file with this name already exists")

    elif command == "delete":
        exists = False
        for x in curr:
            if x == argument:
                newName = "~" + argument[1:5]
                exists = True
                with open(sys.argv[2], mode='r+b') as fileSystem:
                        fileStart = fileLocation[all.index(argument)]
                        leftToRead = fileSize[all.index(argument)]
                        rootIndex = rootEntryLocation[all.index(argument)]
                        filePath = []
                        filePath.append(fileStart)
                        clustersNeeded = (math.ceil(leftToRead / 2**10))
                        while len(filePath) <= clustersNeeded:
                            #builds file path
                            fileSystem.seek(filePath[len(filePath)-1])
                            filePath.append (int.from_bytes(fileSystem.read(1), 'big'))
                        for x in range (0, len(filePath)-1):
                            fileSystem.seek(filePath[x])
                            fileSystem.write(b'\00')
                        fileSystem.seek(rootIndex)
                        fileSystem.write(b'~')
                curr.remove(argument)
                deleted.append(newName)
                for x in all:
                    if x == argument:
                        all[all.index(argument)] = newName

        if exists != True:
            print("file or directory does not exist and cannot be deleted")

    elif command == "read":
        exists = False
        for x in curr:
            if x == argument:
                exists = True
                with open(sys.argv[2], mode='rb') as fileSystem:
                    fileStart = fileLocation[all.index(argument)]
                    leftToRead = fileSize[all.index(argument)]
                    clustersRead = 0
                    filePath = []
                    filePath.append(fileStart)
                    clustersNeeded = (math.ceil(leftToRead / 2**10))
                    while len(filePath) <= clustersNeeded:
                        #builds file path
                        fileSystem.seek(filePath[len(filePath)-1])
                        filePath.append (int.from_bytes(fileSystem.read(1), 'big'))

                    while leftToRead > 0:
                       fileSystem.seek(2**8 + 2**10 + filePath[clustersRead]*(2**10))
                       if leftToRead >= 2**10:
                           print(fileSystem.read(2**10))
                       else:
                           print(fileSystem.read(leftToRead))
                       leftToRead -= 2**10
                       clustersRead += 1
        for x in deleted:
            if x == argument:
                #reads needed size from starting cluster, not necessarily the correct path
                exists = True
                with open(sys.argv[2], mode='rb') as fileSystem:
                    fileStart = fileLocation[all.index(argument)]
                    leftToRead = fileSize[all.index(argument)]
                    clustersNeeded = (math.ceil(leftToRead / 2**10))
                    filePath = []
                    filePath.append(fileStart)
                    for x in range (1, 255):
                        if (len(filePath) <= clustersNeeded):
                        #finds first clustersNeeded empty entries in FAT
                            fileSystem.seek(x)
                            if (int.from_bytes(fileSystem.read(1), 'big') == 0):
                                filePath.append (x)
                    for x in filePath:
                        fileSystem.seek(2**8 + 2**10 + filePath[x]*(2**10))
                        if leftToRead >= 2**10:
                           print(fileSystem.read(2**10))
                           leftToRead = leftToRead - 2**10
                        else:
                           print(fileSystem.read(leftToRead))
        if (exists != True):
            print("file not found")

    #keeps error from printing when quit is the command
    elif command == "quit":
        break

    else:
        print(command + ": command not found")