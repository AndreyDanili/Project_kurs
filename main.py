import VK

if __name__ == '__main__':
    VK.VkUser.backup_photo(VK.VkUser(input(f'Введите ID пользователя: '), input(f'Введите токен с Полигона Яндекс.Диска: ')))
