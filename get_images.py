import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config import URL_BOOKS, URL_LOGIN, BOOK_ID, BOOK_NAME, PAGES, LOGIN, PASSWORD

import requests

import time


def check_close(driver):
    """
    wait until user closed browser window
    :param driver:
    :return:
    """
    closed = False
    driver.title
    while not closed:
        try:
            driver.title
            time.sleep(1)
        except Exception:
            closed = True


def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_service = Service(ChromeDriverManager().install())
    driver: WebDriver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return driver


def login_litres(driver):
    driver.get(URL_LOGIN)

    username_in = driver.find_element(by=By.NAME, value='email')
    username_in.click()
    username_in.send_keys(LOGIN)
    username_in.send_keys(Keys.RETURN)
    time.sleep(2)
    password_in = driver.find_element(by=By.NAME, value='pwd')
    password_in.send_keys(PASSWORD)
    time.sleep(1)
    password_in.send_keys(Keys.RETURN)
    time.sleep(2)


def scroll_down(driver):
    count = 0
    while True:
        page = driver.find_element(by=By.TAG_NAME, value="html")

        page.send_keys(Keys.END)
        driver.implicitly_wait(1)
        page.send_keys(Keys.END)
        driver.implicitly_wait(1)
        page.send_keys(Keys.END)
        count += 1
        print(f'scroll down {count}')
        driver.implicitly_wait(1)
        footer = driver.find_element(by=By.CLASS_NAME, value='footer-wrap')
        if footer and footer.is_displayed():
            loader_button = driver.find_element(by=By.ID, value='arts_loader_button')
            if loader_button and not loader_button.is_displayed():
                break

    print(f'scroll down exit after {count} scrolls')


def load_books(driver: WebDriver):
    print(f"create dir {BOOK_NAME}_{BOOK_ID}")
    if not os.path.exists("books"):
        os.mkdir("books")
    if not os.path.exists(f"books/{BOOK_NAME}_{BOOK_ID}"):
        os.makedirs(f"books/{BOOK_NAME}_{BOOK_ID}")
    driver.get(URL_BOOKS.format(0, "jpg", BOOK_ID))
    time.sleep(2)
    session = requests.session()
    for cookie in driver.get_cookies():
        session.cookies.set(
            domain=cookie['domain'],
            name=cookie['name'],
            value=cookie['value'],
            path=cookie['path'],
            secure=cookie['secure'],
        )

    available_file_types = ['jpeg', 'jpg', 'gif']
    file_types_to_check = available_file_types
    saved_file_type = available_file_types[0]
    for i in range(PAGES):
        percent = ((i + 1) / PAGES) * 100
        for index, file_type in enumerate(file_types_to_check):
            src = URL_BOOKS.format(i, file_type, BOOK_ID) 
            resp = session.get(src)
            if resp.status_code == requests.codes.not_found:
                continue
            if resp.status_code != requests.codes.ok:
                time.sleep(2)
                resp = session.get(src)
            resp.raise_for_status()
            if index != 0:
                file_types_to_check = [file_type] + [item for item in available_file_types if item != file_type]
            saved_file_type = file_type
            break
        with open(f"books/{BOOK_NAME}_{BOOK_ID}/{i}.{saved_file_type}", "wb") as f:
            f.write(resp.content)

        if abs(percent - round(percent)) > 0.2:
            print(f"Done: {round(percent, 2)}%")


def litres_loads():
    driver = create_driver()
    driver.maximize_window()
    login_litres(driver)
    load_books(driver)
    time.sleep(1)

    check_close(driver)
    print('FINISH!')


def main():
    litres_loads()


if __name__ == '__main__':
    main()
