from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# URL of the web page to scrape
url_to_scrape = "https://registry.verra.org/app/projectDetail/VCS/4675"


# Path to the Chrome WebDriver executable (replace with your own path)
# webdriver_path = "/path/to/chromedriver"

# Set up Chrome options for headless mode (optional)
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)

# Initialize the Chrome WebDriver with the specified options and URL
driver = webdriver.Chrome()

try:
    # Navigate to the URL
    driver.get(url_to_scrape)
    # Instead of using sleep
    # sleep(5)
    # Wait for some time to ensure page content is loaded (you can adjust the wait time)
    wait = WebDriverWait(driver, 15)
    # driver.implicitly_wait(10)
    # Get the page source as it appears in the browser
    element = wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "4675")))  # Wait for an <h1> element
    # continue_link = driver.find_element(By.PARTIAL_LINK_TEXT, 'Conti')
    

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')

    # Pretty-print the parsed HTML
    pretty_html = soup.prettify()

    # Print or process the page source as needed
    print(pretty_html)

    if pretty_html:
        # Save the pretty-printed HTML to a file
        output_file_name = "output.html"
        with open(output_file_name, 'w', encoding='utf-8') as file:
            file.write(pretty_html)

finally:
    # Close the WebDriver
    driver.quit()
