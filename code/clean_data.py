import math
import pandas as pd
import sys
import re
from dateutil import parser

#Removes any entries with the same ID.
def removeDuplicates(df):
    print('Duplicte IDs before: ' + str(df.id_str.duplicated().sum()))
    df = df.drop_duplicates(subset=['id_str'], keep='first')
    print('Duplicte IDs after: ' + str(df.id_str.duplicated().sum()))
    return df

#Removes any rows with empty fields that we have not allowed to be empty.
def dropRowsWithEmptyFields(df, columns):
    df = df.dropna(axis=0, how='any', subset=columns)
    return df

#Checks if input is empty or an int and returns True if a match.
def checkInt(inp):
    try:
        if(math.isnan(inp)):
            return True
    except:
        return False
    try:
        int(inp)
        return True
    except:
        return False

#Ensures contained data is an int.
def checkType(df, column_name):
    df = df[df[column_name].map(checkInt) == True]
    return df

#Check that dates match an appropriate regex.
def validate(inp):
    if (re.match("^((0[1-9])|([12]\d)|(3[01]))\/(([0][1-9])|([1][012]))\/\d\d\d\d\s(([0-1]\d)|(2[0-4])):[0-5]\d$", str(inp))):
        return True
    else:
        return False

#Validates the format of all the date-times.
def checkDates(df):
    df = df[df['time'].map(validate) == True]
    return df

#Outputs updated dataframe to a new CSV file.
def writeToCSV(df):
    print("Updating CSV...")
    df.to_csv('../data/CometLandingRefined.csv', index=False)
    print("CSV Updated!")


def combineEng(df):
    df['user_lang'].replace('en-gb', 'en', inplace=True)
    df['user_lang'].replace('en-GB', 'en', inplace=True)
    df['user_lang'].replace('en-AU', 'en', inplace=True)
    return df


def main():

    #Ensure correct usage.
    if(len(sys.argv) != 2):
        print("Incorrect Usage! One argument (CSV Filepath) only!")
        exit()

    #Read in CSV file.
    df = pd.read_csv(sys.argv[1])

    #Columns we are not allowing to be empty.
    mandatory_columns = ['id_str', 'from_user', 'text', 'created_at', 'time', 'user_lang', 'from_user_id_str', 
    'source', 'profile_image_url', 'user_followers_count', 'user_friends_count', 'status_url', 'entities_str']
    #Columns that must contain whole numbers (or be empty for those allowed).
    columns = ['id_str', 'from_user_id_str', 'user_followers_count', 'user_friends_count', 'in_reply_to_user_id_str', 'in_reply_to_status_id_str']

    print("Cleaning Data...")
    #Run Cleanup functions
    df = removeDuplicates(df)
    df = dropRowsWithEmptyFields(df, mandatory_columns)

    for cn in columns:
        df = checkType(df, cn)
    df = checkDates(df)
    #'created_at' is very similar to 'time', so lets drop it.
    df.drop('created_at', inplace=True, axis=1)
    #'geo_coordinates' is not a very helpful column - lets also drop that.
    df.drop('geo_coordinates', inplace=True, axis=1)
    df = combineEng(df)
    #End of cleanup functions.

    print("Data Cleaned!")

    writeToCSV(df)

if __name__ == "__main__":
    main()