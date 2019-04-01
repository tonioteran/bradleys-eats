#!/usr/bin/python3

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

def gsheet2df(list_of_hashes):
    """
    Parse all gsheet data into a pandas DataFrame
    input: list_of_hashes, obtained from google sheet
    output: pandas dataframe
    """
    colnames = (['Date of Visit', 'Restaurant', 'Cuisine', 'Location',
                 'Dishes', 'Comments'])
    df = pd.DataFrame(columns=colnames)
    for e in list_of_hashes:
        if not(e['Date of Visit'] == '' and e['Restaurant'] == ''):
            dov = e['Date of Visit']
            res = e['Restaurant']
            cui = e['Cuisine']
            loc = e['Location']
            dis = e['Dishes and Ratings']
            com = e['Comments']
            tmpdf = pd.DataFrame([[dov,res,cui,loc,dis,com]], columns=colnames)
            df = df.append(tmpdf, ignore_index=True)
    return (df)

def df2htmlRow(row):
    """
    Creates html row text for a df entry
    input: row, pandas data frame row from gsheet
    return: string with html text
    """
    htmlRow = '<tr class=\"row100 body\">\n'
    for i,k in enumerate(row.keys()):
        pre = "<td class=\"cell100 column{}\">".format(i+1)
        post = "</td>"
        line = pre + str(row[k]) + post
        htmlRow += line + "\n"
    htmlRow += '</tr>\n'
    return(htmlRow)

def getHtmlTable(data):
    """
    input: data, pd DataFrame with parsed gsuite info
    """
    table = ''
    for i in range(0,data.shape[0]):
        table += df2htmlRow(data.loc[i,:])
    return(table)




# GSuite config
scope = (['https://spreadsheets.google.com/feeds',
          'https://www.googleapis.com/auth/drive'])
creds = (ServiceAccountCredentials.from_json_keyfile_name(
                                                 'client_secret.json', scope))
client = gspread.authorize(creds)

# Open sheet and fetch data
sheet = client.open("Copy of Bradley’s Eats in NY").sheet1
list_of_hashes = sheet.get_all_records()
# print(list_of_hashes)

# Parse everything into Pandas data frames:
data = gsheet2df(list_of_hashes)
htmlText = getHtmlTable(data)

# Save to file
with open("out.txt", "w") as text_file:
    print(htmlText, file=text_file)


