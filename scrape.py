import requests
from robotexclusionrulesparser import RobotExclusionRulesParser
from urllib.parse import urlparse
import socket


class WebScraper:
    def __init__(self, url):
        self.url = url
        self.permission_checker = URLPermissionChecker(url)




class URLPermissionChecker:
    def __init__(self, url):
        self.url = url
        self.parsed_url = urlparse(url)

    def can_scrape(self):
        if not self._is_valid_url():
            return False
        robot_parser = self._parse_robots_txt()
        can_scrape = robot_parser.is_allowed("User-agent", self.url)
        return can_scrape


    def _is_valid_url(self):
        is_valid = (
            self._is_https() and
            self._is_valid_format() and
            self._is_accessible()
        )
        return is_valid

    def _is_https(self):
        return self.parsed_url.scheme == "https"

    def _is_valid_format(self):
        try:
            hostname = self.parsed_url.hostname
            socket.gethostbyname(hostname)
            return True
        except:
            return False

    def _is_accessible(self):
        try:
            res = requests.get(self.url)
            return res.status_code == 200
        except:
            return False


    def _parse_robots_txt(self):
        robots_txt = self._get_robots_txt()
        robot_parser = RobotExclusionRulesParser()
        robot_parser.parse(robots_txt)
        return robot_parser

    def _get_robots_txt(self):
        root_url = self._get_root_url()
        robots_url = root_url + '/robots.txt'
        response = requests.get(robots_url)
        robots_txt = response.text
        return robots_txt

    def _get_root_url(self):
        root = self.parsed_url.scheme + "://" + self.parsed_url.netloc
        return root
    

