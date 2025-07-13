import requests
import json
from google.cloud import storage
from datetime import datetime
from dotenv import load_dotenv
import os
import logging


logging.basicConfig(level=logging.INFO)


# Load environment variables from the .env file (if present)
load_dotenv()


BUCKET_NAME = os.getenv('BUCKET_NAME')
print(BUCKET_NAME)

def get_data(request):
  url="https://fakestoreapi.com/products"
  datetime_str = datetime.now().strftime("%Y%m%dT%H:%M:%S")
  filename = f"fakestore_{datetime_str}.json"

  try:
    logging.info(f"Fetching data from {url}")
    response=requests.get(url)
    data = response.json()

    # Create client
    storage_client = storage.Client()
    
    # Get the bucket
    bucket = storage_client.bucket(BUCKET_NAME)
    
    #Create a blob or an object
    blob = bucket.blob(f"raw/{filename}")
    
    # Upload a local file to the blob
    blob.upload_from_string(json.dumps(data))
    
    logging.info(f"Uploaded to gs://{BUCKET_NAME}/raw/{filename}")
    return f"File uploaded to  {BUCKET_NAME}//{blob.name}"

  except Exception as e:
    logging.error(f"Error uploading: {e}")
    return f"Error to upload file: {e}"

if __name__ == "__main__":
    get_data(None)