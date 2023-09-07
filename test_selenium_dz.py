import pytest
from selenium.webdriver.common.by import By
from settings import valid_email, valid_password
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.mark.test_show_all_pets
def test_show_all_pets(driver):
    driver.get('https://petfriends.skillfactory.ru/login')
    # Вводим email, заменить на свой email для того чтобы получить свой список питомцев
    driver.find_element(By.ID, 'email').send_keys(valid_email)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Ждем когда окажемся на главной странице пользователя
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, 'h1'), 'PetFriends')
    )

    driver.get('https://petfriends.skillfactory.ru/my_pets')

    # ожидание появления хотя бы одного элемента питомца
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr'))
    )

    # список всех обьектов питомца , в котром есть атрибут ".text" с помощью которого,
    # можно получить информацию о питомце в виде строки: 'Мурзик Котэ 5'
    all_my_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr')

    # проверяем что список своих питомцев не пуст
    assert len(all_my_pets) > 0

def test_all_pets_have_name_type_age(driver):
    driver.get('https://petfriends.skillfactory.ru/login')
    # Вводим email, заменить на свой email для того чтобы получить свой список питомцев
    driver.find_element(By.ID, 'email').send_keys(valid_email)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Ждем когда окажемся на главной странице пользователя
    WebDriverWait(driver, 11).until(
        EC.text_to_be_present_in_element((By.TAG_NAME, 'h1'), 'PetFriends')
    )
    # Проверяем, что мы оказались на главной странице пользователя
    # assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    driver.implicitly_wait(10)

    driver.get('https://petfriends.skillfactory.ru/my_pets')

    # список всех обьектов имен питомца , в котром есть атрибут ".text" с помощью которого,
    # можно получить имя питомца в виде строки: 'Мурзик'
    all_pets_names = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr/td[1]')

    # список всех обьектов пород питомца , в котром есть атрибут ".text" с помощью которого,
    # можно получить информацию о питомце в виде строки: 'Котэ'
    all_pets_types = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr/td[2]')

    # список всех обьектов возраста питомца , в котром есть атрибут ".text" с помощью которого,
    # можно получить информацию о питомце в виде строки: '5'
    all_pets_ages = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody/tr/td[3]')

    # проверяем что списоки своих питомцев не пусты и равны
    assert len(all_pets_names) > 0
    assert len(all_pets_types) > 0
    assert len(all_pets_ages) > 0
    assert len(all_pets_names) == len(all_pets_types) == len(all_pets_ages)

    f = True
    for i in range(len(all_pets_names)):
        # получаем информацию о питомце из списка всех своих питомцев
        pet_name = all_pets_names[i].text
        pet_type = all_pets_types[i].text
        pet_age = all_pets_ages[i].text

        # если в списке есть пустое значение переменнтая f принимает значение ложь
        if pet_name == '': f = False
        if pet_type == '': f = False
        if pet_age == '': f = False

    # проверяем что у всех питомцев есть имя, возраст и порода
    assert f == True