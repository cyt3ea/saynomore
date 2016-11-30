import os
import unittest
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

class PythonOrgSearch(unittest.TestCase):
    @classmethod
    def setUp(inst):        
        binary = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')
        inst.driver = webdriver.Firefox(firefox_binary=binary)
        # inst.driver.implicitly_wait(30)
        inst.driver.maximize_window()

        # navigate to saynomore login page
        inst.driver.get("http://159.203.166.80:8000/")
        
    def test_signup(self):
        # create new user
        driver = self.driver
        driver.find_element_by_tag_name('a').click()
        driver.implicitly_wait(60)

        # confirm navigation to signup page
        self.assertTrue(self.is_element_present(By.ID, 'id_firstname'))
        firstname = driver.find_element_by_id('id_firstname')
        lastname = driver.find_element_by_id('id_lastname')
        username = driver.find_element_by_id('id_username')
        password = driver.find_element_by_id('id_password')

        # pass in values for new user
        firstname.send_keys('Ian')
        lastname.send_keys('Zeng')
        username.send_keys('supremeleader')
        password.send_keys('yuanyuan')

        # submit to create new user
        driver.find_element_by_tag_name('button').click()
        
    
    # def test_login(self):
    #     # test if new user login works
    #     driver = self.driver
    #     username = driver.find_element_by_id('id_username')
    #     password = driver.find_element_by_id('id_password')
    #     username.clear()
    #     password.clear()
    #     username.send_keys('supremeleader')
    #     password.send_keys('yuanyuan')

    #     # submit to login
    #     driver.find_element_by_tag_name('button').click()
    #     driver.implicitly_wait(30)

    #     # confirm successful login and redirect to home page
    #     self.assertTrue(self.is_element_present(By.NAME,'hairstyle_search'))


    def test_search(self):
        driver = self.driver
        username = driver.find_element_by_id('id_username')
        password = driver.find_element_by_id('id_password')
        username.clear()
        password.clear()
        username.send_keys('supremeleader')
        password.send_keys('yuanyuan')

        # submit to login
        driver.find_element_by_tag_name('button').click()
        driver.implicitly_wait(30)

        # test search
        search_field = driver.find_element_by_name('hairstyle_search')

        #enter search keyword and submit
        search_field.send_keys("McFlurry")
        search_field.submit()
        driver.implicitly_wait(30)

        #get list of elements displayed after search
        lists = driver.find_elements_by_link_text("McFlurry")
        self.assertGreaterEqual(len(lists), 1)

    def test_createHair(self):
        driver = self.driver
        # login first
        username = driver.find_element_by_id('id_username')
        password = driver.find_element_by_id('id_password')
        username.clear()
        password.clear()
        username.send_keys('supremeleader')
        password.send_keys('yuanyuan')

        # submit to login
        driver.find_element_by_tag_name('button').click()
        driver.implicitly_wait(30) 

        # select create hair button
        driver.find_element_by_id('create_hair').click()
        driver.implicitly_wait(30)

        # create hair
        name = driver.find_element_by_id('id_name')
        stylist = driver.find_element_by_id('id_stylist')
        location = driver.find_element_by_id('id_location')
        price = driver.find_element_by_id('id_price')
        phone_number = driver.find_element_by_id('id_phone_number')

        # fill in form fields
        name.send_keys('Tiny Trinkle Trotties')
        stylist.send_keys('Selenium Gomez')
        location.send_keys('Rice Hall')
        price.send_keys('15')
        phone_number.send_keys('0000000000')
        driver.find_element_by_tag_name('button').click()
        driver.implicitly_wait(80)

        #check if new hair is created
        self.assertTrue(self.is_element_present(By.LINK_TEXT,'The Travis'))



    @classmethod
    def tearDown(inst):
        # close the browser window
        inst.driver.quit()
        # uncomment following line if you want the browser to remain open
        # inst.driver.close()

    def is_element_present(self, how, what):
        """
        Helper method to confirm presence of element on page
        :params how: by locator type
        :parmas what: locator value
        """

        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException: return False
        return True

if __name__ == "__main__":
    unittest.main()