import os
import smsgates
import unittest2 as unittest

#class configuration_mngr(object):
#    def configure(self, obj):
#        obj.MY_PHONE_NUMBER = ""
#        obj.MY_PASSWORD = ""
#
#class TestVFGate(unittest.TestCase):
#    def test_send_with_device(self):
#        with VFGate(configuration_mngr=configuration_mngr) as gate:
#            gate.send("It worked!", VFGate.MY_PHONE_NUMBER)


class Test_Vodafone_Gate(unittest.TestCase):
    def test_get_gate_class(self):
        self.assertIs(smsgates.get_gate_class('vodafone.ie'),
                      smsgates.Vodafone_Gate)
        self.assertIs(smsgates.get_gate_class('Vodafone.Ie'),
                      smsgates.Vodafone_Gate)
        self.assertIs(smsgates.get_gate_class('VODAFONE.IE'),
                      smsgates.Vodafone_Gate)

    def test_send_with_device(self):
        with smsgates.VFGate(login=os.environ['TEST_SMS_GATES_LOGIN'],
                    password=os.environ['TEST_SMS_GATES_PASSWORD']) as gate:
            gate.send("It worked!", os.environ['TEST_SMS_GATES_PHONE_NR'])


class Test_Orange_Gate(unittest.TestCase):
    def test_get_gate_class(self):
        self.assertIs(smsgates.get_gate_class('orange.pl'),
                      smsgates.Orange_Gate)
        self.assertIs(smsgates.get_gate_class('Orange.Pl'),
                      smsgates.Orange_Gate)
        self.assertIs(smsgates.get_gate_class('ORANGE.PL'),
                      smsgates.Orange_Gate)

    def test_send_with_device(self):
        with smsgates.Orange_Gate(login=os.environ['TEST_SMS_GATES_LOGIN'],
                    password=os.environ['TEST_SMS_GATES_PASSWORD']) as gate:
            gate.send("It worked!", os.environ['TEST_SMS_GATES_PHONE_NR'])


if __name__ == '__main__':
    unittest.main()
