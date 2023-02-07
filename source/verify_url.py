from robotexclusionrulesparser import RobotExclusionRulesParser
from urllib.parse import urlparse
from socket import gethostbyname
from requests import get

class URLPermissionChecker:
    def __init__(self, url):
        self.url = url
        self.parsed_url = urlparse(url)
        self.errors = []

    def can_scrape(self):
        can_scrape = (
            self._is_https() and
            self._is_valid_format() and
            self._is_accessible() and
            self._has_scrape_permission()
        )
        return can_scrape


    def _is_https(self):
        if self.parsed_url.scheme == "https":
            return True
        else:
            self.errors.append('URL must start with https')
            return False


    def _is_valid_format(self):
        try:
            hostname = self.parsed_url.hostname
            gethostbyname(hostname)
            return True
        except:
            self.errors.append('invalid URL format')
            return False


    def _is_accessible(self):
        try:
            res = get(self.url)
            return res.status_code == 200
        except:
            self.errors.append('URL could not be reached')
            return False


    def _has_scrape_permission(self):
        robot_parser = self._parse_robots_txt()
        scrape_permission = robot_parser.is_allowed("User-agent", self.url)
        if not scrape_permission:
            self.errors.append('Scraping permission denied by site owner.')
        return scrape_permission

    def _parse_robots_txt(self):
        robots_txt = self._get_robots_txt()
        robot_parser = RobotExclusionRulesParser()
        robot_parser.parse(robots_txt)
        return robot_parser

    def _get_robots_txt(self):
        root_url = self._get_root_url()
        robots_url = root_url + '/robots.txt'
        response = get(robots_url)
        robots_txt = response.text
        return robots_txt

    def _get_root_url(self):
        root = self.parsed_url.scheme + "://" + self.parsed_url.netloc
        return root