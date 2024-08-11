from googleapiclient.discovery import build

def list_files_in_folder(api_key, folder_id):
    # Build the Drive API client with the API key
    service = build('drive', 'v3', developerKey=api_key)

    # Query to search for files in the specific folder
    query = f"'{folder_id}' in parents and trashed=false"

    # List files in the folder
    results = service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])

    # Print the list of file names
    li=[]
    if not items:
        print('No files found.')
    else:
        print('Files in folder:')
        for item in items:
            li.append(item['name'])
    print(li)


list_files_in_folder(api_key, folder_id)
