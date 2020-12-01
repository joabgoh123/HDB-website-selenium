from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import csv

driver = webdriver.Chrome(executable_path='CHROMEDRIVER_EXECUTABLE')
driver.get('HDB_LINK')
blocks_uncleaned_elements = driver.find_elements_by_xpath('//*[@id="blockDetails"]//font')
blocks_cleaned = []
data = []
for element in blocks_uncleaned_elements:
    try:
        if element.text[0].isdigit():
            blocks_cleaned.append(element.text)
    except IndexError:
        print("Finished block numbers")
blocks_cleaned = list(set(blocks_cleaned))
blocks_cleaned.sort()

for block in blocks_cleaned:
    driver.find_element_by_partial_link_text(block).click()
    street = driver.find_elements_by_xpath('//*[@class="large-5 columns"]')[0].text
    details = driver.find_elements_by_xpath('//*[@class="large-7 columns"]')
    probable_completion = details[0].text 
    delivery_possession = details[1].text
    lease_commencement = details[2].text
    ethnic_quota = details[3].text
    print(ethnic_quota)
    block_no_element = driver.find_elements_by_xpath('//*[@id="blockDetails"]//font')
    block_no = []
    for element in block_no_element:
        if element.text.startswith("#") and element.text not in block_no:
            block_no.append(element.text)
            unit_price_id = element.text + "k"
            xpath = "//*[@id=\'" + element.text + "k\']"
            price = driver.find_element_by_xpath(xpath).get_attribute('title').split("<")[0]

            temp_dict = {"BLK":block, "Street":street,"Unit":element.text,"Probable Completion Date": probable_completion,
            "Delivery Posession Date": delivery_possession, "Lease Commencement Date":lease_commencement, "Ethnic quota":ethnic_quota,
            "Price":price}
            data.append(temp_dict)

with open("PATH_TO_YOUR_FILE",'w',newline='') as csvFile:
    fields = temp_dict.keys()
    writer = csv.DictWriter(csvFile,fields)
    writer.writeheader()
    writer.writerows(data)
print("writing completed")
csvFile.close()
            

