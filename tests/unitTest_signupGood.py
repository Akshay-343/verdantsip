# This is a  test  to check the  signup functionality .
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
        user = "testuser1"
        first_name = "test"
        last_name = "user"
        email = "testing@gmail.com"
        pwd = "mypwd@123"
        driver = self.driver
        driver.maximize_window()
        driver.get("http://127.0.0.1:8000/register")
        elem = driver.find_element(By.ID, "id_username")
        elem.send_keys(user)
        elem = driver.find_element(By.ID, "id_first_name")
        elem.send_keys(first_name)
        elem = driver.find_element(By.ID, "id_last_name")
        elem.send_keys(last_name)
        elem = driver.find_element(By.ID, "id_email")
        elem.send_keys(email)
        elem = driver.find_element(By.ID, "id_password1")
        elem.send_keys(pwd)
        elem = driver.find_element(By.ID, "id_password2")
        elem.send_keys(pwd)
        time.sleep(5)
        elem.send_keys(Keys.RETURN)
        time.sleep(4)
        driver.get("http://127.0.0.1:8000/accounts/login")
        time.sleep(2)
        elem = driver.find_element(By.ID, "id_username")
        elem.send_keys(user)
        elem = driver.find_element(By.ID, "id_password")
        elem.send_keys(pwd)
        time.sleep(4)
        elem.send_keys(Keys.RETURN)
        time.sleep(3)

        try:
            elem = driver.find_element(By.LINK_TEXT, "Logout")
            driver.close()
            assert True

        except NoSuchElementException:
            driver.close()
            self.fail("Signup / Login Failed - user may not exist")


if __name__ == "__main__":
    unittest.main(warnings='ignore')
