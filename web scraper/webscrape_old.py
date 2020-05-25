from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pickle
from time import sleep
import json

g_URL = 'https://f1tv.formula1.com/en/archive'

cookies = pickle.load(open("cookies.pkl", "rb"))

g_DRIVER = webdriver.Chrome()
g_DRIVER.get(g_URL)
for cookie in cookies:
    g_DRIVER.add_cookie(cookie)
g_DRIVER.get(g_URL)

actions = ActionChains(g_DRIVER)

pickle.dump(g_DRIVER.get_cookies() , open("cookies.pkl","wb"))
cookies = pickle.load(open("cookies.pkl", "rb"))

season_dropdown = WebDriverWait(g_DRIVER, 10).until(lambda d: d.find_element_by_class_name('uyvSG'))
try:
    g_DRIVER.find_element_by_css_selector('.cookies-accept-button').click()
except: 
    print("Continue not found")
try:
    g_DRIVER.find_element_by_id('truste-consent-button').click()
except: 
    print("Consent button not found")

season_dropdown.click()
year_buttons = WebDriverWait(g_DRIVER, timeout=10).until(lambda d: d.find_elements_by_css_selector('._30Pv_'))



print(season_dropdown.text)
print(len(year_buttons))
years = []
SCROLL_PAUSE_TIME = 3
all_races = {}
for year_button in year_buttons[:2]:
    str_year = year_button.find_element_by_xpath('..').get_attribute("id").lstrip('filter-year-')
    if str_year == "1980":
        break
    years.append(str_year)
    try:
        year_button.click()
        print(str_year + "clicked")
    except:
        print("button " + year_button.find_element_by_xpath('..').get_attribute("id") + " not clickable")
    sleep(5)
    g_DRIVER.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(7)
    big_elems = g_DRIVER.find_elements_by_class_name("_1Uxp-")
    small_elems = g_DRIVER.find_elements_by_class_name("Wwm_5")
    gp_elements = big_elems + small_elems
    for year in years:
        all_races[year] = {}
    for elem in big_elems[1:1]:
        str_gp = elem.text.replace(" Grand Prix","").lower()
        all_races[str_year][str_gp] = {}
        aux_driver = webdriver.Chrome()
        aux_driver.get(g_URL)
        for cookie in cookies:
            aux_driver.add_cookie(cookie)
        sleep(2)
        aux_driver.get(elem.find_element_by_xpath("..").get_attribute("href"))
        sleep(8)
        aux_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("** scrolled! **")
        sleep(2)
        replays = aux_driver.find_elements_by_class_name("_35iD0")
        for replay in replays:
            m_url = replay.get_attribute("href")
            
            m_session = replay.find_element_by_tag_name("h4").text
            if m_session:
                print("session found: ", m_session)
                all_races[str_year][str_gp][m_session] = m_url
                print("url saved: ", all_races[str_year][str_gp][m_session])
            print("completed replay")
        aux_driver.close()
        sleep(2)
        print(str_year, all_races[str_year])
        print("completed weekend")
    season_dropdown.click()
    print("completed year")
    sleep(0.3)
    

print(years)

with open('data.json', 'w') as outfile:
    json.dump(all_races, outfile)

g_DRIVER.quit()