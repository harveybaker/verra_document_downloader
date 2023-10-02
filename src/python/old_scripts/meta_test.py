# {"id":"doc-0","jsonData":"{\"project_id\":\"1234\",\"description\":\"This document uses a blue color theme\",\"color_theme\":\"red\"}","content":{"mimeType":"application/pdf","uri":"gs://macdemo/verra/EESP PoA_9769 Monitoring  Report_17Oct17-16Oct18 (1).pdf"}}
import json
import os

gcloud_project = os.getenv("GCLOUDPROJECT", "<your project id>")
gcloud_doc_landing = os.getenv("GCLOUDDOCLANDING", "document landing path")

meta = {
    "meta1":"str",
    "meta2":2,
}

data={
    "id":"id_name",
    "jsonData":json.dumps(meta),
    "content":{
        "mimeType":"application/pdf",
        "uri":f"gs://{gcloud_project}/{gcloud_doc_landing}/EESP PoA_9769 Monitoring  Report_17Oct17-16Oct18 (1).pdf"
    }
}

output_file_name = "output.ndjson"
with open(output_file_name, 'a', encoding='utf-8') as file:
    file.write(json.dumps(data))
    file.write('\n')