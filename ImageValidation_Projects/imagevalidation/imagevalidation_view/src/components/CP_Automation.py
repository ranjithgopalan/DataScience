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
        Coveragetab = wait.until(EC.presence_of_element_located((By.XPATH ,"//li[@routerlinkactive]//a[text()='Manage Risk']")))
        Coveragetab.click()
        wait = WebDriverWait(driver, 50)  # Wait up to 10 seconds
        logging.info('PASS: User landed Manage Risk  page successfully')
        save_full_page_screenshot(driver, 'CP_Manage_Risk ')

    except Exception as e:
        logging.error(str(e)+' %s', time.strftime("%H:%M:%S"))
        logging.info('FAIL: '+str(e))
        return
    

def save_full_page_screenshot(driver, file_name):
    """
    Takes a full-page screenshot of the current webpage and saves it as an image file.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        file_name (str): The name of the image file to save.

    Returns:
        None
    """
    height, width = scroll_down(driver,file_name)
    mergeImages(file_name)
  

def scroll_down(driver,file_name):
    """
    Scrolls down the webpage and captures multiple screenshots to cover the entire page height.
    Saves each screenshot as an image file.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        file_name (str): The base name of the image files to save.

    Returns:
        total_height (int): The total height of the webpage.
        total_width (int): The total width of the webpage.
    """
    total_width = driver.execute_script("return document.body.offsetWidth")
    total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
    viewport_width = driver.execute_script("return document.body.clientWidth")
    viewport_height = driver.execute_script("return window.innerHeight")

    rectangles = []
    i = 0
    while i < total_height:
        ii = 0
        top_height = i + viewport_height
        if top_height > total_height:
            top_height = total_height
        while ii < total_width:
            top_width = ii + viewport_width
            if top_width > total_width:
                top_width = total_width
            rectangles.append((ii, i, top_width, top_height))
            ii += viewport_width
        i += viewport_height

    previous = None
    i =0
    for rectangle in rectangles:
       

        if previous is not None:
            driver.execute_script(
                "window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1])
            )
            img_binary = driver.get_screenshot_as_png()
            img = Image.open(BytesIO(img_binary))
            img.save(file_name+str(i)+'.png')
            print(f"Full-page screenshot saved as {file_name+str(i)+'.png'}")
            time.sleep(0.5)  # Adjust the delay as needed
        else:
            img_binary = driver.get_screenshot_as_png()
            img = Image.open(BytesIO(img_binary))
            img.save(file_name+str(i)+'.png')
            print(f"Full-page screenshot saved as {file_name +str(i)+'.png'}")
        previous = rectangle
        i+=1

    return total_height, total_width

def mergeImages(fileName):
    """
    Merges multiple image files into a single image vertically.

    Args:
        fileName (str): The base name of the image files to merge.

    Returns:
        None
    """
    filenames = [f for f in os.listdir('.') if f.startswith(fileName)]
    filenames.sort()
    images = [Image.open(f) for f in filenames]
    new_image = Image.new('RGB', (images[0].width, sum(i.height for i in images)))
    y = 0
    for image in images:
        new_image.paste(image, (0, y))
        y += image.height
    new_image.save(fileName+'combined.png')
    if os.path.exists(fileName+'combined.png'):
        os.replace(fileName+'combined.png', 'ModelValidation/'+fileName+'combined.png')

naviagetoCP("https://uat.pcgcustomer.nprd.aig.com/login")