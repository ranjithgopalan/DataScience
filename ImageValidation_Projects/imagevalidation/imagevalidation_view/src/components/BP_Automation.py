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
        userName = wait.until(EC.presence_of_element_located((By.ID, "idp-discovery-username")))
        time.sleep(2) 
        save_full_page_screenshot(driver, 'BP_Login_Username') 
        # Now you can interact with the input box
        userName.send_keys("uat100168.buser@test.com")
         
        buttonNext = wait.until(EC.presence_of_element_located((By.ID, "idp-discovery-submit")))
        buttonNext.click()
        time.sleep(2) 

        password = wait.until(EC.presence_of_element_located((By.ID, "input73")))
        save_full_page_screenshot(driver, 'BP_Login_password')   
        password.send_keys("New2year@2024")
        buttonVerify = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='form67']/div[2]/input")))
             
        logging.info('INFO:User is navigating  to login dashboard')
        buttonVerify.click()       
        buttonViewPolices = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Add New']")))
        logging.info('PASS: User landed dashboard successfully')
        save_full_page_screenshot(driver, 'BP_Dashboard')   
        buttonViewPolices.click()
        wait = WebDriverWait(driver, 50)  # Wait up to 10 seconds
        logging.info('PASS: User landed search customer page successfully')
        save_full_page_screenshot(driver, 'BP_search_customer_page')

        logging.info('INFO:User is login to enter customer details')
        customerNameEditBox = wait.until(EC.presence_of_element_located((By.XPATH ,"//input[@id='custName']")))
        customerNameEditBox.send_keys("Ranjith")
        customerNameSearch = wait.until(EC.presence_of_element_located((By.XPATH ,"//span[@class='material-icons' and contains(text(),'search')]")))
        customerNameSearch.click()
        time.sleep(5)
        try:
            wait = WebDriverWait(driver, 20)  # Wait up to 10 seconds
            buttonCreateQuoteforNewCustomer = wait.until(EC.presence_of_element_located((By.XPATH ,"//button[contains(text(),'Create Quote for New Customer')]")))
            # buttonCreateQuoteforNewCustomer = wait.until(EC.presence_of_element_located((By.XPATH ,"//*[@id='content']/div/div/app-customer-search/axis-card[1]/axis-card-row/div[2]/div[2]/button")))
            logging.info('PASS: User landed Create new quote page successfully')
            save_full_page_screenshot(driver, 'BP_Customer_page')
        except Exception as e:
            logging.error(str(e)+' %s', time.strftime("%H:%M:%S"))
            logging.info('FAIL: '+str(e))
            return
        
        logging.info('PASS: User is navigating to  create new quote page')
        time.sleep(4)
        buttonCreateQuoteforNewCustomer.click()
        save_full_page_screenshot(driver, 'BP_Product_page')
        logging.info('PASS: User landed product selection page successfully')   
        # # linkProduct.click()
        logging.info('PASS: User is navigated for admitted policies')
        # homeownerpolicy = wait.until(EC.presence_of_element_located((By.XPATH ,"//span[text()='Homeowners']")))
        addhomeownerpolicy = wait.until(EC.presence_of_element_located((By.XPATH ," //*[@id='0']/axis-card-footer/div/div[3]/button/axis-icon/span")))
        addhomeownerpolicy.click()
        logging.info('PASS: User selected for one   homeowner policy')   
        logging.info('PASS: User is navigating to  insured  page')   
        buttonProductSaveAndContinue = wait.until(EC.presence_of_element_located((By.XPATH ,"//button[contains(text(),'Save & Continue')]"))) 
        buttonProductSaveAndContinue.click()
        insurepage = wait.until(EC.presence_of_element_located((By.XPATH ,"//p[@id='Constant_MainInterview_Account_InsuredInfo']")))
        if  insurepage.is_displayed():
            time.sleep(3)
            logging.info('PASS: User landed insured page successfully')
            save_full_page_screenshot(driver, 'BP_Insure_page')
       

    except Exception as e:
        logging.error(str(e)+' %s', time.strftime("%H:%M:%S"))
        logging.info('FAIL: '+str(e))
        return


naviagetoCP("https://uat.pcgbroker.nprd.aig.com")