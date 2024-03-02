import logging
import sys
from requests_html import HTMLSession
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from data_storer.chroma_client import ChromaDb

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebCrawler:

    def __init__(self, base_url : str, db : ChromaDb) -> None:
        self.base_url = urlparse(base_url)
        self.visited_sites = set()
        self.db = db

    def crawl_website(self):
        return self._crawl_website(self.base_url.geturl())
    
    
    def _crawl_website(self, url : str):
        if(len(self.visited_sites)==10):
            return
        if url in self.visited_sites:
            return
        self.visited_sites.add(url)

        session = HTMLSession()
        response = session.get(url)
        
        if response.status_code != 200:
            logger.warning(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
            return
        else:
            logger.info(f"Retrieving data from {url}. Status code: {response.status_code}")

        response.html.render()

        html_content = response.html.raw_html

        site_data = self._extract_data(html_content)
        self.db.add([site_data], url, [{"source": self.base_url.netloc }])
        logging.info(site_data)

        soup = BeautifulSoup(html_content, 'html.parser')
        links = [link for link in soup.find_all('a', href=True)]

        for link in links:
            next_url = urljoin(url, link['href'])
            parsed_next_url = urlparse(next_url)

            if parsed_next_url.netloc == self.base_url.netloc:
                self._crawl_website(next_url)

    def _extract_data(self, html: str) -> str:
        soup = BeautifulSoup(html, 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()

        text = soup.get_text(separator=' ')
        text = ' '.join(text.split()) 

        return text