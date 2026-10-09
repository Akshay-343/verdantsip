# This test is used to check all allergens button
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class ll_ATS(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_ll(self):
        user = "instructor"
        pwd = "mavericks1b"
        driver = self.driver
        driver.maximize_window()
        driver.get("http://127.0.0.1:8000/accounts/login/")
        elem = driver.find_element(By.ID, "id_username")
        elem.send_keys(user)
        elem = driver.find_element(By.ID, "id_password")
        elem.send_keys(pwd)
        time.sleep(3)
        elem.send_keys(Keys.RETURN)
        time.sleep(3)
        driver.find_element(By.XPATH, "//a[contains(., 'Admin')]").click()
        time.sleep(3)
        driver.find_element(By.XPATH, "//a[contains(., 'All Allergen')]").click()
        time.sleep(2)

        try:
            elem = driver.find_element(By.XPATH, "//*[text()='All Allergens']")
            time.sleep(3)
            driver.close()
            assert True

        except NoSuchElementException:
            driver.close()
            self.fail("All Allergens button not working ")


if __name__ == "__main__":
    unittest.main(warnings='ignore')
