import requests
from bs4 import BeautifulSoup

def download_html(url):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content with Beautiful Soup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Pretty-print the parsed HTML
            pretty_html = soup.prettify()

            return pretty_html
        else:
            print(f"Failed to download HTML. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # URL to download HTML from
    url_to_download = "https://registry.verra.org/app/projectDetail/VCS/4675"

    # Download and parse the HTML
    html_content = download_html(url_to_download)

    if html_content:
        # Save the pretty-printed HTML to a file
        output_file_name = "output.html"
        with open(output_file_name, 'w', encoding='utf-8') as file:
            file.write(html_content)

        print(f"Pretty-printed HTML content saved to {output_file_name}")
