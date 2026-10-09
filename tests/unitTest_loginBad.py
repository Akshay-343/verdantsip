# This is a Unit test file to determine if login functionality is working correctly or not
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
        pwd = "instructor123"
        driver = self.driver
        driver.maximize_window()
        driver.get("http://127.0.0.1:8000/accounts/login")
        elem = driver.find_element(By.ID, "id_username")
        elem.send_keys(user)
        elem = driver.find_element(By.ID, "id_password")
        elem.send_keys(pwd)
        time.sleep(6)
        elem.send_keys(Keys.RETURN)

        time.sleep(6)

        try:
            elem = driver.find_element(By.XPATH, "//*[text()='Login']")
            driver.close()
            assert True

        except NoSuchElementException:
            driver.close()
            self.fail("Login page error")

        time.sleep(3)


if __name__ == "__main__":
    unittest.main(warnings='ignore')
