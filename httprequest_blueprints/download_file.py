import argparse
import requests
import os
import shutil


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', dest='url', required=True)
    parser.add_argument('--authorization-header', dest='authorization_header',
                        required=False, default=None)
    parser.add_argument(
        '--destination-file-name',
        dest='destination_file_name',
        default='',
        required=False)
    parser.add_argument(
        '--destination-folder-name',
        dest='destination_folder_name',
        default='',
        required=False)
    args = parser.parse_args()
    return args


def combine_folder_and_file_name(folder_name, file_name):
    """
    Combine together the provided folder_name and file_name into one path variable.
    """
    combined_name = os.path.normpath(
        f'{folder_name}{"/" if folder_name else ""}{file_name}')
    combined_name = os.path.normpath(combined_name)

    return combined_name


def clean_folder_name(folder_name):
    """
    Cleans folders name by removing duplicate '/' as well as leading and trailing '/' characters.
    """
    folder_name = folder_name.strip('/')
    if folder_name != '':
        folder_name = os.path.normpath(folder_name)
    return folder_name


def convert_to_boolean(string):
    """
    Shipyard can't support passing Booleans to code, so we have to convert
    string values to their boolean values.
    """
    if string in ['True', 'true', 'TRUE']:
        value = True
    else:
        value = False
    return value


def extract_filename_from_url(url):
    file_name = url.split('/')[-1]
    return file_name


def download_file(url, destination_name):
    print(f'Currently downloading the file from {url}...')
    with requests.get(url, stream=True) as r:
        with open(destination_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=(16 * 1024 * 1024)):
                f.write(chunk)
    print(f'Successfully downloaded {url} to {destination_name}.')
    return


def add_to_header(header, key, value):
    header[key] = value
    return header


def create_folder_if_dne(destination_folder_name):
    if not os.path.exists(destination_folder_name) and (
            destination_folder_name != ''):
        os.makedirs(destination_folder_name)


def main():
    args = get_args()
    url = args.url
    authorization_header = args.authorization_header
    destination_file_name = args.destination_file_name
    if not destination_file_name:
        destination_file_name = extract_filename_from_url(url)
    destination_folder_name = clean_folder_name(args.destination_folder_name)
    destination_name = combine_folder_and_file_name(
        destination_folder_name, destination_file_name)
    header = {}

    create_folder_if_dne(destination_folder_name)

    if authorization_header:
        header = add_to_header(header, 'Authorization', authorization_header)

    download_file(url, destination_name)


if __name__ == '__main__':
    main()
