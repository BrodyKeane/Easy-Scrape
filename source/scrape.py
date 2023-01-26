from requests import get
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




    

