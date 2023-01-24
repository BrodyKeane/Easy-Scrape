import requests
from robotexclusionrulesparser import RobotExclusionRulesParser
from urllib.parse import urlparse


class WebScraper:
    def __init__(self, url):
        self.url = url
        self.permission_checker = URLPermissionChecker(url)




class URLPermissionChecker:
    def __init__(self, url):
        self.url = url

    def can_scrape(self):
        robot_parser = self._parse_robots_txt()
        can_scrape = robot_parser.is_allowed("User-agent", self.url)
        return can_scrape

    def get_root_url(self):
        parsed_url = urlparse(self.url)
        root = parsed_url.scheme + "://" + parsed_url.netloc
        return root
    
    def _get_robots_txt(self):
        root_url = self.get_root_url()
        robots_url = root_url + '/robots.txt'
        response = requests.get(robots_url)
        robots_txt = response.text
        return robots_txt

    def _parse_robots_txt(self):
        robots_txt = self._get_robots_txt()
        robot_parser = RobotExclusionRulesParser()
        robot_parser.parse(robots_txt)
        return robot_parser

