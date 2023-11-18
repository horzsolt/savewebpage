import asyncio
import logging
import os
from urllib.parse import urlparse
from pyppeteer import launch

async def generate_pdf(url, pdf_path):

    browser = await launch()
    page = await browser.newPage()

    await page.goto(url)
    await page.pdf({'path': pdf_path, 'format': 'A4'})
    await browser.close()

def saveWebPageAsPdf(url: str, tags: str)-> bool:
    logging.debug(f"DL {str}")
    pageName = urlparse(url)
    logging(pageName.path)
    logging(os.path.basename(pageName.path))

    asyncio.get_event_loop().run_until_complete(generate_pdf('https://example.com', 'example.pdf'))
