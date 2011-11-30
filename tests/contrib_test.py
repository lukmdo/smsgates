import os
import smsgates.contrib
import unittest2 as unittest


class VodafoneGateTest(unittest.TestCase):
    def test_get_gate_class(self):
        gate_factory = smsgates.contrib.GateFactory()
        self.assertIs(gate_factory.get_class('vodafone.ie'),
                      smsgates.contrib.VodafoneGate)
        self.assertIs(gate_factory.get_class('Vodafone.Ie'),
                      smsgates.contrib.VodafoneGate)
        self.assertIs(gate_factory.get_class('VODAFONE.IE'),
                      smsgates.contrib.VodafoneGate)

#    def test_send_with_device(self):
#        with smsgates.contrib.VodafoneGate(
#            login=os.environ['TEST_SMS_GATES_LOGIN'],
#            password=os.environ['TEST_SMS_GATES_PASSWORD']) as gate:
#            gate.send("It worked!", os.environ['TEST_SMS_GATES_PHONE_NR'])


class OrangeGateTest(unittest.TestCase):
    def test_get_gate_class(self):
        gate_factory = smsgates.contrib.GateFactory()
        self.assertIs(gate_factory.get_class('orange.pl'),
                      smsgates.contrib.OrangeGate)
        self.assertIs(gate_factory.get_class('Orange.Pl'),
                      smsgates.contrib.OrangeGate)
        self.assertIs(gate_factory.get_class('ORANGE.PL'),
                      smsgates.contrib.OrangeGate)

#    def test_send_with_device(self):
#        with smsgates.Orange_Gate(
#            login=os.environ['TEST_SMS_GATES_LOGIN'],
#            password=os.environ['TEST_SMS_GATES_PASSWORD']) as gate:
#            gate.send("It worked!", os.environ['TEST_SMS_GATES_PHONE_NR'])


if __name__ == '__main__':
    unittest.main()
