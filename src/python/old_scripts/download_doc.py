import requests

# URL of the PDF file
pdf_url = "https://registry.verra.org/mymodule/ProjectDoc/Project_ViewFile.asp?FileID=87536&IDKEY=8097809fdslkjf09rndasfufd098asodfjlkduf09nm23mrn87u120712144"

# Send an HTTP GET request to the URL
response = requests.get(pdf_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Get the content of the PDF file
    pdf_content = response.content

    # Specify the file name to save the PDF
    pdf_filename = "downloaded_pdf.pdf"

    # Save the PDF content to a file
    with open(pdf_filename, 'wb') as pdf_file:
        pdf_file.write(pdf_content)

    print(f"PDF downloaded and saved as '{pdf_filename}'")
else:
    print(f"Failed to download PDF. Status code: {response.status_code}")
