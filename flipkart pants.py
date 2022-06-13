
import numpy
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from bs4 import BeautifulSoup as bs
import pandas as pd


"""

1. what all information we need to store?
    A. Brand 
    B. Name
    C. Link to that page
    D. Image Link
    E. Price
    F. Percentage Discount
    G. Free Delivery

2. Find how much time we need to store the data?
    will print it in the terminal
    maybe store the meta data in a text file

3. 


"""

# the following use of path has been deprecated so its better we install a service which will be comapitable for all the browsers
# driver_path = os.path.join(os.getcwd(), 'chromedriver')

flipkart = "www.flipkart.com"
div = 'div'
a = 'a'

class ClassTags :
    discounted_price = '_30jeq3'
    title = 'IRpwTa'
    brand = '_2WkVRV'
    percent_discount = '_3Ay6Sb' 
    original_cost = '_3I9_wc'
    image_link = '_2r_T1I'
    next = '_1LKTO3'

# href of any of them gives link to the page

class TypeDiv :
    discounted_price = div
    title = a
    brand = div
    percent_discount = div # its inside span
    original_cost = div
    image_link = 'img' # its inside alt src
    next = a

column_names  = ["title","discounted price","brand","percent dicount","original cost", "image link"]

# never grow a data frame instead store in a dict 
# data_scrapped = pd.DataFrame(columns = column_names)

data = []

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.maximize_window()


url = 'https://www.flipkart.com/mens-track-pants/pr?sid=clo%2Cvua%2Cjlk%2C6ql&otracker%5B%5D=categorytree&otracker%5B%5D=nmenu_sub_Men_0_Track+pants&sort=price_asc'

driver.get(url)


k = 0
for i in range(25):

    time.sleep(2)
    soup = bs(driver.page_source, "html.parser")
    divisions = soup.find_all( 'div' ,class_='_13oc-S')
    
    for each in divisions:
        row = each.findChildren(recursive = False)
        for er in row:
            try:
                data.append([
                er.find(TypeDiv.title,class_ = ClassTags.title).get('title'),
                er.find(TypeDiv.discounted_price,class_ = ClassTags.discounted_price).text,
                er.find(TypeDiv.brand, class_ = ClassTags.brand).text,
                er.find(TypeDiv.percent_discount, class_ = ClassTags.percent_discount).text,
                er.find(TypeDiv.original_cost, class_ = ClassTags.original_cost).text,
                er.find(TypeDiv.image_link, class_ = ClassTags.image_link).get('src')
                ]
                )
                k+=1       
            except:
                pass


    next_element = driver.find_elements_by_class_name(ClassTags.next)[-1]
    action = ActionChains(driver)
    action.click(on_element = next_element)
    action.perform()

print(data)

dataFrame = pd.DataFrame( data, columns=column_names)
dataFrame.to_csv('laptopInfo.csv')



print(k)

driver.close()