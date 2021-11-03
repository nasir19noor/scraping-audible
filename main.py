from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

options = Options()
options.headless = False
# options.add_argument('window-size=1920x1080')

web = "https://www.audible.com/search"
path = 'chromedriver\chromedriver.exe'
driver = webdriver.Chrome(path)
driver.get(web)
driver.maximize_window()

# Pagination
pagination = driver.find_element_by_xpath('//ul[contains(@class, "pagingElements")]')
pages = pagination.find_elements_by_tag_name('li')
last_page = pages[-2].text

book_title = []
book_author = []
book_length = []
current_page = 1

while current_page <= 3:
    time.sleep(2)
    # explicit wait
    container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'adbl-impression-container')))
    # container = driver.find_element_by_class_name("adbl-impression-container")
    products = WebDriverWait(container, 5).until(EC.presence_of_all_elements_located((By.XPATH, './li')))
    # products = container.find_elements_by_xpath('./li')

    for product in products:
        title = product.find_element_by_xpath('.//h3[contains(@class, "bc-heading")]').text
        print(title)
        book_title.append(title)
        author = product.find_element_by_xpath('.//li[contains(@class, "authorLabel")]').text
        print(author)
        book_author.append(author)
        length = product.find_element_by_xpath('//li[contains(@class, "runtimeLabel")]').text
        print(length)
        book_length.append(length)
    current_page += 1
    try:
        next_page = driver.find_element_by_xpath('//span[contains(@class, "nextButton")]')
        next_page.click()
    except:
        pass

df_books = pd.DataFrame({'title': book_title, 'author': book_author, 'length': book_length})
df_books.to_csv(f'books/books_total.csv')
df_books.to_json(f'books/books_total.json')
driver.quit()