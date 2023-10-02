from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import json
import requests
import re
from datetime import datetime
import subprocess
from typing import Dict

# Import Env variables or hard code yourself
gcloud_project = os.getenv("GCLOUDPROJECT", "<your project id>")
gcloud_doc_landing = os.getenv("GCLOUDDOCLANDING", "document landing path")

# Get the current timestamp
current_time = datetime.now()

# Format the timestamp as yyyymmddhhmmss
formatted_time = current_time.strftime("%Y%m%d%H%M%S")

def gen_path(new_path: str):
    # Check if the directory already exists
    if not os.path.exists(new_path):
        # If it doesn't exist, create the directory
        os.makedirs(new_path)

def doc_store_upload(formatted_time: str, file_path: str, meta: Dict):
    category =  re.sub('"|\'|-| |,|_|/|\\|;','_',meta["category"])
    mimeType = meta["Content-Type"]
    name = re.sub( r'[^a-zA-Z0-9-_\.]', '_', meta["name"])
    project_id=meta["project_id"]
    id = re.sub(r'[^a-zA-Z0-9]','', f"{project_id}_{name}")[:63]
    output_file_name = f"{file_path}/{name}"
    # upload html to docstore ndjson
    data={
        "id":id,
        "jsonData":json.dumps(meta),
        "content":{
            "mimeType":mimeType,
            "uri":f"gs://{gcloud_project}/{gcloud_doc_landing}/{output_file_name}"
        }
    }
    output_file_name = f"docs/doc_store_{formatted_time}.ndjson"
    with open(output_file_name, 'a', encoding='utf-8') as file:
        file.write(json.dumps(data))
        file.write('\n')


# Add list of project id to download 
project_id_list = [
    "3180",
    "3557",
    "3360",
    "3093",
    "2584",
    "2549",
    "924",
    "1090",
    "2035",
]

# project_id_list = ["3180"]

for project_id in project_id_list:
    print(project_id)
    # Initiate meta data
    meta = {
        "project_id":project_id
    }
    # Specify the directory path you want to create (replace with your desired path)
    directory_path = f"docs/{project_id}"
    gen_path(directory_path)

    # URL of the web page to scrape
    url_to_scrape = f"https://registry.verra.org/app/projectDetail/VCS/{project_id}"
    meta["url"]=url_to_scrape
    meta["root_url"]=url_to_scrape

    # Set up Chrome options for headless mode (optional)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)

    # Initialize the Chrome WebDriver with the specified options and URL
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Navigate to the URL
        driver.get(url_to_scrape)
        # Wait for some time to ensure page content is loaded (you can adjust the wait time)
        wait = WebDriverWait(driver, 15)
        try:
            element = wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, f"{project_id}")))  # Wait for the project id to appear in the soup
        except:
            print("initiate manual sleep")
            sleep(10)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        # Pretty-print the parsed HTML
        pretty_html = soup.prettify()

        if pretty_html:
            # Download the html information
            file_path = f"{directory_path}/html"
            gen_path(file_path)
            # Save the pretty-printed HTML to a file
            meta["category"] = "summary"
            meta["Content-Type"] =  "text/html"
            meta["name"] = f"{project_id}_vcs.html"
            name = meta["name"]
            output_file_name = f"{file_path}/{name}"
            with open(output_file_name, 'w', encoding='utf-8') as file:
                file.write(pretty_html)
            # upload html to docstore ndjson
            doc_store_upload(formatted_time=formatted_time, file_path=file_path, meta=meta)

            # Check for documents
            body = soup.find_all("apx-document-group")
            for docs in body:
                header = docs.find_all("div", {"class": "card-header bg-primary"})
                for h in header:
                    category =  re.sub('"|\'|-| |,|_|/|\\|;','_',h.get_text().strip())
                    meta["category"] = category
                doc_a = docs.find_all("a")
                for link in doc_a:
                    file_path = f"{directory_path}/{category}"
                    gen_path(file_path)
                    meta["Content-Type"] =  "application/pdf"
                    name = re.sub( r'[^a-zA-Z0-9-_\.]', '_', link.get_text().strip())
                    meta["name"] =  name
                    output_file_name = f"{file_path}/{name}"
                    url = link.get("href").strip()
                    meta["url"]=url
                    # Send an HTTP GET request to the URL
                    response = requests.get(f"{url}")
                    # Check if the request was successful (status code 200)
                    if response.status_code == 200:
                        # Get the content of the PDF file
                        pdf_content = response.content
                        # Save the PDF content to a file
                        with open(output_file_name, 'wb') as pdf_file:
                            pdf_file.write(pdf_content)
                        # upload html to docstore ndjson
                        if output_file_name[-4:].lower()=='.pdf':
                            doc_store_upload(formatted_time=formatted_time, file_path=file_path, meta=meta)

    finally:
        # Close the WebDriver
        driver.quit()

# Need to move the landing  
# gsutil -m cp -r docs/ gs://macdemo/verradocstore/
# Define the gsutil command as a list of strings
gsutil_command = [
    'gsutil',
    '-m',
    'mv',
    '-r',
    'docs/',
    f'gs://{gcloud_project}/{gcloud_doc_landing}/'
]

# Run the gsutil command
try:
    subprocess.run(gsutil_command, check=True)
    print("Successfully moved files to Google Cloud Storage.")
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")