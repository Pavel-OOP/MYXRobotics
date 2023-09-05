import logging
import os
import random
import string
import time
import unittest

from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select


def random_char(char_num):
    return ''.join(random.choice(string.ascii_letters) for _ in range(char_num))


class MYX_robotics(unittest.TestCase):
    def setUp(self):
        chromedriver_autoinstaller.install()
        self.driverChrome = webdriver.Chrome()
        self.driverChrome.implicitly_wait(30)

    def testCases(self):
        driverChrome = self.driverChrome
        driverChrome.get("http://localhost:8080/login")

        formExists = driverChrome.find_element(By.CSS_SELECTOR, "body > form[method='post']").is_displayed()
        formLogin = driverChrome.find_element(By.CSS_SELECTOR, "form[method='post'] > h1").get_attribute("innerHTML")
        with self.subTest(msg="form is displayed"):
            self.assertTrue(formExists)
            self.assertEqual(" Login ", formLogin)
            # we continue to assert presence of important fields

        driverChrome.find_element(By.CSS_SELECTOR, "a").click()

        formExists = driverChrome.find_element(By.CSS_SELECTOR, "body > form[method='post']").is_displayed()
        formRegister = driverChrome.find_element(By.CSS_SELECTOR, "form[method='post'] > h1").get_attribute("innerHTML")
        dropdownExists = driverChrome.find_element(By.CSS_SELECTOR, "select#type").is_displayed()
        with self.subTest(msg="form is displayed"):
            self.assertTrue(formExists)
            self.assertEqual(" Register ", formRegister)
            self.assertTrue(dropdownExists)
            # we continue to assert important fields

        email1 = random_char(5) + "@gmail.com"
        driverChrome.find_element(By.CSS_SELECTOR, "form[method='post'] > input[name='email']").send_keys(email1)
        password1 = random_char(5)
        driverChrome.find_element(By.CSS_SELECTOR, "form[method='post'] > input[name='password']").send_keys(password1)
        print(email1)
        print(password1)

        expectedOpt = ["", "Normal", "Enterprise"]
        actualOpt = []
        dropdownOpt = driverChrome.find_elements(By.CSS_SELECTOR, "select#type > option")

        for ele in dropdownOpt:
            actualOpt.append(ele.text)

        with self.subTest(msg="options are valid"):
            self.assertEqual(expectedOpt, actualOpt)

        select = Select(driverChrome.find_element(By.CSS_SELECTOR, "select#type"))
        select.select_by_visible_text("Enterprise")
        driverChrome.find_element(By.CSS_SELECTOR, "form[method='post'] > input[value='Register']").click()

        redirectURL = driverChrome.current_url
        with self.subTest(msg="successfully redirected to Login"):
            self.assertEqual("http://localhost:8080/login", redirectURL)

        driverChrome.find_element(By.CSS_SELECTOR, "form[method='post'] > input[name='email']").send_keys(email1)
        driverChrome.find_element(By.CSS_SELECTOR, "form[method='post'] > input[name='password']").send_keys(password1)
        driverChrome.find_element(By.CSS_SELECTOR, "form[method='post'] > input[value='Sign in']").click()

        emailCheck = driverChrome.find_element(By.CSS_SELECTOR, "header > span:nth-of-type(2)").text
        emailCheck = emailCheck.split("as ")
        with self.subTest(msg="Login is valid"):
            self.assertEqual(email1, emailCheck[1])

        driverChrome.find_element(By.CSS_SELECTOR, "input#twin-name").send_keys(random_char(5))

        f = open("testFile1.txt", "w")
        f.write("Some test file")
        f.close()
        directory = os.getcwd()
        fileDir = directory + "/testFile1.txt"

        element = WebDriverWait(driverChrome, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input#file-upload")))
        element.send_keys(fileDir)

        fileUploaded = driverChrome.find_elements(By.XPATH, "//*[text()[contains(.,'testFile1.txt')]]")

        with self.subTest(msg="file was uploaded successfully"):
            self.assertTrue(len(fileUploaded) != 0)

        print("Thank you for your time!")

    def tearDown(self):
        self.driverChrome.quit()


if __name__ == '__main__':
    unittest.main()
