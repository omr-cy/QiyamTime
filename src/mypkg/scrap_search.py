from bs4 import BeautifulSoup
from httpx import Client
from fake_useragent import UserAgent

client: Client = Client(
    headers={
        "user-agent": UserAgent().random,
        "Accept-Language": "en-US,en;q=0.9,lt;q=0.8,et;q=0.7,de;q=0.6"
    },
    follow_redirects=True,
    http2=True,  # use HTTP/2 
    # timeout=0.2,
)

class Search:
    def __init__(self, query :str, parser :str="html.parser"):  
        self.query = query.strip().replace(' ','%20')
        self.parser = parser
       
    @property
    def soup(self):
        response = client.get(f"https://www.startpage.com/sp/search?q={self.query}")
        print(f"Search Status = {response.status_code}")
        soup:BeautifulSoup = BeautifulSoup(response.content, self.parser)
        return soup

    def target_link(self, link):
        link = self.soup.find("a", href=lambda href: href and f"{link.strip()}" in href)
        return link["href"]


