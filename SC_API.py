import requests
import json
import pandas as pd
import datetime
filename="Data.csv"
counter=1
response = requests.get(
'https://www.databricks.com/en-partners-assets/data/partner/c&si-partner/en.json')
data_out=response.json()
ti=[]
ul=[]
for i in range(0,len(data_out)):
    if data_out[i]['fieldUrl']==None:
        pass
    else:
        title=data_out[i]['title']
        url=data_out[i]['fieldUrl']['url']['path']
        ti.append(title)
        ul.append(url)
        print(counter)
        counter+=1
data={'Title':ti,
'URL':ul
    }
df=pd.DataFrame(data,columns=['Title','URL'])
df.to_csv(filename,index=False)
print("Done")
