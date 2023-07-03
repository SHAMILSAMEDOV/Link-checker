from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
import requests


url = "your_link"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Referer': 'https://www.google.com/'
}

def goWebsite(link):
    chrome_options = Options()
    chrome_options.add_argument('--headless')

    uzunlug = len(link)
    global driver
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(link)
    time.sleep(5)
    findTags()


def findTags():
    a_tags = driver.find_elements(By.TAG_NAME, "a")
    link_tags = driver.find_elements(By.TAG_NAME, "link")
    a_links = []
    a_links_diff = []
    
    for a_tag in a_tags:
        a_link = a_tag.get_attribute('href')
        #substrLink = a_link[0:26]
        a_links.append(a_link)
        # for i in a_links:
        #     if i == url or i == "javascript:void(0);" or i == "javascript:void(0)":
        #         continue
        #     else:
        #         a_links_diff.append(i)
    
    for l_tag in link_tags:
        l_link = l_tag.get_attribute("href")
        a_links.append(l_link)
        

    
    #count = 1
    #print("href deyerleri: --------------------------------------------------------------------------")
    # for l in a_links_diff:
    #     print(count, l)
    #     count+=1

    # for a_link in a_links:
    #     print(count,a_link)
    #     count+=1

    #listler
    same_links = []
    js_links = []

    # same_linl_count = 0
    # js_void_count = 0
    # diff_link_count = 0
    for i in a_links:
        if len(i)>=len(url):
            i_substr = i[0:len(url)]
            if i_substr != url:
                a_links_diff.append(i)
                #diff_link_count+=1
            elif i_substr == url:
                same_links.append(i)
                #same_linl_count+=1
        elif len(i)<len(url) and i == "javascript:void(0)" or len(i)<len(url) and i == "javascript:void(0);":
            js_links.append(i)
            #js_void_count+=1
            continue
        elif len(i)<len(url):
            a_links_diff.append(i)
            #diff_link_count+=1
    
    # print("same link count - {0}\ndiff link count - {1}\njsVoid count - {2}\n\n".format(same_linl_count, diff_link_count, js_void_count))
    
    ok_links = []
    fail_links = []

    print("Different links: {} -----------------------------------------------------------------------------------------------------------------\n\n".format(len(a_links_diff)))
    for urele in a_links_diff:
        if urele.startswith('javascript:'):
            continue
        response = requests.get(urele, headers=headers)

        if response.status_code == 200:
            ok_links.append(urele+" -- "+str(response.status_code))
        else:
            fail_links.append(urele+" -- "+str(response.status_code))
        time.sleep(2)
    
    
    # Nəticə
    ok_count = 1
    fail_count = 1 
    print("################################################################Success############################################################\n\n")
    for o in ok_links:
        print(str(ok_count)+")","Success", "--", o)
        ok_count+=1

    print("\n\n##############################################################Fail################################################################\n\n")

    for f in fail_links:
        print(str(fail_count)+")", "Fail", "--", f)
        fail_count+=1


    # print("Same links: -----------------------------------------------------------------------------------------------------------------")
    # for s in same_links:
    #     print(s)
    
    # print("JsVoid links: -----------------------------------------------------------------------------------------------------------------")
    # for j in js_links:
    #     print(j)



goWebsite(url)
