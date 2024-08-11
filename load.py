from googleapiclient.discovery import build
import requests
from pinecone import Pinecone
import os
from dotenv import load_dotenv

load_dotenv()
# Hugging Face API setup
HF_API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"
HF_headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"}
os.environ['PINECONE_API_KEY']=os.getenv('PINECONE_API_KEY')
pc = Pinecone()
index = pc.Index('videos')

def get_embedding(text):
    response = requests.post(HF_API_URL, headers=HF_headers, json={"inputs": text})
    if response.status_code == 200:
        return response.json()  # The API returns a list of lists, we want the first (and only) embedding
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

def list_files_and_add_to_pinecone(google_api_key, folder_id):
    # Build the Drive API client with the API key
    service = build('drive', 'v3', developerKey=google_api_key)

    # Query to search for files in the specific folder
    query = f"'{folder_id}' in parents and trashed=false"

    # List files in the folder
    results = service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
        return

    print('Processing files:')
    for item in items:
        file_name = item['name']
        file_id = item['id']
        print(f"Processing: {file_name}")

        try:
            # Get embedding for the file name
            embedding = get_embedding(file_name)

            # Add to Pinecone
            index.upsert(vectors=[(file_id, embedding, {"name": file_name})])

            print(f"Added {file_name} to Pinecone")
        except Exception as e:
            print(f"Error processing {file_name}: {e}")

    print("Finished processing all files")

# Usage
google_api_key = os.getenv('GOOGLE_API_KEY')
folder_id = os.getenv('YOUR_FOLDER_ID')
list_files_and_add_to_pinecone(google_api_key, folder_id)