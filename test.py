import unittest
from scrape import URLPermissionChecker

class TestScrape(unittest.TestCase):

    def test_permission_to_scrape_allowed(self):
        url = 'https://www.w3schools.com'
        test_scrape = URLPermissionChecker(url)
        permission = test_scrape.can_scrape()
        self.assertEqual(permission, True) 

    def test_permission_to_scrape_not_allowed(self):
        url = 'https://www.w3schools.com/code/'
        test_scrape = URLPermissionChecker(url)
        permission = test_scrape.can_scrape()
        self.assertEqual(permission, False)

    def test_permission_to_scrape_on_404(self):
        url = 'https://www.imdb.com/fake-url'
        test_scrape = URLPermissionChecker(url)
        permission = test_scrape.can_scrape()
        self.assertEqual(permission, True)

    def test_get_root_url(self):
        url = 'https://www.w3schools.com/html/default.asp'
        test_scrape = URLPermissionChecker(url)
        root = test_scrape.get_root_url()
        self.assertEqual(root, 'https://www.w3schools.com')

    def test_get_root_url_from_root(self):
        url = 'https://www.w3schools.com'
        test_scrape = URLPermissionChecker(url)
        root = test_scrape.get_root_url()
        self.assertEqual(root, 'https://www.w3schools.com')

    def test_get_root_url_from_404(self):
        url = 'https://www.w3schools.com/fake-urll'
        test_scrape = URLPermissionChecker(url)
        root = test_scrape.get_root_url()
        self.assertEqual(root, 'https://www.w3schools.com')

    def test_get_root_url_from_url(self):
        url = 'asdfasdfasdfxlf[feamfai9efa'
        test_scrape = URLPermissionChecker(url)
        root = test_scrape.get_root_url()
        self.assertEqual(root, '://')

    def test_get_list_of_elements(self):
        pass


if __name__ == '__main__':
    unittest.main()
