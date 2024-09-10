import os
from pathlib import Path
from google.cloud import translate_v3beta1 as translate

# Constants
PROJECT_ID = "cyrus-testing-2023"
TARGET_LOCALE = "zh-TW"
SOURCE_PATH = r"C:\Users\cyrus\OneDrive - Vocational Training Council - Staff\AY2324_Validation_VQ"
DESTINATION_PATH = os.path.join(
    r"C:\Users\cyrus\OneDrive - Vocational Training Council - Staff\Translated TLP\\", TARGET_LOCALE
)


DOCUMENT_MIME_TYPES = {
    "DOC": {"MIME Type": "application/msword", "Output": ["DOC", "DOCX"]},
    "DOCX": {"MIME Type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "Output": ["DOCX"]},
    "PDF": {"MIME Type": "application/pdf", "Output": ["PDF"]},
    "PPT": {"MIME Type": "application/vnd.ms-powerpoint", "Output": ["PPT", "PPTX"]},
    "PPTX": {"MIME Type": "application/vnd.openxmlformats-officedocument.presentationml.presentation", "Output": ["PPTX"]},
    "XLS": {"MIME Type": "application/vnd.ms-excel", "Output": ["XLS", "XLSX"]},
    "XLSX": {"MIME Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "Output": ["XLSX"]},
}

def translate_document(project_id: str, file_path: str, target_locale: str) -> translate.TranslationServiceClient:
    """Translates a document.

    Args:
        project_id: The GCP project ID.
        file_path: The path to the file to be translated.
        target_locale: The target language locale.

    Returns:
        The translated document.
    """
    client = translate.TranslationServiceClient()
    location = "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    with open(file_path, "rb") as document:
        document_content = document.read()

    file_extension = os.path.splitext(file_path)[1][1:].upper()
    mime_type = DOCUMENT_MIME_TYPES.get(file_extension, {}).get("MIME Type", "")

    document_input_config = {"content": document_content, "mime_type": mime_type}

    response = client.translate_document(
        request={
            "parent": parent,
            "target_language_code": target_locale,
            "document_input_config": document_input_config,
            "is_translate_native_pdf_only": True
        }
    )

    print(f"Translated {file_path}, Detected Language Code - {response.document_translation.detected_language_code}")
    return response

def list_files_recursive(path: str) -> list:
    """Recursively lists all files in a directory.

    Args:
        path: The root directory path.

    Returns:
        A list of file paths.
    """
    file_list = []
    for root, _, files in os.walk(path):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

def filter_files(file_list: list) -> list:
    """Filters files based on supported document types.

    Args:
        file_list: The list of file paths.

    Returns:
        A filtered list of file paths.
    """
    return [file_path for file_path in file_list if Path(file_path).suffix[1:].upper() in DOCUMENT_MIME_TYPES.keys()]

def main():
    file_list = list_files_recursive(SOURCE_PATH)
    filtered_file_list = filter_files(file_list)

    for source_file_path in filtered_file_list:
        print(f"Source file: {source_file_path}")
        relative_path = os.path.relpath(source_file_path, SOURCE_PATH)
        destination_file_path = os.path.join(DESTINATION_PATH, relative_path)

        if os.path.exists(destination_file_path):
            continue

        os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)

        try:
            response = translate_document(PROJECT_ID, source_file_path, TARGET_LOCALE)
            with open(destination_file_path, "wb") as output_file:
                output_file.write(response.document_translation.byte_stream_outputs[0])
        except Exception as e:
            print(f"An error occurred while translating {source_file_path}: {str(e)}")
            with open("error.log", "a", encoding="utf-8", errors="ignore") as error_file:
                error_file.write(f"{source_file_path}\n") 
            error_log_path = os.path.join(os.path.dirname(destination_file_path), "error.log")
            if os.path.exists(error_log_path):
                with open(error_log_path, "r", encoding="utf-8", errors="ignore") as error_file:
                    if source_file_path in error_file.read():
                        continue
            with open(error_log_path, "a", encoding="utf-8", errors="ignore") as error_file:
                error_file.write(f"{source_file_path}\n")

if __name__ == "__main__":
    main()