import unittest
import clean_data
import random
import pandas as pd


# https://stackoverflow.com/questions/13605669/python-unittest-can-we-repeat-unit-test-case-execution-for-a-configurable-numbe

def repeat(times):
    def repeatHelper(f):
        def callHelper(*args):
            for i in range(0, times):
                f(*args)

        return callHelper

    return repeatHelper


def genInt():
    return random.randint(0, 1000000)


class cleanTest(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({'id_str':[ '1','2','1'],'time':["05/12/2014 18:07", "12/13/2014 18:07", "05/12/2014 18:05"],'user_lang':['en-gb','en-GB','en-AU'],'mustInt':[1,'string','ImNotInt']})

    @repeat(5)
    def test_checkInt(self):
        print("run")
        result = clean_data.checkInt(genInt())
        self.assertTrue(result)
    
    def test_checkString(self):
        string = 'String'
        result = clean_data.checkInt(string)
        self.assertFalse(result)
    
    def test_validate(self):
        date = "05/12/2014 18:07"
        result = clean_data.validate((date))
        self.assertTrue(result)
    
    def test_invalideTime(self):
        date = "12/13/2014 18:07"
        result = clean_data.validate(date)
        self.assertFalse(result)

    def test_combineEng(self):
        
        df = clean_data.combineEng(self.df)
        dfExpected = pd.DataFrame({'id_str':[ '1','2','1'],'time':["05/12/2014 18:07", "12/13/2014 18:07", "05/12/2014 18:05"],'user_lang':['en','en','en'],'mustInt':[1,'string','ImNotInt']})
        pd.testing.assert_frame_equal(df, dfExpected)

    def test_removedDuplicates(self):
        df = clean_data.removeDuplicates(self.df)
        dfExpected = pd.DataFrame({'id_str':['1','2'],'time':["05/12/2014 18:07", "12/13/2014 18:07"],'user_lang':['en-gb','en-GB'],'mustInt':[1,'string']})
        pd.testing.assert_frame_equal(df, dfExpected)
    
    def test_checkType(self):
        df = clean_data.checkType(self.df, 'mustInt')
        df['mustInt']=df['mustInt'].apply(lambda x:int(x))
        dfExpected = pd.DataFrame({'id_str':['1'],'time':["05/12/2014 18:07"],'user_lang':['en-gb'],'mustInt':[1]})
        pd.testing.assert_frame_equal(df, dfExpected)

    def test_checkDate(self):
        df = clean_data.checkDates(self.df)
        df = df.set_index('id_str')
        dfExpected = pd.DataFrame({'id_str':[ '1','1'],'time':["05/12/2014 18:07", "05/12/2014 18:05"],'user_lang':['en-gb','en-AU'],'mustInt':[1,'ImNotInt']})
        dfExpected = dfExpected.set_index('id_str')
        pd.testing.assert_frame_equal(df, dfExpected)


if __name__ =='__main__':
    unittest.main()
