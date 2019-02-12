from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time
from pprint import pprint
from urllib.request import Request, urlopen
import json
import re
import requests
import urllib
import csv


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")


def ParseReviews(asin):
    totalJsonData = {}
    XPATH_PRODUCT_NAME = "//a[@data-hook='product-link']"
    reviews_data = []
    driver = webdriver.Chrome(chrome_options=chrome_options)
    page = 1
    while True:
        url = 'https://www.amazon.com/product-reviews/'+asin + \
            '/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType=all_reviews&pageNumber=' + \
            str(page)
        driver.get(url)
        time.sleep(1)
        try:
            totalJsonData["product-name"] = str(driver.find_element_by_xpath(
                XPATH_PRODUCT_NAME).text)
            totalJsonData["review-count"] = str(driver.find_element_by_class_name(
                "totalReviewCount").text)
        except:
            pass
        try:
            reviews = driver.find_element_by_id("cm_cr-review_list")
        except:
            continue

        for review in reviews.find_elements_by_class_name("review"):
            data = {}
            data["review-id"] = review.get_attribute("id")
            data["review-title"] = str(review.find_element_by_class_name(
                "review-title").text)
            data["review-rating"] = str(review.find_element_by_class_name(
                "review-rating").find_element_by_tag_name("span").get_attribute('innerHTML'))
            data["review-text"] = str(review.find_element_by_class_name(
                "review-text").text).replace('\n', '')
            data["review-author"] = str(review.find_element_by_class_name(
                "author").text)
            data["review-date"] = str(review.find_element_by_class_name(
                "review-date").text)
            try:
                data["cr-vote-text"] = str(review.find_element_by_class_name(
                    "cr-vote-text").text)
            except:
                data["cr-vote-text"] = ""
           
            try:
                data["avp-badge"] = str(driver.find_element_by_xpath("//span[@data-hook='avp-badge']").text)
            except:
                data["avp-badge"] = ""
                
                
            reviews_data.append(data)
        print("Review Page# {} completed".format(page))
        page += 1

        try:
            driver.find_element_by_xpath("//li[@class='a-last']//a")
        except:
            break

    totalJsonData["reviews"] = reviews_data
    driver.close()

    return totalJsonData

def ReadAsin():
    AsinList = [
        'B07GYJSTJL',
    ]
    extracted_data = []
    for asin in AsinList:
        
        print("Downloading and processing: "+asin)
        extracted_data.append(ParseReviews(asin))

    f = open('data_competitor.json', 'w')
    json.dump(extracted_data, f, indent=4)
    f.close()
    
    i = 0
    for asinData in extracted_data:
        with open(AsinList[i] + ".csv", "w") as file:
            i+=1
            csv_file = csv.writer(file)
            for item in asinData['reviews']:
                csv_file.writerow(item.values())
    

if __name__ == '__main__':
    ReadAsin()