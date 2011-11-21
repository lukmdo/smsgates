import os
from smsgates import VFGate
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


class TestVFGate(unittest.TestCase):
    def test_send_with_device(self):
        with VFGate(login=os.environ['TEST_SMS_GATES_LOGIN'], password=os.environ['TEST_SMS_GATES_PASSWORD']) as gate:
            gate.send("It worked!", os.environ['TEST_SMS_GATES_PHONE_NR'])

if __name__ == '__main__':
    unittest.main()
