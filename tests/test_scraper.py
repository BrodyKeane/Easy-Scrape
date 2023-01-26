import unittest
from source.scrape import CorrelatedDataScraper

class TestCorrelatedDataScraper(unittest.TestCase):
    def test_result_success(self):
        url = 'https://quotes.toscrape.com'
        container_tag = '.quote'
        data_tags = ['.author', '.text']
        scraper = CorrelatedDataScraper(url, container_tag, data_tags)
        rows = scraper.scrape()

        author = 'J.K. Rowling'
        text = '“It is our choices, Harry, that show what we truly are, far more than our abilities.”'
        pseudo_row = {'.author': author, '.text': text}

        self.assertEqual(rows[1], pseudo_row)

    def test_result_success_with_limit(self):
        url = 'https://books.toscrape.com'
        container_tag = '.row > li'
        data_tags = ['h3 a', '.price_color']
        scraper = CorrelatedDataScraper(url, container_tag, data_tags, row_limit=2)
        rows = scraper.scrape()

        title = 'Tipping the Velvet'
        price = 'Â£53.74'
        pseudo_row = {'h3 a': title, '.price_color': price}

        self.assertEqual(rows[1], pseudo_row)

    def test_result_failure_past_limit(self):
        url = 'https://books.toscrape.com'
        container_tag = '.row > li'
        data_tags = ['h3 a', '.price_color']
        scraper = CorrelatedDataScraper(url, container_tag, data_tags, row_limit=1)
        rows = scraper.scrape()

        def raise_index_error():
            rows[1]

        self.assertRaises(IndexError, raise_index_error)

    def test_limit_zero_removes_limit(self):
        url = 'https://books.toscrape.com'
        container_tag = '.row > li'
        data_tags = ['h3 a', '.price_color']
        scraper = CorrelatedDataScraper(url, container_tag, data_tags, row_limit=0)
        rows = scraper.scrape()

        title = 'Tipping the Velvet'
        price = 'Â£53.74'
        pseudo_row = {'h3 a': title, '.price_color': price}       

        self.assertEqual(rows[1], pseudo_row)

    def test_result_from_end_of_large_scrape(self):
        url = 'https://books.toscrape.com'
        container_tag = '.row > li'
        data_tags = ['h3 a', '.price_color']
        scraper = CorrelatedDataScraper(url, container_tag, data_tags)
        rows = scraper.scrape()

        title = "It's Only the Himalayas"
        price = 'Â£45.17'
        pseudo_row = {'h3 a': title, '.price_color': price}       

        self.assertEqual(rows[-1], pseudo_row)

    def test_container_tag_not_found_returns_none(self):
        url = 'https://books.toscrape.com'
        container_tag = '.fake_tag'
        data_tags = ['h3 a', '.price_color']
        scraper = CorrelatedDataScraper(url, container_tag, data_tags)
        rows = scraper.scrape()

        def raise_index_error():
            rows[1]

        self.assertRaises(IndexError, raise_index_error)

    def test_data_tag_not_found_returns_none(self):
        url = 'https://books.toscrape.com'
        container_tag = '.fake_tag'
        data_tags = ['fake_tag']
        scraper = CorrelatedDataScraper(url, container_tag, data_tags)
        rows = scraper.scrape()

        def raise_index_error():
            rows[1]

        self.assertRaises(IndexError, raise_index_error)