''' ___NGDS_HEADER_BEGIN___

National Geothermal Data System - NGDS
https://github.com/ngds

File: <filename>

Copyright (c) 2013, Siemens Corporate Technology and Arizona Geological Survey

Please Refer to the README.txt file in the base directory of the NGDS
project:
https://github.com/ngds/ckanext-ngds/README.txt

___NGDS_HEADER_END___ '''

from selenium import webdriverfrom selenium.common.exceptions import NoSuchElementExceptionfrom selenium.webdriver.common.keys import Keysimport time# naviages to harvest configuration page# browser is the instance of the webbrowser used by seleniumdef navigateToHarvestPage(browser):    #elem = browser.find_element_by_name("Contribute") # Find the contribute box    try:        elem = browser.find_element_by_xpath("//a[contains(@href,'/ngds/contribute')]")        elem.send_keys(Keys.RETURN)        time.sleep(0.2) # Let the page load, will be added to the API    except NoSuchElementException:        assert 0, "can't find contribute link on main website page"            try:        newHarvestBtn = browser.find_element_by_xpath("//a[contains(@href,'/ngds/harvest')]")    except NoSuchElementException:        assert 0, "can't find harvest link leading to harvest page"        newHarvestBtn.send_keys(Keys.RETURN)    time.sleep(0.2)# Inputs a form field in the harvest configuration page# browser is the current instance of the web browser obtained by selenium# id is the id of the HTML field# val is the string to be passed as valuedef inputFormField(browser, id, val):    try:        #newHarvestBtn = browser.find_element_by_name("Harvest a Resource")        field = browser.find_element_by_id(id)        field.send_keys(val)    except NoSuchElementException:        assert 0, "can't find "+ id +" element in current page"# Reads the value of a form field in the harvest configuration page# browser is the current instance of the web browser obtained by selenium# id is the id of the HTML fielddef readFormField(browser, id):    value = ""    try:        #newHarvestBtn = browser.find_element_by_name("Harvest a Resource")        field = browser.find_element_by_id(id)        value = field.get_attribute('value')    except NoSuchElementException:        assert 0, "can't find "+ id +" element in current page"    return value# single test case to be executed by nosetestdef test_input_harvest_config():    browser = webdriver.Firefox() # Get local session of firefox    browser.get("http://localhost:5004/ngds") # Load ngds page    assert "NGDS" in browser.title        print "Navigating to harvest page..."    navigateToHarvestPage(browser)    # provide a set of inputs to the form, and later verify they were saved    input_URL= "myURL"    input_Title = "myTitle"    input_Name = "myName"    input_Org = "myOrganization"    input_Email = "myEmail"    input_Phone = "123-456-7890"    input_Street = "myStreet and something"    input_City = "My City"    input_State = "NJ"    input_Zipcode = "08648"        input_Frequency = "daily"        print "Inputing form fields..."    inputFormField(browser, "url", input_URL)    inputFormField(browser, "title", input_Title)        try:        chbox = browser.find_element_by_xpath("//input[contains(@value,'daily')]")        chbox.send_keys(Keys.SPACE)    except NoSuchElementException:         assert 0, "can't find 'daily' check box"        inputFormField(browser, "name", input_Name)    inputFormField(browser, "organization", input_Org)    inputFormField(browser, "email", input_Email)    inputFormField(browser, "phone", input_Phone)    inputFormField(browser, "city", input_City)    inputFormField(browser, "street", input_Street)    inputFormField(browser, "state", input_State)    inputFormField(browser, "zip", input_Zipcode)        try:        save = browser.find_element_by_xpath("//button[contains(@name,'save')]")        save.send_keys(Keys.ENTER)    except NoSuchElementException:         assert 0, "can't find 'Save' button"             # this should take us to the previous page, showing a list of saved records    # now we verify that the record was created    print " verifying record creation..."      # select the last element in the table, supposedly the last one we added    try:        lastViewBtn = browser.find_element_by_xpath("//table/tbody/tr[last()]/td[1]/img[2]")        assert lastViewBtn is not None        lastViewBtn.click()    except NoSuchElementException:         assert 0, "can't find 'View' button on table for last table element"          # now verifies the content        output_URL = readFormField(browser, "url")    print "URL = "+output_URL    assert output_URL == input_URL    output_Title = readFormField(browser, "title")    assert output_Title == input_Title        isSelected = False    try:        chbox = browser.find_element_by_xpath("//input[contains(@value,'daily')]")        isSelected = chbox.is_selected()    except NoSuchElementException:         assert 0, "can't find 'daily' check box"    assert isSelected == True        output_Name = readFormField(browser, "name")    assert output_Name == input_Name        output_Org = readFormField(browser, "organization")    assert output_Org == input_Org        output_Email = readFormField(browser, "email")    assert output_Email == input_Email        output_Phone = readFormField(browser, "phone")    assert output_Phone == input_Phone        output_City = readFormField(browser, "city")    assert output_City == input_City        output_Street = readFormField(browser, "street")    assert output_Street == input_Street        output_State = readFormField(browser, "state")    assert output_State == input_State        output_Zipcode = readFormField(browser, "zip")    assert output_Zipcode == input_Zipcode        time.sleep(5)          print "Closing browser"         browser.close()
