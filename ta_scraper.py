import csv
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

#Chrome Options
option = webdriver.ChromeOptions()
option.add_argument("--incognito")
##initialize Chrome Driver
driver = webdriver.Chrome("/Users/yuanhengwang/Desktop/Python/Data Incbubator/chromedriver",chrome_options=option)
my_url = 'https://www.tripadvisor.com/Attraction_Review-g60763-d587661-Reviews-Top_of_the_Rock_Observation_Deck-New_York_City_New_York.html'
driver.get(my_url)
driver.maximize_window()


def parseSinglePage(source_url,traveler_type,review_score):
    ##html parsing
    page_soup = soup(source_url,"html.parser")

    single_page_reviews = []
    ##grab all the Reviews
    containers = page_soup.findAll("div",{"class":"review-container"})
    for container in containers:
        user_id = container.findAll("span",{"class":"expand_inline scrname"})[0].text
        try:
            user_location = container.findAll("div",{"class":"location"})[0].text
        except:
            user_location = None
        review_title = container.findAll("span",{"class":"noQuotes"})[0].text
        review_date = container.findAll("span",{"class":"ratingDate relativeDate"})[0]["title"]
        review = container.findAll("p",{"class":"partial_entry"})[0].text
        single_page_reviews.append([user_id,user_location,traveler_type,review_title,review_date,review_score,review])
    return single_page_reviews
###############
# High level logic:
# Driver calls each combination of review_score and traveler_type:
#   While review counts < 101 or next.button is enabled:
#   Driver calls each page:
#       Time: wait for 5 seconds
#       scrapers get the data: user_id, user_location, traveler_type, review_title,review_date,review_score, review
###############

review_score_filter = [
"""//input[@id="taplc_location_review_filter_controls_responsive_0_filterRating_1"]""",
"""//input[@id="taplc_location_review_filter_controls_responsive_0_filterRating_2"]""",
"""//input[@id="taplc_location_review_filter_controls_responsive_0_filterRating_3"]""",
"""//input[@id="taplc_location_review_filter_controls_responsive_0_filterRating_4"]""",
"""//input[@id="taplc_location_review_filter_controls_responsive_0_filterRating_5"]"""
]

traveler_type_filter = [
"""//input[@id="taplc_location_review_filter_controls_responsive_0_filterSegment_Families"]""",
"""//input[@id="taplc_location_review_filter_controls_responsive_0_filterSegment_Couples"]""",
"""//input[@id="taplc_location_review_filter_controls_responsive_0_filterSegment_Solo"]""",
"""//input[@id="taplc_location_review_filter_controls_responsive_0_filterSegment_Business"]""",
"""//input[@id="taplc_location_review_filter_controls_responsive_0_filterSegment_Friends"]"""
]

timeout = 15
total_reviews = []
for review_score_select in review_score_filter:
    driver.implicitly_wait(10)
    time.sleep(5)
    checkbox = WebDriverWait(driver,timeout).until(EC.visibility_of_element_located((By.XPATH,review_score_select)))
    #driver.find_element_by_xpath(review_score_select).click()
    driver.execute_script("arguments[0].click();", checkbox)
    for traveler_type_select in traveler_type_filter:
        # try:
        #     WebDriverWait(driver,timeout).until(EC.visibility_of_element_located((By.XPATH,"//img[@class='cta']")))
        # except TimeoutException:
        #     print("Time has running out!")
        #     driver.quit()
        driver.implicitly_wait(10)
        time.sleep(5)
        checkbox = WebDriverWait(driver,timeout).until(EC.visibility_of_element_located((By.XPATH,traveler_type_select)))
        #driver.find_element_by_xpath(traveler_type_select).click()
        driver.execute_script("arguments[0].click();", checkbox)
        counter = 0
        while counter <=1000:
            driver.implicitly_wait(5)
            time.sleep(5)
            try:
                WebDriverWait(driver,timeout).until(EC.visibility_of_element_located((By.XPATH,"""//*[@id="taplc_location_reviews_list_responsive_detail_0"]/div/div[22]/div/div/a[2]""")))
                driver.find_element_by_xpath("""//*[@id="taplc_location_reviews_list_responsive_detail_0"]/div/div[22]/div/div/a[2]""").is_enabled()
            except:
                #parse the last page of the review for the combination
                last_page_reviews = parseSinglePage(driver.page_source,traveler_type_select,review_score_select)
                counter += len(last_page_reviews)
                total_reviews.extend(last_page_reviews)
                print("Reviews for the group combination have all been scraped!")
                break
            #parse reviews of each page
            each_page_reviews = parseSinglePage(driver.page_source,traveler_type_select,review_score_select)
            counter += len(each_page_reviews)
            total_reviews.extend(each_page_reviews)
            driver.implicitly_wait(5)
            time.sleep(5)
            checkbox = WebDriverWait(driver,timeout).until(EC.visibility_of_element_located((By.XPATH,"""//*[@id="taplc_location_reviews_list_responsive_detail_0"]/div/div[22]/div/div/a[2]""")))
            #driver.find_element_by_xpath("""//*[@id="taplc_location_reviews_list_responsive_detail_0"]/div/div[22]/div/div/a[2]""").click()
            driver.execute_script("arguments[0].click();", checkbox)
        driver.implicitly_wait(10)
        time.sleep(5)
        checkbox = WebDriverWait(driver,timeout).until(EC.visibility_of_element_located((By.XPATH,traveler_type_select)))
        #driver.find_element_by_xpath(traveler_type_select).click()
        driver.execute_script("arguments[0].click();", checkbox)
    driver.implicitly_wait(10)
    time.sleep(5)
    checkbox = WebDriverWait(driver,timeout).until(EC.visibility_of_element_located((By.XPATH,review_score_select)))
    #driver.find_element_by_xpath(review_score_select).click()
    driver.execute_script("arguments[0].click();", checkbox)
driver.close()
driver.quit()

##write the output to csv
f = open("review_output_relative_big.csv",'w',encoding='utf-8')
writer = csv.writer(f)
header = ["user_id","user_location","traveler_type","review_title","review_date","review_score","review"]

writer.writerow(header)
for record in total_reviews:
    record[2] = record[2].split('_')[-1][:-2]
    record[5] = record[5].split('_')[-1][:-2]
    writer.writerow(record)
f.close()
