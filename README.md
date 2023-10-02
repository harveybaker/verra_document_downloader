# verra_document_downloader
This repository is developed to help scrape https://verra.org/ for documents and to push them to google cloud big query

login to google cloud on your local computer
[gcloud auth login](https://cloud.google.com/sdk/gcloud/reference/auth/login)

to set up and run locally 
set up env
`GCLOUDPROJECT="<your project id>")`
`GCLOUDDOCLANDING="document landing path")`
`cd src`
`python python/full_download.py`

image.png