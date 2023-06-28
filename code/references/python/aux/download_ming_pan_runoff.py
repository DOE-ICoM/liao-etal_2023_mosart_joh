import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Path to the service account private key file
credentials_file = '/qfs/people/liao313/google/hexwatershed-b70adb1b4ed5.json'
# Create credentials object from the private key file
credentials = service_account.Credentials.from_service_account_file(
    credentials_file, scopes=['https://www.googleapis.com/auth/drive']
)
def get_file_ids(folder_id):
    # Set up Google Drive API client
    service = build('drive', 'v3', credentials=credentials)

    file_ids = []
    aFileName= []

    # Get the list of files in the shared folder
    results = service.files().list(
        q=f"'{folder_id}' in parents",
        fields="files(id,name)"
    ).execute()

    files = results.get('files', [])
    for file in files:
        aFileName.append(file['name'])
        file_ids.append(file['id'])

    return file_ids,aFileName

# Replace 'FOLDER_ID' with the actual ID of the shared folder
folder_id = '1gG69GOIJQPEGwsfO0zU8zGxL0Ze9hvgP'

# Call the function to get the file IDs
file_ids,aFileName = get_file_ids(folder_id)

# Print the file IDs
for file_id in file_ids:
    print(file_id)

#https://medium.com/@acpanjan/download-google-drive-files-using-wget-3c2c025a8b99

#wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=FILEID' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=FILEID" -O FILENAME && rm -rf /tmp/cookies.txt


#save to a parafly file
sFilename_parafly = '/qfs/people/liao313/jobs/dataset/mingpan_runoff/parafly_download_mingpan.ini'
f_parafly = open(sFilename_parafly, 'w')

sWorkspace_output = "/compyfs/liao313/00raw/ming_pan_runoff"
os.makedirs(sWorkspace_output, exist_ok=True)
nFile= len(file_ids)
for i in range(nFile):
    file_id = file_ids[i]
    FILEID = file_id
    sFilename = aFileName[i]
    FILENAME = sWorkspace_output + '/' +  sFilename
    sSpec = r"\1\n"
    sCommond = "wget --load-cookies ~/tmp/cookies.txt " + '"' + "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies ~/tmp/cookies.txt --keep-session-cookies --no-check-certificate " + "'" +"https://docs.google.com/uc?export=download&id=" + FILEID + "'" + " -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/"+sSpec+"/p')&id=" + FILEID + '"' + " -O " + FILENAME + " && rm -rf /tmp/cookies.txt"
    print(sCommond)
    f_parafly.write(sCommond + '\n')

f_parafly.close()
