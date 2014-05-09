#!/usr/bin/env python
# encoding: utf-8
'''
LircMpcBridge -- Pipe irw to this script and the remote will call mpc
Parameters: -test : Print command to Sysout instead of executing it

'''
from operator import indexOf

class Executor():
    def execute(self, commands):
        "executes the commands. What executes means depends on the implementations of the subclasses"
        pass

class SystemExecutor(Executor):
    "Executes the commands as system commands (opening a subprocess)"
    def execute(self, commands):
        import subprocess
        for cmd in commands:
            subprocess.Popen(cmd, stdout=subprocess.PIPE).wait
        
class StdoutExecutor(Executor):
    "Writes the commands to stdout"
    def execute(self, commands):
        for cmd in commands:
            for i in cmd:
                print i,
            print
        
class WriteToListExecutor(Executor):
    "Adds the commands to be executed to the given list"
    
    def __init__(self, toBeAppendTo):
        "Sets the list where the commands will be added"
        self.__toBeAppendTo = toBeAppendTo
        
    def execute(self, commands):
        for cmd in commands:
            self.__toBeAppendTo.append(cmd)
        

class CommandProcessor():
    def setInitVolume(self, volume):
        self.__volume = volume;

    def processCommand(self, command):
        for key in self.__commandToFunctionMap.keys():
            if key in command:
                toExecute = self.__commandToFunctionMap.get(key,None)()
                self.__executor.execute(toExecute)
                break;
            
    def __mute(self):
        self.__mute = self.__mute == False
        return self.__createVolumeCommand()
        

    def __createVolumeCommand(self):
        if self.__mute:
            return [["/usr/bin/mpc","volume","0"]]
        return [["/usr/bin/mpc","volume",str(self.__volume)]]
        
                        
    def __volUp(self):
        self.__mute = False
        index = indexOf(self.__volumeSteps, self.__volume)+1
        if index < len(self.__volumeSteps):
            self.__volume = self.__volumeSteps[index]
            return self.__createVolumeCommand()
        return []

    def __volDown(self):
        self.__mute = False
        index = indexOf(self.__volumeSteps, self.__volume)-1
        if index >= 0:
            self.__volume = self.__volumeSteps[index]
            return self.__createVolumeCommand()
        return []

    def __init__(self, executor):
        self.__executor = executor
        self.__volume = 0;

        self.__commandToFunctionMap = {
              "KEY_VOLUMEUP": self.__volUp,
              "KEY_VOLUMEDOWN": self.__volDown,
              "KEY_MUTE": self.__mute
              }
        self.__volumeSteps = [0,5,10,15,20,30,40,50,60,70,80,90,100]
        
        self.__mute = False
    
    def setVolume(self, volume):
        "Set the volume. The value has to be an int and in __volumeSteps"
        if indexOf(self.__volumeSteps, volume):
            self.__volume = volume
    

if __name__ == "__main__":
    import sys
    test = False
    executor = SystemExecutor()
    for arg in sys.argv:
        if arg == "-test":
            executor = StdoutExecutor()

    processor = CommandProcessor(executor)            
    while True:
        command = sys.stdin.readline()
        processor.processCommand(command)
