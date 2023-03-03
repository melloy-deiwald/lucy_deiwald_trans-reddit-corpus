import json, sys
import pandas as pd
import numpy as np

year = sys.argv[1]

files = ["ftm-result.json", "MtF-result.json", "NonBinary-result.json", "trans-result.json", "truscum-result.json"]
formated_data = []

#!!!!!!
location = ""
#!!!!!!

with open(location+year+"/subreddit_view/"+year+"-"+"ftm-result.json", "r") as order_file_json:
    order_json_data = json.load(order_file_json)

keys = list(order_json_data.keys())
formated_data.append(keys)

for file in files:

    with open(location+year+"/subreddit_view/"+year+"-"+file, "r") as input_file_json:
        json_data = json.load(input_file_json)

    column = []

    first = True
    for item in json_data:
        if first:
            column.append(json_data[item])
            first = False
        else:
            column.append(json_data[item][0])
    formated_data.append(column)

numpy_data = np.array(formated_data)
df = pd.DataFrame(data=numpy_data).T
df.columns = [f'mycol{i}' for i in range(0,len(df.T))] 
cvs_data = df.to_csv(location+year+"_formatted.csv", index = False)

