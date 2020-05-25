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
all_races = {}
for year_button in year_buttons:
    str_year = year_button.find_element_by_xpath('..').get_attribute("id").lstrip('filter-year-')
    if str_year == "1980":
        break
    years.append(str_year)
    all_races[str_year] = {}
    sleep(0.5)
    try:
        year_button.click()
        print(str_year + " clicked")
    except:
        print("button " + year_button.find_element_by_xpath('..').get_attribute("id") + " not clickable")
    sleep(5)
    g_DRIVER.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(7)
    elems = g_DRIVER.find_elements_by_class_name("content-wrapper")
    order_counter = 0  
    for element in elems:
        try:
            elem = element.find_element_by_class_name("_1Uxp-")
            order_counter += 1
            print("GP: ",elem.text)
            elem_mode = "big"
            print("big mode")
        except:
            try:
                elem = element.find_element_by_class_name("Wwm_5")
                order_counter += 1
                print("GP: ",elem.text)
                elem_mode = "small"
                print("small mode")
            except:
                print("No element found, possibly wrong content-wrapper - jumping to next content-wrapper")
                continue
        str_location = elem.text.replace(" Grand Prix","").lower()
        if "Testing" in str_location:
            order_counter = 0
        str_gp = str(order_counter)+"_"+str_location
        
        all_races[str_year][str_gp] = {}
        if elem_mode == "big":
            try:
                elem_url = elem.find_element_by_xpath("..").get_attribute("href")
                if elem_url == None:
                    print("URL is None")
                    replays = element.find_elements_by_class_name("_2vwXV")
                    for replay in replays:
                        m_url = replay.get_attribute("href")
                        
                        m_session = replay.find_element_by_tag_name("h5").text
                        if m_session:
                            print("session found: ", m_session)
                            all_races[str_year][str_gp][m_session] = m_url
                            print("url saved: ", all_races[str_year][str_gp][m_session])
                        print("completed unclickable weekend")
                else:
                    print("weekend has URL: ", elem_url)
                    aux_driver = webdriver.Chrome()
                    aux_driver.get(g_URL)
                    for cookie in cookies:
                        aux_driver.add_cookie(cookie)
                    sleep(2)
                    aux_driver.get(elem_url)
                    sleep(8)
                    aux_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    print("** scrolled! **")
                    sleep(2)
                    
                    
                    btnFound = True
                    while btnFound == True:
                        try:
                            viewmore_button = aux_driver.find_element_by_css_selector("._2hfwz")
                            print("found 'view more' button")
                        except Exception as e:
                            if hasattr(e, 'message'):
                                print(e.message)
                            else:
                                print(e)
                            btnFound = False
                            continue
                        # action = ActionChains(aux_driver)
                        # action.move_to_element(viewmore_button).perform()
                        aux_driver.execute_script("arguments[0].click();", viewmore_button)
                        # viewmore_button.click()
                        sleep(0.5)
                   
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
                    sleep(1)
            except Exception as e:
                if hasattr(e, 'message'):
                    print(e.message)
                else:
                    print(e)
                print("weekend has no URL")
                replays = element.find_elements_by_class_name("_2vwXV")
                for replay in replays:
                    m_url = replay.get_attribute("href")
                    
                    m_session = replay.find_element_by_tag_name("h5").text
                    if m_session:
                        print("session found: ", m_session)
                        all_races[str_year][str_gp][m_session] = m_url
                        print("url saved: ", all_races[str_year][str_gp][m_session])
                    print("completed unclickable replay")
            sleep(0.3)
            print("completed weekend")
        elif elem_mode == "small":
            print("scraping small element...")
            replays = element.find_elements_by_class_name("_2vwXV")
            for replay in replays:
                m_url = replay.get_attribute("href")
                m_session = replay.find_element_by_tag_name("h5").text
                if m_session:
                    print("session found: ", m_session)
                    all_races[str_year][str_gp][m_session] = m_url
                    print("url saved: ", all_races[str_year][str_gp][m_session])
                print("completed unclickable replay")
    season_dropdown.click()
    print("completed year")
    sleep(0.3)
    

print(years)

with open('data.json', 'w') as outfile:
    json.dump(all_races, outfile)

g_DRIVER.quit()