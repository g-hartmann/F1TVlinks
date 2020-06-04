from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
import pickle
from time import sleep
import json
import colorama

colorama.init()

def sleep_anim(sec):
    if sec >= 1:
        for i in range(int(sec)):
            print(".", end="")
            sleep(1)
        print()

def process_replays(html_replay, p_driver=None):
    if p_driver == None:
        replays = element.find_elements_by_class_name(html_replay["html_class_name"])
    else:
        replays = p_driver.find_elements_by_class_name(html_replay["html_class_name"])
    for replay in replays:
        m_url = replay.get_attribute("href")
        m_session = replay.find_element_by_tag_name(html_replay["heading_tag"]).get_attribute("textContent")
        if m_session:
            print_green("session found: " + m_session)
            ALL_RACES[str_year][str_gp][m_session] = m_url
            print_green("url saved: " + ALL_RACES[str_year][str_gp][m_session])
        print_green("completed replay")
        print()

def add_cookies_to_driver(p_driver):
    for cookie in COOKIES:
        p_driver.add_cookie(cookie)

def remove_banner(banner_button):
    try:
        WebDriverWait(DRIVER, 1).until(lambda d: d.find_element_by_class_name(banner_button)).click()
    except Exception as e:
        print_yellow(banner_button + " button not found")
        print(e.__str__)
    sleep(0.1)

def print_green(string):
    print(colorama.Fore.GREEN, end="")
    print(string)
    print(colorama.Style.RESET_ALL, end="")

def print_yellow(string):
    print(colorama.Fore.YELLOW, end="")
    print(string)
    print(colorama.Style.RESET_ALL, end="")

def print_red(string):
    print(colorama.Fore.RED, end="")
    print(string)
    print(colorama.Style.RESET_ALL, end="")


BASE_URL = 'https://f1tv.formula1.com/en/archive'
COOKIE_FILEPATH = "cookies.pkl"
COOKIES = pickle.load(open(COOKIE_FILEPATH, "rb"))
OUTPUT_FILEPATH = "data.json"

HTMLATTR_COOKIE_ACCEPT_BTN = 'cookies-accept-button'
HTMLATTR_CONSENT_BTN = 'truste-close'
HTMLATTR_SEASON_SELECT = 'uyvSG'
HTMLATTR_YEAR_SELECT_BTN = '_30Pv_'
HTMLATTR_GP_ELEM_WRAPPER = "content-wrapper"
HTMLATTR_GP_ELEM_BIG = "_1Uxp-"
HTMLATTR_GP_ELEM_SMALL = "Wwm_5"
HTMLATTR_VIEW_MORE_BTN = "_2hfwz"
HTMLATTR_COOKIE_BANNER = "cookie-banner"
HTML_REPLAY_PRE2018 = {"html_class_name": "_2vwXV", "heading_tag": "h5"}
HTML_REPLAY_POST2018 = {"html_class_name": "_35iD0", "heading_tag": "h4"}

options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
DRIVER = webdriver.Chrome(options=options)


DRIVER.get(BASE_URL)
add_cookies_to_driver(DRIVER)
DRIVER.get(BASE_URL)
print_yellow("Make sure you are logged in, then hit enter")
wait_for_login = input()
pickle.dump(DRIVER.get_cookies() , open(COOKIE_FILEPATH,"wb"))
add_cookies_to_driver(DRIVER)
DRIVER.get(BASE_URL)

remove_banner(HTMLATTR_COOKIE_ACCEPT_BTN)
remove_banner(HTMLATTR_CONSENT_BTN)
remove_banner(HTMLATTR_COOKIE_ACCEPT_BTN)
try:
    DRIVER.execute_script("return document.getElementById("+HTMLATTR_COOKIE_BANNER+").remove();")
except:
    pass

html_btn_season_select = WebDriverWait(DRIVER, 10).until(lambda d: d.find_element_by_class_name(HTMLATTR_SEASON_SELECT))
html_btn_season_select.click()
print_green("Selected year: " + html_btn_season_select.get_attribute("textContent"))

html_btns_year_select = WebDriverWait(DRIVER, 10).until(lambda d: d.find_elements_by_class_name(HTMLATTR_YEAR_SELECT_BTN))

