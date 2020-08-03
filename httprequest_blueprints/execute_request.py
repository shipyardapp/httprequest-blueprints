import argparse
import requests
import os


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--method', dest='method', required=True,
                        choices={'GET', 'POST', 'PUT'})
    parser.add_argument('--url', dest='url', required=True)
    parser.add_argument('--authorization-header', dest='authorization_header',
                        required=False, default=None)
    parser.add_argument('--message', dest='message', required=False)
    parser.add_argument(
        '--print-response',
        dest='print_response',
        default='FALSE',
        choices={
            'TRUE',
            'FALSE'},
        required=False)
    parser.add_argument(
        '--destination-file-name',
        dest='destination_file_name',
        default='response.txt',
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


def main():
    args = get_args()
    method = args.method
    url = args.url
    authorization_header = args.authorization_header
    message = args.message
    print_response = convert_to_boolean(args.print_response)
    destination_file_name = args.destination_file_name
    destination_folder_name = clean_folder_name(args.destination_folder_name)
    destination_name = combine_folder_and_file_name(
        destination_folder_name, destination_file_name)

    if not os.path.exists(destination_folder_name) and (
            destination_folder_name != ''):
        os.makedirs(destination_folder_name)

    header = {}
    if authorization_header:
        header = {'Authorization': authorization_header}

    try:
        if method == 'GET':
            req = requests.get(url, headers=header)
        elif method == 'POST':
            req = requests.post(url, headers=header, data=message)
        elif method == 'PUT':
            req = requests.put(url, headers=header, data=message)
    except Exception as e:
        print(f'Failed to execute {method} request to {url}')
        raise(e)

    with open(destination_name, 'w') as response_output:
        response_output.write(req.text)

    print(
        f'Successfully sent request {url} and stored response to {destination_name}.')

    if print_response:
        print(f'\n\n Response body: {req.content}')


if __name__ == '__main__':
    main()
