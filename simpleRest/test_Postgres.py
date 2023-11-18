import unittest

from pg_helper import PostgresHelper

class Test_Postgres(unittest.TestCase):

    def test_select(self):

        with (PostgresHelper()) as pg:
            [print(dlItem) for dlItem in pg.list_urls_to_download()]

if __name__ == '__main__':
    unittest.main()
