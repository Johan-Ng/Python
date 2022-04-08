import unittest
import clean_data
import random

def repeat(times):
    def repeatHelper(f):
        def callHelper(*args):
            for i in range(0, times):
                f(*args)

        return callHelper

    return repeatHelper


def gen_int():
    return random.randint(0, 1000000)

class cleanTest(unittest.TestCase):

    @repeat(5)
    def test_checkInt(self):
        print("run")
        result = clean_data.checkInt(gen_int())
        self.assertTrue(result)
    
    def test_validate(self):
        date = "05/12/2014 18:07:14"
        result = clean_data.validate((date))
        self.assertTrue(result)
    
    def test_invalideTime(self):
        date = "12/13/2014 18:07:14"
        result = clean_data.validate(date)
        self.assertFalse(result)

if __name__ =='__main__':
    unittest.main()
