import requests
from bs4 import BeautifulSoup
from langchain.tools import BaseTool
import ast

websites_content = ""


# URL to scrape


class CustomWebScraperTool(BaseTool):
    name: str = "WebsiteScraper"
    description: str = "Takes a list of websites then scrap and combine their respective content"

    def _run(self, urls_string: str) -> str:
        global websites_content

        try:
            urls = ast.literal_eval(urls_string)
            for link in urls:
                websites_content = websites_content + scrap_document(link)
        except Exception as ex:
            print("Error while parsing a link", ex)

        return websites_content


def scrap_document(url):
    article_content = ""
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the content of the response
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the title
        title = soup.find('h1').get_text(strip=True)

        # Extract the article content
        content = []
        for paragraph in soup.find_all('p'):
            content.append(paragraph.get_text(strip=True))

        # Join the content into a single string
        article_content = "\n".join(content)

        # Print the results
        print(f"Title: {title}\n")
        print("Content:")
        print(article_content)
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    return article_content
