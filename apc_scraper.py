import requests
import pandas as pd

from kubra_scraper import KubraScraper


class APCScraper(KubraScraper):
    owner = "austinfast"
    repo = "power-outage-data"
    filepath = "apc/outages.json"

    instance_id = "7636a60f-7b81-4fb0-a30d-ed79a8e271e7"
    view_id = "c3471c92-6e1b-494b-a884-391139a2cc18"
    
#Save summary file
###data = self._make_request(self.data_url).json()
req = requests.get(data_url)
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
#Save file
df2.to_csv("./apc/summary.csv", mode='a', index=False, header=True)

    #Kentucky 
    #instance_id = "877fd1e9-4162-473f-b782-d8a53a85326b" 
    #view_id = "a6cee9e4-312b-4b77-9913-2ae371eb860d"
