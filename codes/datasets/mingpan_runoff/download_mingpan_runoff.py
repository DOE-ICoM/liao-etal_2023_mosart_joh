import os
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
# Path to the service account private key file
credentials_file = '/qfs/people/liao313/google/hexwatershed-b70adb1b4ed5.json'
# Create credentials object from the private key file
credentials = service_account.Credentials.from_service_account_file(
    credentials_file, scopes=['https://www.googleapis.com/auth/drive']
)

service = build('drive', 'v3', credentials=credentials)
def get_file_ids(sFolderID):
    # Set up Google Drive API client
    
    aFileID = []
    aFileName= []

    # Get the list of files in the shared folder
    results = service.files().list(
        q=f"'{sFolderID}' in parents",
        fields="files(id,name)"
    ).execute()

    files = results.get('files', [])
    for file in files:
        aFileName.append(file['name'])
        aFileID.append(file['id'])

    return aFileID, aFileName



def download_file(sFileID, sFilename_out):
    """Downloads a file
    Args:
        sFileID: ID of the file to download
   
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    #creds, _ = google.auth.default()

    try:
        # create drive api client
        #service = build('drive', 'v3', credentials=credentials)
        # pylint: disable=maybe-no-member
        request = service.files().get_media(fileId=sFileID)
        #file = io.BytesIO()
        with io.FileIO(sFilename_out, 'wb') as file:
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(F'Download {int(status.progress() * 100)}.')

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    
# Replace 'FOLDER_ID' with the actual ID of the shared folder
sFolderID = '1gG69GOIJQPEGwsfO0zU8zGxL0Ze9hvgP'
# Call the function to get the file IDs
aFileID, aFileName = get_file_ids(sFolderID)

#https://medium.com/@acpanjan/download-google-drive-files-using-wget-3c2c025a8b99

#wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=FILEID' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=FILEID" -O FILENAME && rm -rf /tmp/cookies.txt

sWorkspace_output = "/compyfs/liao313/00raw/mingpan_runoff"
os.makedirs(sWorkspace_output, exist_ok=True)
nFile= len(aFileID)

aYear = list()
for i in range(nFile):
    sFilename = aFileName[i]
    sDummy = os.path.splitext(sFilename)[0]
    sYear = int(sDummy[-4:])
    aYear.append(sYear)

#sort by year and save the index 
aIndex = sorted(range(len(aYear)), key=lambda k: aYear[k])

for i in range(nFile):
    sFileID = aFileID[i]
    sFilename = aFileName[i]
    sDummy = os.path.splitext(sFilename)[0]
    sYear = sDummy[-4:]
    sFilename_out = sWorkspace_output + '/' +  sFilename
    print(sFilename_out)
    download_file(sFileID, sFilename_out )

    
