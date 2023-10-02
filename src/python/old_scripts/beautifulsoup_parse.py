from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup


html_file_path = 'output.html'

with open(html_file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

body = soup.find_all("apx-document-group")
for docs in body:
    print("~~~~~")
    print(docs.prettify())
    header = docs.find_all("div", {"class": "card-header bg-primary"})
    for h in header:
        print(h.get_text().strip())
    doc_a = docs.find_all("a")
    doc_date = docs.find_all("td", {"class": "pr-3 text-right"})
    print(doc_a)
    print(doc_date)
    for i in range(len(doc_a)):
        link = doc_a[i]
        date = doc_date[i]
        print(link.get_text().strip())
        print(link.get("href").strip())
        print(date.get_text().strip())
    
