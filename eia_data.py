import requests
import pandas as pd
import os

def get_retail_gas(start, end, csv_file):
    EIA_KEY = os.environ.get("EIA_KEY")
    url = f"https://api.eia.gov/v2/petroleum/pri/gnd/data/?api_key={EIA_KEY}&frequency=weekly&data[0]=value&start={start}&end={end}&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"

    res = requests.get(url)
    res.raise_for_status()

    data = res.json()['response']['data']
    output = []
    total = 0

    for datum in data:
        if "Minnesota Regular Conventional Retail Gasoline" in datum['series-description']:
            price = float(0 if datum['value'] is None else datum['value'])
            output.append([datum['period'], price, datum['units']])
            total += price

    df = pd.DataFrame(output, columns=['Date', 'Price', 'Units'])

    if not os.path.isfile(csv_file):
        df.to_csv(csv_file, index=False)
    else:
        existing_df = pd.read_csv(csv_file)
        combined_df = pd.concat([existing_df, df])
        combined_df.to_csv(csv_file, index=False)

start = "2024-05-01"
end = "2024-07-30"
csv_file = '/home/bretrosen/data/gas-prices-mn-2024/data/eia_data_mn.csv'

get_retail_gas(start, end, csv_file)
