# TLP-Translator

This simple script helps you translate all Microsoft Office documents and PDF in a folder recursively.
For my use case, I run this script target to a share drive (Onedrive), translate all files, and saves it back to another folder.

## Setup

### Local Python
For Windows, install Python 3, and open powershell run
```
.\setup.bat
```
It creates Python virtual environment in .venv folder.

### Google Cloud Platform 
1. Setup gcloud cli https://cloud.google.com/sdk/docs/install#windows (Just use the installer.)
2. Run ```gcloud init``` and you can pick any setup as the Python code will set region and project ID.
3. Run ```gcloud auth application-default login```


## Using the script
Open translate.py, and change the constant.
```
# Constants
PROJECT_ID = "cyrus-testing-2023"
TARGET_LOCALE = "zh-TW"
SOURCE_PATH = r"C:\Users\cyrus\OneDrive - Vocational Training Council - Staff\AY2324_Validation_VQ"
DESTINATION_PATH = os.path.join(
    r"C:\Users\cyrus\OneDrive - Vocational Training Council - Staff\Translated TLP\\", TARGET_LOCALE
)
```
TARGET_LOCALE please check https://cloud.google.com/translate/docs/languages?_gl=1*gflylq*_up*MQ..&gclid=Cj0KCQjwlvW2BhDyARIsADnIe-LB58TQscwOoPpASZ3yx9Twr2cnrVqzca5tzjY6GBpG0TG1BHzr_28aAl0AEALw_wcB&gclsrc=aw.ds 

Activates the virtual environment and run translate.py
```
.venv\Scripts\activate
python .\translate.py
```
