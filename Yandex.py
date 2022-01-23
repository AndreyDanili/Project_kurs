import requests


class YaUploader:
    def __init__(self, token_yandex):
        self.token = token_yandex

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload_remote_photo(self, file_name: str, image_content):
        href = self._get_upload_link(disk_file_path=f'Backup_photo/{file_name}').get("href", "")
        requests.put(href, files={'file': image_content})

    def upload_file(self, file_name: str):
        href = self._get_upload_link(disk_file_path=f'Backup_photo/{file_name}').get("href", "")
        response = requests.put(href, data=open(file_name, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print("Success")

    def create_folder(self, folder_name):
        href = 'https://cloud-api.yandex.net/v1/disk/resources?' + f'path={folder_name}'
        headers = self.get_headers()
        response = requests.put(href, headers=headers)
        if response.status_code == 201:
            return print(f'Папка "Backup_photo" создана')
        elif response.status_code == 409:
            return print(f'Папка "Backup_photo" была создана ранее')
        else:
            print('Ошибка создания папки')
        print(response)
