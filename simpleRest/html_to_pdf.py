import urllib.request
import logging
from urllib.parse import urlparse
import unittest
from pywebcopy import save_website


from download_item import DownloadItem

def saveWebPageAsPdf(downloadItem: DownloadItem) -> bool:
    logging.debug(f"DL {downloadItem.url}")
    urllib.request.urlretrieve(downloadItem.url, f'{downloadItem.id}.html')

class HtmlSaver(unittest.TestCase):

    def test_DL(self):
        save_website(
            url="https://fusionauth.io/docs/get-started/core-concepts/entity-management",
            project_folder="/home/horzsolt/mnt/nas/SAVED_WEBPAGES",
            project_name="my_site",
            bypass_robots=True,
            debug=True,
            open_in_browser=False,
            delay=1000,
            threaded=False,
        )


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(HtmlSaver)
    unittest.TextTestRunner().run(suite)
    # unittest.main()
