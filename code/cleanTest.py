import unittest
import clean_data
import random
import pandas as pd


# Copied from https://stackoverflow.com/questions/13605669/python-unittest-can-we-repeat-unit-test-case-execution-for-a-configurable-numbe

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
    # This will run before every singl test
    def setUp(self):
        self.df = pd.DataFrame({'id_str':[ '1','2','1'],'time':["05/12/2014 18:07", "12/13/2014 18:07", "05/12/2014 18:05"],'user_lang':['en-gb','en-GB','en-AU'],'mustInt':[1,'string','ImNotInt'], 'withEmpty':['1',' ',' ']})

    # Passing random int within the range of 0-1000000 into the checkInt 
    # Tests that checkInt will return true when the argument passing into it is an int
    @repeat(5)
    def test_checkInt(self):
        print("run")
        result = clean_data.checkInt(genInt())
        self.assertTrue(result)
    
    # Tests that checkInt will return flase when the argument passing into it is not an int
    def test_checkString(self):
        string = 'String'
        result = clean_data.checkInt(string)
        self.assertFalse(result)
    
    # Tests that isNotWhite will return true when the argument passing into it isn't a blank string
    def test_isNotWhite(self):
        string = "Not White Spaces"
        result = clean_data.isNotWhite(string)
        self.assertTrue(result)

    # Tests that isNotWhite will return false when the argument passing into it is a blank string
    def test_isNotWhite(self):
        string = ' '
        result = clean_data.isNotWhite(string)
        self.assertFalse(result)

    # Tests that validte will return true when the argument passing into it is in the correct date-time format
    def test_validate(self):
        date = "05/12/2014 18:07"
        result = clean_data.validate((date))
        self.assertTrue(result)
    
    # Tests that validte will return false when the argument passing into it is in the incorrect date-time format
    def test_invalideTime(self):
        date = "12/13/2014 18:07"
        result = clean_data.validate(date)
        self.assertFalse(result)

    # Tests that combineEng will converts all types of en into en
    def test_combineEng(self):
        df = clean_data.combineEng(self.df)
        dfExpected = pd.DataFrame({'id_str':[ '1','2','1'],'time':["05/12/2014 18:07", "12/13/2014 18:07", "05/12/2014 18:05"],'user_lang':['en','en','en'],'mustInt':[1,'string','ImNotInt'], 'withEmpty':['1',' ',' ']})
        
        # https://mungingdata.com/pandas/unit-testing-pandas/
        pd.testing.assert_frame_equal(df, dfExpected)

    # Tests that removeDuplicates will removed the row wwith duplicates id_str (special ID for each tweet)
    def test_removedDuplicates(self):
        df = clean_data.removeDuplicates(self.df)
        dfExpected = pd.DataFrame({'id_str':['1','2'],'time':["05/12/2014 18:07", "12/13/2014 18:07"],'user_lang':['en-gb','en-GB'],'mustInt':[1,'string'], 'withEmpty':['1',' ']})
        pd.testing.assert_frame_equal(df, dfExpected)

    # Tests that checkType will removed the rows that isn't int or empty spaces
    def test_checkType(self):
        df = clean_data.checkType(self.df, 'mustInt')
        df['mustInt']=df['mustInt'].apply(lambda x:int(x))
        dfExpected = pd.DataFrame({'id_str':['1'],'time':["05/12/2014 18:07"],'user_lang':['en-gb'],'mustInt':[1], 'withEmpty':['1']})
        pd.testing.assert_frame_equal(df, dfExpected)

    # Tests that checkDates will removed the row that contains an invalid date
    def test_checkDate(self):
        df = clean_data.checkDates(self.df)
        df = df.set_index('id_str')
        dfExpected = pd.DataFrame({'id_str':[ '1','1'],'time':["05/12/2014 18:07", "05/12/2014 18:05"],'user_lang':['en-gb','en-AU'],'mustInt':[1,'ImNotInt'], 'withEmpty':['1',' ']})
        dfExpected = dfExpected.set_index('id_str')
        pd.testing.assert_frame_equal(df, dfExpected)

    # Checks that dropColumn will drops the given column
    def test_dropColumn(self):
        df = clean_data.dropColumn(self.df,'id_str')
        dfExpected = pd.DataFrame({'time':["05/12/2014 18:07", "12/13/2014 18:07", "05/12/2014 18:05"],'user_lang':['en-gb','en-GB','en-AU'],'mustInt':[1,'string','ImNotInt'], 'withEmpty':['1',' ',' ']})    
        pd.testing.assert_frame_equal(df, dfExpected)
    
    # Checks that dropRowsWithEmptyFields will removed the empty rows in the given column
    def test_dropRowsWithEmpty(self):
        df = clean_data.dropRowsWithEmptyFields(self.df, 'withEmpty')
        df['mustInt']=df['mustInt'].apply(lambda x:int(x))
        dfExpected = pd.DataFrame({'id_str':['1'],'time':["05/12/2014 18:07"],'user_lang':['en-gb'],'mustInt':[1], 'withEmpty':['1']})
        pd.testing.assert_frame_equal(df, dfExpected)

if __name__ =='__main__':
    unittest.main()
