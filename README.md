# **The Guardian Scraper**
This web scraper, named "GuardianSpider," is designed to extract information related to technology articles from The Guardian. It uses the Scrapy framework for web crawling, the readability library for content extraction, and interacts with Google BigQuery to store the extracted data.

### How it Works
1. **Start URL:** 
* The scraper begins by navigating to The Guardian's technology section: The Guardian Technology.

2. **Extracting Article Links:**
* It extracts links from the technology page.
* Filters and selects only the links related to technology articles.

3. **Parsing Articles:**
* For each technology article link, it follows the link and extracts the following information:
  * Date of the article
  * Title
  * Author
  * Text content
  * Article URL

4. **Saving Data:**
* The extracted data is stored in a pandas DataFrame.

5. **BigQuery Integration:**
The data is saved to a local CSV file (output_guardian.csv).
The pandas DataFrame is uploaded to Google BigQuery for further analysis and storage.
The BigQuery table path is defined as project_id.dataset_id.table_id.

### Requirements
  * Python
  * Scrapy
  * readability
  * pandas
  * google-cloud-bigquery
  * google-auth

### Configuration
1. Google BigQuery Credentials:
* Replace the placeholder file path in the key_path variable with the path to your JSON key file for authenticating with Google Cloud.
2. Google BigQuery Project Details:
* Adjust the project_id, dataset_id, and table_id variables based on your Google BigQuery project setup.

### Running the Scraper:
* `scrapy crawl guardian`

### Note
* Ensure that you have the required Python libraries installed (scrapy, readability, pandas, google-cloud-bigquery, google-auth) before running the scraper.

Feel free to customize and extend this scraper based on your specific requirements.
