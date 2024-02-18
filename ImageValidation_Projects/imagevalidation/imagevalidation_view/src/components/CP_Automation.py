import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import io
import pyautogui
import time
from io import BytesIO
from selenium.webdriver.chrome.options import Options
import os
import logging
from UIFunctions import save_full_page_screenshot

def naviagetoCP(url):
    """
    Opens the specified URL in a headless Chrome browser and performs a series of actions.

    Args:
        url (str): The URL to open.

    Returns:
        None
    """
    try:
        url = str(url)
        options = Options()
        if os.path.exists('runtime.log'):
            os.remove('runtime.log')
        logging.basicConfig(filename='runtime.log', level=logging.INFO, format='%(asctime)s %(message)s')
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        driver.get(url)
        wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
        userName = wait.until(EC.presence_of_element_located((By.ID, "okta-signin-username")))
        # Now you can interact with the input box
        userName.send_keys("uatedel@gmail.com")
        password = wait.until(EC.presence_of_element_located((By.ID, "okta-signin-password")))
        password.send_keys("Fly2India!")

        LoginButton = wait.until(EC.presence_of_element_located((By.ID, "okta-signin-submit")))
        save_full_page_screenshot(driver, 'CP_Login')        
        logging.info('INFO:User is navigating  to login dashboard')
        LoginButton.click()       
        buttonViewPolices = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/div/app-app-shell/div/app-dashboard/div[1]/div/div/div[3]/axis-card/axis-card-body/div/div[1]/div/button")))
        wait = WebDriverWait(driver, 50)  # Wait up to 10 seconds
        logging.info('PASS: User landed dashboard successfully')
        save_full_page_screenshot(driver, 'CP_Dashboard')

        logging.info('INFO:User is navigating to  billing page')
        Billingtab = wait.until(EC.presence_of_element_located((By.XPATH ,"//li[@routerlinkactive]//a[text()='Billing']")))
        Billingtab.click()
        wait = WebDriverWait(driver, 50)  # Wait up to 10 seconds
        logging.info('PASS: User landed billing page successfully')
        save_full_page_screenshot(driver, 'CP_Billing')

        logging.info('INFO:User is navigating to  coverage  page')
        Coveragetab = wait.until(EC.presence_of_element_located((By.XPATH ,"//li[@routerlinkactive]//a[text()='Coverages']")))
        Coveragetab.click()
        wait = WebDriverWait(driver, 50)  # Wait up to 10 seconds
        logging.info('PASS: User landed coverage page successfully')
        save_full_page_screenshot(driver, 'CP_Coverage')

        logging.info('INFO:User is navigating to  Claims  page')
        Coveragetab = wait.until(EC.presence_of_element_located((By.XPATH ,"//li[@routerlinkactive]//a[text()='Claims']")))
        Coveragetab.click()
        wait = WebDriverWait(driver, 50)  # Wait up to 10 seconds
        logging.info('PASS: User landed claims page successfully')
        save_full_page_screenshot(driver, 'CP_claims')

        logging.info('INFO:User is navigating to  Manage Risk  page')
        manangeRisk = wait.until(EC.presence_of_element_located((By.XPATH ,"//li[@routerlinkactive]//a[text()='Manage Risk']")))
        manangeRisk.click()
        time.sleep(5)
        wait = WebDriverWait(driver, 50)  # Wait up to 10 seconds
        logging.info('PASS: User landed Manage Risk  page successfully')
        save_full_page_screenshot(driver, 'CP_Manage_Risk ')

    except Exception as e:
        logging.error(str(e)+' %s', time.strftime("%H:%M:%S"))
        logging.info('FAIL: '+str(e))
        return
  
naviagetoCP("https://uat.pcgcustomer.nprd.aig.com/login")