'''
Created on 09.05.2014

@author: blicrain
'''
import unittest
import lirc_mpc_bridge


class Test(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.commands = [];
        self.processor = lirc_mpc_bridge.CommandProcessor(lirc_mpc_bridge.WriteToListExecutor(self.commands))

    def testVolume(self):
        self.processor.processCommand("xxKEY_VOLUMEUPxx")
        self.assertEqual(1, len(self.commands), "Expected one volume command");
        self.assertEqual("5", self.commands[0][2])

        self.processor.processCommand("xxKEY_VOLUMEUPxx")
        self.assertEqual("10", self.commands[-1][2])

        self.processor.processCommand("KEY_VOLUMEDOWN")
        self.assertEqual("5", self.commands[-1][2])
    
    def testStop(self):
        self.processor.processCommand("KEY_STOPCD")
        self.assertEqual(["stop"], self.commands[-1][1:])

    def testPlayThenStop(self):
        self.processor.processCommand("KEY_KP2")
        self.processor.processCommand("KEY_STOPCD")
        self.processor.processCommand("KEY_PLAYPAUSE")
        self.assertEqual(["play", "2"], self.commands[-1][1:])


    def testMute(self):
        self.processor.setVolume(10)
        
        self.processor.processCommand("KEY_MUTE")
        self.assertEqual(["volume", "0"], self.commands[-1][1:3])

        self.processor.processCommand("KEY_MUTE")
        self.assertEqual(["volume", "10"], self.commands[-1][1:3])
        
    def testKey1To9(self):
        for i in range(1,10):
            self.processor.processCommand("KEY_KP"+str(i))
            self.assertEqual(["/usr/bin/mpc","clear"], self.commands[-3])
            self.assertEqual(["/usr/bin/mpc","load", "radio"], self.commands[-2])
            self.assertEqual(["/usr/bin/mpc","play", str(i)], self.commands[-1])

        
    def testUnknownKey(self):
        self.processor.processCommand("RJKLJGKLDJGFDJKLL")
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()