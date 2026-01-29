from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

web = 'https://books.toscrape.com/'

# Chrome options
options = Options()
options.add_argument("--start-maximized")

# Creating the driver (NO chromedriver path)
driver = webdriver.Chrome(options=options)
driver.get(web)
books = driver.find_elements(By.XPATH, '//article[@class="product_pod"]')

data = []

for book in books:
    title = book.find_element(By.XPATH, './/h3/a').get_attribute('title')
    price = book.find_element(By.XPATH, './/p[@class="price_color"]').text
    link = book.find_element(By.XPATH, './/h3/a').get_attribute('href')
    rating = book.find_element(By.XPATH, './/p[contains(@class,"star-rating")]').get_attribute('class').split()[-1]
    stock = book.find_element(By.XPATH, './/p[contains(@class,"instock")]').text.strip()
    image = book.find_element(By.XPATH, './/img').get_attribute('src')

    data.append([title, price, rating, stock, link, image])

df = pd.DataFrame(data, columns=["title", "price", "rating", "stock", "link", "image"])
df.to_csv("books-2.csv", index=False)
df.to_json("books-2.json", orient="records")

driver.quit()