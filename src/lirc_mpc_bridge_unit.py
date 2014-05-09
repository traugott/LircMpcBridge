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
    
    def testMute(self):
        self.processor.setVolume(10)
        
        self.processor.processCommand("KEY_MUTE")
        self.assertEqual(["volume", "0"], self.commands[-1][1:3])

        self.processor.processCommand("KEY_MUTE")
        self.assertEqual(["volume", "10"], self.commands[-1][1:3])
        
    def testUnknownKey(self):
        self.processor.processCommand("RJKLJGKLDJGFDJKLL")
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()