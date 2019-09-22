from flask import Flask, render_template
import pandas as pd
import urllib, json
from pandas.io.json import json_normalize


app = Flask(__name__)

@app.route('/')
def home ():
    with urllib.request.urlopen("https://opendata.arcgis.com/datasets/ea875858ec11462ab4e8a2ef5dc2c4ce_0.geojson") as url:
        data = json.loads(url.read().decode())
        data = data['features']

    df = json_normalize(data)
    df = df.rename(columns = {'properties.Year_and_Quarter':'Year_and_Quarter', 
                            'properties.Sector':'Sector', 
                            'properties.Kshs_Million':'Kshs_Million'})

    new = df['Year_and_Quarter'].str.split(" ", n = 1, expand = True)
    df['Year'] = new[0]

    df.drop(['type', 'id', 'geometry', 'properties.OBJECTID', 'Year_and_Quarter'], inplace = True, axis = 1)

    df1 = df.groupby(['Sector', 'Year']).sum()
    df2 = pd.pivot_table(df1, values="Kshs_Million", index=["Sector"], columns=["Year"])

    return df2.to_html()
    

if __name__ == '__main__':
    app.run(debug = True)