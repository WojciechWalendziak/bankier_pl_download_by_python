
import time
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

i = 0
check = 0
counter = 0
duns_counter = 0
table_list = []
last_financial_year_list = []
duns_list = []

driver = webdriver.Chrome(ChromeDriverManager().install())
time.sleep(3)

try:
    driver.get('https://www.bankier.pl/gielda/notowania/akcje')
    time.sleep(5)
except:
    print('page loading failed')

try:
    cookie_box = driver.find_element(By.ID, 'onetrust-button-group')
except:
    print('cookie window not found')

try:
    cookie_accept_button = cookie_box.find_element(By.ID, 'onetrust-accept-btn-handler')
    cookie_accept_button.click()
    time.sleep(5)
except:
    print('cookie button click failed')

try:
    selectors_boxes = driver.find_elements(By.CLASS_NAME, 'onChangeFormSubmit')
    time.sleep(2)
except:
    print('onChangeFormSubmit class not found')

try:
    for selectors_box in selectors_boxes:
        selector_tag = selectors_box.find_element(By.TAG_NAME, 'label')
        if selector_tag.get_attribute('innerHTML').strip() == 'Indeks:':
            print('searched dropdown found')
            time.sleep(5)
            break
        else:
            print(selector_tag.get_attribute('innerHTML').strip() + 'skipped')
except:
    print('div with dropdown not found')

try:
    selector_class = selectors_box.find_element(By.CLASS_NAME, 'selector')
    time.sleep(2)
except:
    print('selector class not found')

try:
    selector = Select(selector_class.find_element(By.TAG_NAME, 'select'))
    time.sleep(2)
except:
    print('select tag not found')

try:
    selector.select_by_value('WIG20')
    time.sleep(5)
except:
    print('selecting wig20 option from dropdown failed')

try:
    wig20_table = driver.find_element(By.TAG_NAME, 'table')
except:
    print('table not found')

try:
    wig20_table_text = wig20_table.get_attribute('outerHTML')
except:
    print('outer HTML of wig20_table not found')

try:
    extracted_table = pd.read_html(wig20_table_text, match='Walor')
except:
    print('pd.read_html failed')

try:
    table_to_excel = pd.DataFrame(extracted_table[0])
except:
    print('data frame failed')

try:
    extracted_table[0].to_csv('wig20_index_csv.csv', index=False)
except:
    print('save to csv failed')

try:
    table_to_excel.to_excel('wig20_index_excel.xlsx', sheet_name='current_stock_data')
except:
    print('save to excel failed')

driver.quit()


