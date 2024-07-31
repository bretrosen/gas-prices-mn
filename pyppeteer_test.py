# from requests_html import HTMLSession
# import logging

# logging.basicConfig(level=logging.DEBUG)

# session = HTMLSession()
# session.browser_args = ['--no-sandbox']
# # headers = {'User-Agent': 'bretrosen@gmail.com'}
# headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36"}
# response = session.get("https://www.npr.org/")


# try:
#     response.html.render()
#     print(response.html.html[:500])  # Print first 500 characters of the HTML
# except Exception as e:
#     logging.exception("An error occurred while rendering the page")


import asyncio
from pyppeteer import launch

async def main():
    browser = await launch(headless=False, args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'])
    page = await browser.newPage()
    await page.goto('https://www.npr.org/')
    await page.screenshot({'path': '/home/ec2-user/test1.png'})
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
