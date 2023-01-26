from requests import get
from robotexclusionrulesparser import RobotExclusionRulesParser
from urllib.parse import urlparse
from socket import gethostbyname
from bs4 import BeautifulSoup

class CorrelatedDataScraper:
    def __init__(self, url, container_tag, data_tags, row_limit=100):
        self.url = url
        self.container_tag = container_tag
        self.data_tags = data_tags
        self.row_limit = row_limit

    def scrape(self):
        containers = self._find_containers()
        rows = self._get_rows(containers)
        return rows

    def _find_containers(self):
        response = get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        containers = soup.select(self.container_tag, limit=self.row_limit)
        return containers

    def _get_rows(self, containers):
        rows = []
        for container in containers:
            row = self._populate_row(container)
            rows.append(row)
        return rows

    def _populate_row(self, container):
        row = {}
        for data_tag in self.data_tags:
            try:
                data = container.select_one(data_tag).text
                row[data_tag] = data
            except:
                row[data_tag] = f'{data_tag} not found'
        return row

    def set_container_tag(self, tag):
        self.container_tag = tag

    def add_data_tag(self, tag):
        self.data_tags.append(tag)

    def remove_data_tag(self, tag):
        self.data_tags.remove(tag)



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
            gethostbyname(hostname)
            return True
        except:
            return False

    def _is_accessible(self):
        try:
            res = get(self.url)
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
        response = get(robots_url)
        robots_txt = response.text
        return robots_txt

    def _get_root_url(self):
        root = self.parsed_url.scheme + "://" + self.parsed_url.netloc
        return root
    

