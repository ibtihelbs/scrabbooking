from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

driver = webdriver.Chrome()
driver.get("https://books.toscrape.com/")

all_data = []
rating_map = {"One":1,"Two":2,"Three":3,"Four":4,"Five":5}

while True:
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, '//article[@class="product_pod"]')
        )
    )

    books = driver.find_elements(By.XPATH, '//article[@class="product_pod"]')

    for book in books:
        title = book.find_element(By.XPATH, './/h3/a').get_attribute('title')
        price = float(book.find_element(By.XPATH, './/p[@class="price_color"]').text.replace('£',''))
        link = book.find_element(By.XPATH, './/h3/a').get_attribute('href')
        rating = rating_map.get(
            book.find_element(By.XPATH, './/p[contains(@class,"star-rating")]')
            .get_attribute('class').split()[-1]
        )
        stock = "In stock" in book.find_element(
            By.XPATH, './/p[contains(@class,"instock")]'
        ).text

        all_data.append([title, price, rating, stock, link])

    # try to go to next page
    try:
        next_btn = driver.find_element(By.XPATH, '//li[@class="next"]/a')
        next_btn.click()
    except:
        break  # no more pages

df = pd.DataFrame(
    all_data,
    columns=["title", "price", "rating", "in_stock", "link"]
)

print("Total books:", len(df))
df.to_csv("books_all.csv", index=False)

driver.quit()
