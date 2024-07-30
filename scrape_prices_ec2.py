from requests_html import HTMLSession
import pandas as pd
from datetime import datetime, timedelta
import os
import csv
from pyppeteer import launch
from bs4 import BeautifulSoup
import asyncio

# def parse_time(reported_time):
#     if 'hour' in reported_time:
#         hours = int(reported_time.split()[0])
#         return timedelta(hours=hours)
#     elif 'minute' in reported_time:
#         minutes = int(reported_time.split()[0])
#         return timedelta(minutes=minutes)
#     else:
#         return timedelta(0)


# def scrape_prices(url, csv_file):
#     session = HTMLSession()
#     response = session.get(url)
#     response.html.render(wait=1)

#     stations = response.html.find('div.GenericStationListItem-module__stationListItem___3Jmn4')

#     data = []
#     for rank, station in enumerate(stations[:10], start=1):
#         try:
#             store = station.find('h3', first=True).text.strip()
#             address = station.find('.StationDisplay-module__address___2_c7v', first=True).text.strip()
#             price = station.find('span.text__xl___2MXGo.text__left___1iOw3.StationDisplayPrice-module__price___3rARL', first=True).text.strip()
#             reported_time = station.find('span.ReportedBy-module__postedTime___J5H9Z', first=True).text.strip()
#         except AttributeError:
#             print("Ope!")
#             continue

#         now = datetime.now()
#         adjusted_time = now - parse_time(reported_time)
#         date = adjusted_time.strftime("%Y-%m-%d")
#         time_ = adjusted_time.strftime("%H:%M:%S")

#         data.append([date, time_, store, address, price, rank])

#     df = pd.DataFrame(data, columns=['Date', 'Time', 'Store', 'Address', 'Price', 'Rank'])

#     if not os.path.isfile(csv_file):
#         df.to_csv(csv_file, index=False)
#     else:
#         existing_df = pd.read_csv(csv_file)
#         combined_df = pd.concat([existing_df, df])
#         combined_df.to_csv(csv_file, index=False)

# scrape_prices("https://www.gasbuddy.com/gasprices/minnesota", '/home/ec2-user/gas-prices-mn-2024/data/gas_prices_mn.csv')
# scrape_prices("https://www.gasbuddy.com/gasprices/minnesota/twin-cities", '/home/ec2-user/gas-prices-mn-2024/data/gas_prices_tc.csv')
# scrape_prices("https://www.gasbuddy.com/gasprices/minnesota/minneapolis", '/home/ec2-user/gas-prices-mn-2024/data/gas_prices_mpls.csv')
# scrape_prices("https://www.gasbuddy.com/gasprices/minnesota/st.-paul", '/home/ec2-user/gas-prices-mn-2024/data/gas_prices_st_paul.csv')
# scrape_prices("https://www.gasbuddy.com/gasprices/minnesota/st.-louis-park", '/home/ec2-user/gas-prices-mn-2024/data/gas_prices_stl_park.csv')
# scrape_prices("https://www.gasbuddy.com/gasprices/minnesota/carlton/1448", '/home/ec2-user/gas-prices-mn-2024/data/gas_prices_carlton_cty.csv')
# scrape_prices("https://www.gasbuddy.com/gasprices/minnesota/pine/2151", '/home/ec2-user/gas-prices-mn-2024/data/gas_prices_pine_cty.csv')
# scrape_prices("https://www.gasbuddy.com/gasprices/minnesota/st.-louis/884", '/home/ec2-user/gas-prices-mn-2024/data/gas_prices_stl_cty.csv')



async def scrape_prices(url, csv_file):
    browser = await launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    page = await browser.newPage()
    await page.goto(url)
    await page.waitForSelector('div.GenericStationListItem-module__stationListItem___3Jmn4')
    content = await page.content()
    await browser.close()

    soup = BeautifulSoup(content, 'html.parser')
    stations = soup.find_all('div', class_='GenericStationListItem-module__stationListItem___3Jmn4')

    data = []
    now = datetime.now()

    for rank, station in enumerate(stations[:10], start=1):
        store = station.find('h3', class_='header__header3___1b1oq').text.strip()
        address = station.find('div', class_='StationDisplay-module__address___2_c7v').text.strip()
        price = station.find('span', class_='text__xl___2MXGo').text.strip()
        reported_time = station.find('span', class_='ReportedBy-module__postedTime___J5H9Z').text.strip()

        adjusted_time = now
        if 'hour' in reported_time:
            hours = int(reported_time.split()[0])
            adjusted_time -= timedelta(hours=hours)
        elif 'minute' in reported_time:
            minutes = int(reported_time.split()[0])
            adjusted_time -= timedelta(minutes=minutes)

        date = adjusted_time.strftime('%Y-%m-%d')
        time = adjusted_time.strftime('%H:%M:%S')

        data.append([date, time, store, address, price, rank])

    file_exists = os.path.isfile(csv_file)
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Date', 'Time', 'Store', 'Address', 'Price', 'Rank'])
        writer.writerows(data)

# Main function to run the scraper
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(scrape_prices("https://www.gasbuddy.com/gasprices/minnesota", '/home/ec2-user/gas-prices-mn-2024/data/gas_prices_mn.csv'))
