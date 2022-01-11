import json
from io import BytesIO
import requests
from tqdm import tqdm


class VkUser:
    url = 'https://api.vk.com/method/'
    list_photo = []

    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def get_photos_profile(self, user_id):
        url = self.url + 'photos.get'
        list_friends_id = VkUser.get_friends(self, user_id)
        for friend_id in tqdm(list_friends_id, colour='blue', desc=f"Загрузка фотографий профиля 5 друзей ID{user_id}"):
            url_params = {
                'owner_id': friend_id,
                'album_id': 'profile',
                'extended': 1
                }
            friend_photo_profile = requests.get(url, params={**self.params, **url_params}).json()
            VkUser.upload_last_user_photo(friend_photo_profile)
        with open('information.json', 'w') as file:
            json.dump(VkUser.list_photo, file)
        print('Загрузка файла information.json...')
        YaUploader.upload_file(ya_user, 'information.json')
        return

    @staticmethod
    def upload_last_user_photo(user_photo_profile):
        dict_photo = {'file_name': f"{user_photo_profile['response']['items'][-1]['likes']['count']}.jpg"}
        for photo in VkUser.list_photo:
            if dict_photo['file_name'] == photo['file_name']:
                dict_photo['file_name'] = f"{user_photo_profile['response']['items'][-1]['date']}.jpg"
        dict_photo['size'] = user_photo_profile['response']['items'][-1]['sizes'][-1]['type']
        VkUser.list_photo.append(dict_photo)
        url_photo = user_photo_profile['response']['items'][-1]['sizes'][-1]['url']
        photo = requests.get(url_photo)
        photo_content = BytesIO(photo.content)
        YaUploader.upload_remote_photo(ya_user, dict_photo['file_name'], photo_content)
        return

    def get_friends(self, user_id):
        url = self.url + 'friends.get'
        url_params = {
            'user_id': user_id,
            'order': 'random',
            'extended': 1,
            'count': 5
            }
        result = requests.get(url, params={**self.params, **url_params}).json()['response']['items']
        return result


class YaUploader:
    def __init__(self, token: str):
        self.token = token

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

    def upload_remote_photo(self, file_name: str, photo_content):
        href = self._get_upload_link(disk_file_path=f'Нетология/{file_name}').get("href", "")
        requests.put(href, files={'file': photo_content})

    def upload_file(self, file_name: str):
        href = self._get_upload_link(disk_file_path=f'Нетология/{file_name}').get("href", "")
        response = requests.put(href, data=open(file_name, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print("Success")


vk_user = VkUser('token_vk', '5.131')
ya_user = YaUploader('token_yandex')
VkUser.get_photos_profile(vk_user, '260337')
