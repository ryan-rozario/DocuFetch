import sys
from web_crawler_data.webbase_loader import WebCrawler
from data_storer.chroma_client import ChromaDb

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <base_url>")
        sys.exit(1)
    
    base_url = sys.argv[1]
    chroma_db = ChromaDb()
    crawler = WebCrawler(base_url, chroma_db)
    crawler.crawl_website()