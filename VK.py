import Yandex
import json
import requests
from io import BytesIO
from tqdm import tqdm
from datetime import datetime


class VkUser:
    url = 'https://api.vk.com/method/'
    list_photo = []

    def __init__(self, user_id, token_yandex):
        self.token_yandex = token_yandex
        self.user_id = user_id
        self.params = {
            'access_token': 'token_VK',
            'v': '5.131'
        }

    def backup_photo(self):
        if not self.user_id.isdigit():
            self.user_id = VkUser.get_user_id(self)
        url = self.url + 'photos.get'
        url_params = {
            'owner_id': self.user_id,
            'album_id': 'profile',
            'extended': 1
        }
        Yandex.YaUploader.create_folder(Yandex.YaUploader(self.token_yandex), 'Backup_photo')
        photos_profile = requests.get(url, params={**self.params, **url_params}).json()['response']['items']
        count_photos = requests.get(url, params={**self.params, **url_params}).json()['response']['count']
        VkUser.upload_user_photos(self, photos_profile, count_photos)
        with open('information.json', 'w') as file:
            json.dump(VkUser.list_photo, file)
        print('Загрузка файла information.json...')
        Yandex.YaUploader.upload_file(Yandex.YaUploader(self.token_yandex), 'information.json')
        return

    def upload_user_photos(self, photos_profile, count_photos):
        count = count_photos
        if count_photos >= 5:
            count = 5
        print(f'В профиле найдено {count_photos} фото, будет сохранено {count} последних.')
        photos_profile.reverse()
        for photo in tqdm(photos_profile[:count], colour='blue', desc=f"Загрузка фотографий профиля ID {self.user_id}"):
            dict_photo = {'file_name': f"{photo['likes']['count']}.jpg"}
            for photo_name in VkUser.list_photo:
                if dict_photo['file_name'] == photo_name['file_name']:
                    dict_photo['file_name'] = f"{datetime.utcfromtimestamp(photo['date']).strftime('%d_%m_%Y')}.jpg"
            dict_photo['size'] = photo['sizes'][-1]['type']
            VkUser.list_photo.append(dict_photo)
            url_photo = photo['sizes'][-1]['url']
            image = requests.get(url_photo)
            image_content = BytesIO(image.content)
            Yandex.YaUploader.upload_remote_photo(Yandex.YaUploader(self.token_yandex), dict_photo['file_name'], image_content)
        return

    def get_user_id(self):
        url = self.url + 'utils.resolveScreenName'
        url_params = {
            'screen_name': self.user_id
        }
        user_id = requests.get(url, params={**self.params, **url_params}).json()['response']['object_id']
        return user_id
