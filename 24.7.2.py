import os
from api import PetFriends
from settings import valid_email, valid_password
from tests.tests_pet_friends import pf

TestPetFriend = PetFriends()


# 1. Получение ключа авторизации без пароля
def test_get_api_key_without_password(email=valid_email, passwd=''):
    """Получение ключа авторизации без пароля. Статус 403 - Forbidden"""

    status, result = pf.get_api_key(email, passwd)
    assert status == 403
    assert 'key' not in result


# 2. Получение ключа авторизации без эмейла
def test_get_api_key_without_email(email='', passwd=valid_password):
    """Получение ключа авторизации без эмейла. Статус 403 - Forbidden"""

    status, result = pf.get_api_key(email, passwd)
    assert status == 403
    assert 'key' not in result


# 3. Добавление питомца без авторизации
def test_add_new_pet_without_auth(name='Джек', animal_type='собака', age='9'):
    """Добавление питомца без авторизации. Статус 403 - Forbidden"""

    auth = ''

    status, result = pf.add_new_pet_simple(auth, name, animal_type, age)
    assert status == 403


# 4. Изменение данных о питомце - пустое имя
def test_update_pet_without_name(name='', animal_type='кот', age='3', filter='my_pets'):
    """Изменение питомца - пустое имя. Статус 400 ошибка в данных, т.к. имя - required"""

    _, res_auth = pf.get_api_key(valid_email, valid_password)
    auth = res_auth['key']

    _, _, pet_id = pf.get_pet_list_and_last_id(auth, filter)
    if pet_id != 0:
        status, result = pf.update_pet_by_id(auth, pet_id, name, animal_type, age)
        assert status == 400
    else:
        raise Exception("Нет моих питомцев")


# 5. Добавление питомца без имени
def test_add_new_pet_without_name(name='', animal_type='кот', age='1'):
    """Добавление питомца без имени. Статус 400 ошибка в данных, т.к. имя - required"""

    status, res_auth = pf.get_api_key(valid_email, valid_password)
    auth = res_auth['key']

    status, result = pf.add_new_pet_simple(auth, name, animal_type, age)
    assert status == 400


# 6. Добавление питомца без типа
def test_add_new_pet_without_type(name='Неизвестный кот', animal_type='', age='5'):
    """Добавление питомца без типа. Статус 400 ошибка в данных, т.к. тип - required"""

    status, res_auth = pf.get_api_key(valid_email, valid_password)
    auth = res_auth['key']

    status, result = pf.add_new_pet_simple(auth, name, animal_type, age)
    assert status == 400


# 7. Добавление питомца с отрицательным возрастом
def test_add_new_pet_without_negative_age(name='Джек < 0', animal_type='собака', age='-1'):
    """Добавления питомца с отрицательным возрастом. Статус 400 ошибка в данных, т.к. возраст не может быть отрицательным"""

    status, res_auth = pf.get_api_key(valid_email, valid_password)
    auth = res_auth['key']

    status, result = pf.add_new_pet_simple(auth, name, animal_type, age)
    assert status == 400


# 8. Добавление питомца - возраст прописан текстом
def test_add_new_pet_without_age_not_number(name='Джек', animal_type='собака', age='один год'):
    """Добавление питомца с возрастом = текстом. Статус 400 ошибка в данных"""

    status, res_auth = pf.get_api_key(valid_email, valid_password)
    auth = res_auth['key']

    status, result = pf.add_new_pet_simple(auth, name, animal_type, age)
    assert status == 400


# 9. Добавление питомца с возрастом > int65
def test_add_new_pet_with_too_much_age(name='Дедушка-Джек', animal_type='собака', age=(2 ** 65 + 1)):
    """Добавление питомца с почтенным возрастом. Статус 400 ошибка в данных"""

    status, res_auth = pf.get_api_key(valid_email, valid_password)
    auth = res_auth['key']

    status, result = pf.add_new_pet_simple(auth, name, animal_type, age)
    assert status == 400


# 10. Добавление фото питомца в текстовом формате, вместо jpg
def test_add_photo_of_pet_txt_file(pet_photo='dog.txt', filter='my_pets'):
    """Добавление фото питомца - указан текстовый файл, вместо jpg. Статус - 500 ошибка"""

    _, res_auth = pf.get_api_key(valid_email, valid_password)
    auth = res_auth['key']

    _, _, pet_id = pf.get_pet_list_and_last_id(auth, filter)

    pet_photo = os.path.join(os.path.dirname(__file__), 'images', pet_photo)

    if pet_id != 0:

        # Добавляем фото
        status, result = pf.add_pets_photo(auth, pet_id, pet_photo)
        assert status == 500
    else:
        raise Exception("Нет моих питомцев")
