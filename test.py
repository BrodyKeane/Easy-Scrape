import unittest
from scrape import URLPermissionChecker, CorrelatedDataScraper

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





class TestURLPermissionChecker(unittest.TestCase):
    def test_permission_to_scrape_from_root(self):
        url = 'https://www.w3schools.com'
        test_scrape = URLPermissionChecker(url)
        permission = test_scrape.can_scrape()
        self.assertEqual(permission, True) 

    def test_permission_to_scrape_from_sub_dir(self):
        url = 'https://www.w3schools.com/html/html_blocks.asp'
        test_scrape = URLPermissionChecker(url)
        permission = test_scrape.can_scrape()
        self.assertEqual(permission, True) 

    def test_permission_to_scrape_not_allowed(self):
        url = 'https://www.w3schools.com/code/'
        test_scrape = URLPermissionChecker(url)
        permission = test_scrape.can_scrape()
        self.assertEqual(permission, False)

    def test_permission_to_scrape_on_404(self):
        url = 'https://www.w3schools.com/fakdafse-url'
        test_scrape = URLPermissionChecker(url)
        permission = test_scrape.can_scrape()
        self.assertEqual(permission, False)

    def test_permission_to_scrape_from_blank_url(self):
        url = ''
        test_scrape = URLPermissionChecker(url)
        permission = test_scrape.can_scrape()
        self.assertEqual(permission, False)

    def test_permission_to_scrape_from_http(self):
        url = 'http://www.w3schools.com'
        test_scrape = URLPermissionChecker(url)
        permission = test_scrape.can_scrape()
        self.assertEqual(permission, False)

    def test_permission_to_scrape_from_unformatted_url(self):
        url = 'w3schools.com'
        test_scrape = URLPermissionChecker(url)
        permission = test_scrape.can_scrape()
        self.assertEqual(permission, False)





if __name__ == '__main__':
    unittest.main()
