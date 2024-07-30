from requests_html import HTMLSession
import logging

logging.basicConfig(level=logging.DEBUG)

session = HTMLSession()
session.browser_args = ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
response = session.get('https://www.gasbuddy.com/gasprices/minnesota')


try:
    response.html.render(wait=5, timeout=60, keep_page=True, retries=3)
    print(response.html.html[:500])  # Print first 500 characters of the HTML
except Exception as e:
    logging.exception("An error occurred while rendering the page")
