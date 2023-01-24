import unittest
from scrape import URLPermissionChecker

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
