import requests
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import json

from selenium.webdriver.chrome.options import Options

d = DesiredCapabilities.CHROME
d['loggingPrefs'] = { 'performance':'ALL' }

chrome_options = Options()
chrome_options.add_experimental_option('w3c', False)

driver = webdriver.Chrome(desired_capabilities=d, options=chrome_options)
#driver = webdriver.Chrome()
driver.get("https://outagemap.alabamapower.com/")
time.sleep(5)

logs = driver.get_log("performance")
driver.close()

logs2 = pd.DataFrame(logs)
logs3 = logs2[logs2['message'].str.contains("data.json")]
logs3 = logs3.reset_index()
logs3['message'][0]
logs4 = logs3['message'].str.split("\"\:method\"\:\"GET\"\,\"\:path\"\:\"", n =2)[0][1]
logs5 = logs4.split("public/summary-1/data.json")
url_id = logs5[0]
#Example: "https://kubra.io/data/645393b1-4699-4049-93e6-2932351f7dc4/public/summary-1/data.json"
url = f'https://kubra.io{url_id}public/summary-1/data.json'
print (url)

req = requests.get(url)
data = req.json()

df = pd.DataFrame.from_dict(data)
df = df['summaryFileData'].apply(pd.Series)
df_p = df[0].apply(pd.Series)

#Pull out this moment's summary data
this_row = df_p.iloc[[4]] 
#Pull out timestamp
date = str(df_p.iloc[0,0])
#Add timestamp column
this_row = this_row.assign(timestamp=[date])
#Pull out number of customers affected
this_row['customers_affected'] = this_row['total_cust_a']['totals']['val']
#Rearrange columns and remove columns "total_cust_a" + "0" 
df2 = this_row[['timestamp', 'customers_affected', 'total_cust_s', 'total_outages', 'summaryTotalId']]

#df2.to_csv('./apc/summary.csv', mode='a', index=False, header=True)
df2.to_csv('apc/summary.csv', mode='a', index=False, header=False)