sleep_anim(1)
for year_button in html_btns_year_select[:]:
    if year_button.get_attribute("disabled") != None:
        html_btns_year_select.remove(year_button)
        print_yellow("removed " + year_button.get_attribute("textContent") + ": not clickable")
print_green("Found " + str(len(html_btns_year_select)) + " year select buttons. (" + html_btns_year_select[0].get_attribute("textContent") + " - " + html_btns_year_select[-1].get_attribute("textContent") + ")")

# Main loop: Choose year -> Process GP elements in year -> Choose next year
ALL_RACES = {}
for year_button in html_btns_year_select:
    str_year = year_button.get_attribute("textContent")
    if str_year == "":
        print_red("Empty str_year!")
        raise Exception
    ALL_RACES[str_year] = {}
    sleep(0.5)

    try:
        year_button.click()
        print_green("clicked " + str_year)
    except:
        print_red("button " + year_button.find_element_by_xpath('..').get_attribute("id") + " not clickable")
    sleep_anim(5)
    DRIVER.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep_anim(6)
    DRIVER.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep_anim(6)
    
    gp_elems = DRIVER.find_elements_by_class_name(HTMLATTR_GP_ELEM_WRAPPER)
    order_counter = 0  
    # secondary loop: Evaluate GP element -> process replays in GP element -> Evaluate next GP element
    for element in gp_elems:
        try:
            elem = element.find_element_by_class_name(HTMLATTR_GP_ELEM_BIG)
            order_counter += 1
            print_green("GP: " + elem.get_attribute("textContent"))
            elem_mode = "big"
            print_green("processing big element")
        except:
            try:
                elem = element.find_element_by_class_name(HTMLATTR_GP_ELEM_SMALL)
                order_counter += 1
                print_green("GP: " + elem.get_attribute("textContent"))
                elem_mode = "small"
                print_green("processing small element")
            except:
                print_green("No element found, probably wrong content-wrapper - jumping to next content-wrapper...")
                continue
        
        # Get clean location name. If it's pre-season testing, the order value should be 0
        str_location = elem.get_attribute("textContent").replace(" Grand Prix","").lower()
        if "testing" in str_location:
            order_counter = 0

        str_gp = str(order_counter)+"_"+str_location
        
        ALL_RACES[str_year][str_gp] = {}
        if elem_mode == "big":
            elem_url = elem.find_element_by_xpath("..").get_attribute("href")
            if elem_url == None: # pre-2018-style replay page. 
                print_green("GP element has no href")
                process_replays(HTML_REPLAY_PRE2018)
            else: # post-2018-style replay page. An auxiliary webdriver has to be opened.
                print_green("GP element has href: " + elem_url)
                print_green("Opening auxiliary driver")
                aux_driver = webdriver.Chrome(options=options)
                aux_driver.get(BASE_URL)
                add_cookies_to_driver(aux_driver)
                sleep_anim(3)
                aux_driver.get(elem_url)
                sleep_anim(10)
                aux_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                print_green("scrolled down...")
                sleep_anim(4)
                
                # Find and click all "View more"-buttons.
                btnFound = True
                while btnFound == True:
                    try:
                        viewmore_button = aux_driver.find_element_by_class_name(HTMLATTR_VIEW_MORE_BTN)
                        print_green("found 'view more' button")
                    except NoSuchElementException:
                        print_green("No more 'view more' buttons.")
                        btnFound = False
                        continue
                    aux_driver.execute_script("arguments[0].click();", viewmore_button)
                    sleep_anim(1)
                sleep_anim(1)
                process_replays(HTML_REPLAY_POST2018, aux_driver)
                aux_driver.quit()
                sleep_anim(1)
            sleep(0.3)
            print_green("completed weekend")
            print()
        elif elem_mode == "small":
            process_replays(HTML_REPLAY_PRE2018)

    html_btn_season_select.click()
    print()
    print_green("completed year")
    print("\n \n")
    sleep(0.3)
    

with open(OUTPUT_FILEPATH, 'w') as outfile:
    json.dump(ALL_RACES, outfile)

total_replays = 0
for year in ALL_RACES.keys():
    for weekend in ALL_RACES[year].keys():
        for replay in ALL_RACES[year][weekend].keys():
            total_replays += 1

print_green("Finished! Found " + str(total_replays) + " replays.")

DRIVER.quit()