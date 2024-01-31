from urllib.parse import urlparse
import scrapy
from readability import Document
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account


class GuardianSpider(scrapy.Spider):
    name = "guardian"
    allowed_domains = ["www.theguardian.com"]
    start_urls = ["https://www.theguardian.com/uk/technology"]

    data = []

    def parse(self, response):
        # Extracts links from The guardian technology page 
        article_links = response.css('.dcr-lv2v9o::attr(href)').extract()

        # Filter links to include only those related to technology
        filtered_article_links = [link for link in article_links if link.startswith('/technology')]

        # Iterate over the filtered links and call the parse_article function for each article
        for article_link in filtered_article_links:
            full_article_link = response.urljoin(article_link)
            yield scrapy.Request(url=full_article_link, callback=self.parse_article)


    def parse_article(self, response):

        # Use the readability library to extract content from the article
        doc = Document(response.text)
        
        # Extract specific information from the article using CSS selectors
        date = response.css('.dcr-u0h1qy::text').get()
        title = response.css('.dcr-1fasd0d, .dcr-qao4mw::text').get()
        author = response.css('div.dcr-1umb6ym a::text').get()
        text = response.css('.dcr-1lpi6p1 ::text').getall()

        # Convert the list of strings into a single string
        text_as_string = '\n'.join(text)

        # Get the URL of the article
        article_url = response.url

        # Check if all necessary information has been extracted
        if date and title and author and text_as_string:
            data = {
                'title': title,
                'author': author,
                'text': text_as_string,
                'date': date,
                'url': article_url,
            }
            self.log(f"Data extracted: {data}")
            self.data.append(data)

    def closed(self, reason):
        # Convert the list of data into a pandas DataFrame
        df = pd.DataFrame(self.data)
        
        # BigQuery configuration
        project_id = 'guardianscrapy'  
        dataset_id = 'guardian_technology' 
        table_id = 'articles'  

        table_path = f'{project_id}.{dataset_id}.{table_id}'
        key_path = 'C:\\Users\\Maria Alice\\Desktop\\scrapyproject\\GBQ.json'
        credentials = service_account.Credentials.from_service_account_file(key_path, scopes=['https://www.googleapis.com/auth/cloud-platform'])
        
        # Save the data to a local CSV file
        df.to_csv("output_guardian.csv", index=False)
        
        # Load the DataFrame to BigQuery
        df.to_gbq(destination_table=table_path, project_id=project_id, if_exists='replace', credentials=credentials)
        
        self.log(f'DataFrame carregado para BigQuery: {table_path}')    

        