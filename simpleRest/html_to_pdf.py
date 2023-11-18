import urllib.request
import logging
from urllib.parse import urlparse


from download_item import DownloadItem

def saveWebPageAsPdf(downloadItem: DownloadItem) -> bool:
    logging.debug(f"DL {downloadItem.url}")
    urllib.request.urlretrieve(downloadItem.url, f'{downloadItem.id}.html')
