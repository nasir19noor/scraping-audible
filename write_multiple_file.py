from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

options = Options()
options.headless = False
# options.add_argument('window-size=1920x1080')

web = "https://www.audible.com/search"
path = 'chromedriver\chromedriver.exe'
driver = webdriver.Chrome(path, options=options)
driver.get(web)
driver.maximize_window()

# Pagination
pagination = driver.find_element_by_xpath('//ul[contains(@class, "pagingElements")]')
pages = pagination.find_elements_by_tag_name('li')
last_page = pages[-2].text


# next_page.click

current_page = 1

while current_page <= int(last_page):
    # path = 'chromedriver\chromedriver.exe'
    # driver = webdriver.Chrome(path, options=options)
    driver.get(f'{web}?page={current_page}')
    driver.maximize_window()
    container = driver.find_element_by_class_name("adbl-impression-container")
    products = container.find_elements_by_xpath('./li')

    book_title = []
    book_author = []
    book_length = []

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
    print(book_title)
    print(book_author)
    print(book_length)

    df_books = pd.DataFrame({'title': book_title, 'author': book_author, 'length': book_length})
    df_books.to_csv(f'books/books_{current_page}.csv')
    df_books.to_json(f'books/books_{current_page}.json')

    current_page += 1
    try:
        next_page = driver.find_element_by_xpath('//span[contains(@class, "nextButton")]')
        next_page.click
    except:
        pass

driver.quit()