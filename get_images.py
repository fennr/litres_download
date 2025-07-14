import os

from selenium.common import exceptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config import URL_BOOKS, URL_LOGIN, BOOK_ID, BOOK_NAME, PAGES, LOGIN, PASSWORD

import time


def check_close(driver):
    """
    wait until user closed browser window
    :param driver:
    :return:
    """
    closed = False
    s = driver.title
    while not closed:
        try:
            s = driver.title
            time.sleep(1)
        except:
            closed = True


def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    # chrome_service = Service("c:/temp/chromedriver.exe")
    chrome_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
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


def load_books(driver):
    print(f"create dir {BOOK_NAME}_{BOOK_ID}")
    if not os.path.exists(f"{BOOK_NAME}_{BOOK_ID}"):
        os.makedirs(f"{BOOK_NAME}_{BOOK_ID}")
    type_file = "jpg"
    driver.get(URL_BOOKS.format(0, "jpg", BOOK_ID))
    if len(driver.find_elements(By.CLASS_NAME, "Error-module__LhUUaG__wrapper")) > 0:
        type_file = "gif"
    time.sleep(2)
    for i in range(PAGES):
        driver.get(URL_BOOKS.format(i, type_file, BOOK_ID))
        time.sleep(2)
        img = driver.find_element(By.TAG_NAME, "img")
        with open(f"{BOOK_NAME}_{BOOK_ID}/{i}.png", "wb") as file:
                file.write(img.screenshot_as_png)



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
