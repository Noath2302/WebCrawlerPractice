from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import re
import json
webpage = "https://de.polene-paris.com"
base_url = "https://de.polene-paris.com/collections/all"

def get_link(clearfix):
    try:
        all_links = [a_tag.get('href') for a_tag in clearfix.find_all('a')]
        return webpage+min(all_links,key=len)
    except Exception as e:
        return str(e)

def get_name(description):
    try:
        name = description.find('h3',class_='ts-label-s').text
        return name
    except Exception as e:
        return str(e)

def get_current_price(prices):
    try:
        current_price = prices.find('span',class_=['ts-label-s price-label']).text
        return current_price
    except Exception as e:
        return str(e)

def get_original_price(prices):
    try:
        original_price = prices.find('span',class_=['sp2p normal-price-crossedout']).text
        return original_price
    except Exception as e:
        return str(e)

def get_saving(prices):
    try:
        saving = prices.find('span',class_='product-price-savings').text
        return saving
    except Exception as e:
        return str(e)

def get_description(description):
    try:
        return description.find('p',class_=['ts-label-s','edition-label','ts-grey']).text
    except Exception as e:
        return str(e)
def get_data(product):
    df_dict = {}
    #df_dict["link"] = get_link(product.find('div',class_='clearfix'))
    df_dict["name"] = get_name(product)
    df_dict["current_price"] = get_current_price(product)
    df_dict["description"] = get_description(product)
    return df_dict

def get_page(url):
    options = webdriver.EdgeOptions()
    driver = webdriver.Edge(options=options)
    driver.get(url)
    region_acceptance = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'spicegems_cr_btn_no')))
    region_acceptance.click()
    cookies_acceptance = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '.cc-btn.cc-allow.isense-cc-btn.isense-cc-allow.isense-cc-submit-consent')))
    cookies_acceptance.click()
    page = driver.page_source
    driver.close()
    return page


output_products = []

current_page = get_page(base_url)
soup = bs(current_page,features="html.parser")
product_list = soup.find_all('article',class_=['product-card js-card is-animation-card'])
for product in product_list:
    adding_df = get_data(product)
    output_products.append(adding_df)

with open("Polene.json", "w") as final:
    json.dump(output_products, final)
