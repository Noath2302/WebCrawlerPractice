from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
webpage = "https://www.medpex.de"
base_url = "https://www.medpex.de/top-angebote/"

def get_link(clearfix):
    try:
        all_links = [a_tag.get('href') for a_tag in clearfix.find_all('a')]
        return webpage+min(all_links,key=len)
    except Exception as e:
        return str(e)

def get_name(description):
    try:
        name = description.find('span',class_='product-name').text
        return name
    except Exception as e:
        return str(e)

def get_current_price(prices):
    try:
        current_price = prices.find('span',class_=['normal-price','middle-valign']).text
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
        return description.text
    except Exception as e:
        return str(e)
def get_data(product):
    df = pd.DataFrame()
    df_dict = {}
    df_dict["link"] = get_link(product.find('div',class_='clearfix'))
    df_dict["name"] = get_name(product.find('div',class_='description'))
    df_dict["current_price"] = get_current_price(product.find('div',class_='prices'))
    df_dict["original_price"] = get_original_price(product.find('div',class_='prices'))
    df_dict["saving"] = get_saving(product.find('div',class_='prices'))
    df_dict["description"] = get_description(product.find('div',class_='description'))
    df = pd.DataFrame.from_dict([df_dict])
    return df

def get_page(url):
    options = webdriver.EdgeOptions()
    driver = webdriver.Edge(options=options)
    driver.get(url)
    cookies_acceptance = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '.cmpboxbtn.cmpboxbtnyes.cmptxt_btn_yes')))
    cookies_acceptance.click()
    page = driver.page_source
    driver.close()
    return page


page = get_page(base_url)
number_of_page_pat = r"Seite [0-9]{1,2} von ([0-9]{1,2})"
max_number_of_page = max([int(i) for i in re.findall(number_of_page_pat,page)])

current_page_index = 1
df = pd.DataFrame()
while (current_page_index <= max_number_of_page):
    current_page = get_page(base_url+str(current_page_index))
    soup = bs(current_page)
    product_list_all = soup.find('div',id="product-list")
    product_list = product_list_all.find_all('div',class_=['product-list-entry data-tracking-product'])
    for product in product_list:
        adding_df = get_data(product)
        df=pd.concat([df, adding_df])
    current_page_index+=1

df.to_excel('output.xlsx',index=False)
