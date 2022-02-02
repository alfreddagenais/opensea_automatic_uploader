
# Colorama module: pip install colorama
from colorama import init, Fore, Style

# Selenium module imports: pip install selenium
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.common.exceptions import TimeoutException as TE
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Python default imports.
from datetime import datetime as dt
from glob import glob
import os
import time

"""Colorama module constants."""
# This module may not work under MacOS.
init(convert=True, autoreset=True)  # Init the Colorama module.
red = Fore.RED  # Red color.
green = Fore.GREEN  # Green color.
yellow = Fore.YELLOW  # Yellow color.
reset = Style.RESET_ALL  # Reset color attribute.


class Webdriver:
    """Webdriver class and methods to prevent exceptions."""

    def __init__(self) -> None:
        """Contains the file paths of the webdriver and the extension."""
        # Used files path, change them with your path if necessary.
        self.webdriver_path = os.path.abspath('assets/chromedriver.exe') if \
            os.name == 'nt' else os.path.abspath('assets/chromedriver')
        #self.metamask_extension_path = os.path.abspath('assets/MetaMask.crx')
        self.driver = self.webdriver()  # Start new webdriver.

    def webdriver(self) -> webdriver:
        """Start a webdriver and return its state."""
        options = webdriver.ChromeOptions()  # Configure options for Chrome.
        #options.add_extension(self.metamask_extension_path)  # Add extension.
        options.add_argument("log-level=3")  # No logs is printed.
        options.add_argument("--mute-audio")  # Audio is muted.
        options.add_argument("--lang=en-US")  # Set webdriver language
        options.add_experimental_option(  # to English. - 2 methods.
            'prefs', {'intl.accept_languages': 'en,en_US'})
        driver = webdriver.Chrome(service=Service(  # DeprecationWarning using
            self.webdriver_path), options=options)  # executable_path.
        driver.maximize_window()  # Maximize window to reach all elements.
        return driver

    def clickable(self, element: str) -> None:
        """Click on an element if it's clickable using Selenium."""
        try:
            WDW(self.driver, 10).until(EC.element_to_be_clickable(
                (By.XPATH, element))).click()
        except Exception:  # Some buttons need to be visible to be clickable,
            self.driver.execute_script(  # so JavaScript can bypass this.
                'arguments[0].click();', self.visible(element))

    def visible(self, element: str):
        """Check if an element is visible using Selenium."""
        return WDW(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, element)))

    def elements(self, element: str):
        """Get elements in page"""
        return self.driver.find_elements(By.XPATH, element)

    def sub_element(self, parent, element: str):
        """Get sub element of a parent"""
        return parent.find_element(By.XPATH, element)
    
    def sub_elements(self, parent, element: str):
        """Get sub elements of a parent"""
        return parent.find_elements(By.XPATH, element)

    def send_keys(self, element: str, keys: str) -> None:
        """Send keys to an element if it's visible using Selenium."""
        try:
            self.visible(element).send_keys(keys)
        except Exception:  # Some elements are not visible but are present.
            WDW(self.driver, 5).until(EC.presence_of_element_located(
                (By.XPATH, element))).send_keys(keys)

    def send_date(self, element: str, keys: str, date_format: str = '') -> None:
        """Send a date (DD-MM-YYYY HH:MM) to a date input by clicking on it."""
        if date_format != '':
          self.clickable(element)  # Click first on the element.
          end_date_object = dt.strptime(keys, date_format)
          self.send_keys(element, end_date_object.day)
          self.send_keys(element, Keys.ARROW_RIGHT)
          self.send_keys(element, end_date_object.month)
        else:
          keys = keys.split('-') if '-' in keys else [keys]
          keys = [keys[1], keys[0], keys[2]] if len(keys) > 1 else keys
          for part in range(len(keys) - 1 if keys[len(keys) - 1]  # Compare years
                  == str(dt.now().year) else len(keys)):  # To count clicks.
              self.clickable(element)  # Click first on the element.
              self.send_keys(element, keys[part])  # Then send it the date.

    def clear_text(self, element) -> None:
        """Clear text from an input."""
        self.clickable(element)  # Click on the element then clear its text.
        # Note: change with 'darwin' if it's not working on MacOS.
        control = Keys.COMMAND if os.name == 'posix' else Keys.CONTROL
        webdriver.ActionChains(self.driver).key_down(control).perform()
        webdriver.ActionChains(self.driver).send_keys('a').perform()
        webdriver.ActionChains(self.driver).key_up(control).perform()

    def window_handles(self, window_number: int) -> None:
        """Check for window handles and wait until a specific tab is opened."""
        WDW(self.driver, 30).until(lambda _: len(
            self.driver.window_handles) > window_number)
        # Switch to the asked tab.
        self.driver.switch_to.window(self.driver.window_handles[window_number])


def cls() -> None:
    """Clear console function."""
    # Clear console for Windows using 'cls' and Linux & Mac using 'clear'.
    os.system('cls' if os.name == 'nt' else 'clear')


def exit(message: str = '') -> None:
    """Stop running the program using the sys module."""
    import sys
    sys.exit(f'\n{red}{message}')


if __name__ == '__main__':

    cls()  # Clear console.

    web = Webdriver()  # Start a new webdriver and init its methods.

    web.driver.get('https://opensea.io/collection/nftnlove?tab=activity&search[isSingleCollection]=true')
    time.sleep(1) # Sleep for 3 seconds

    clearallBtn = '//*[@id="main"]/div/div/div[3]/div/div[2]/div/div[3]/div[1]/div/button'
    #clearall = web.visible(clearallBtn).location_once_scrolled_into_view
    web.clickable(clearallBtn)
    # print(clearall)

    #element1 = web.visible('(//*[@role="listitem"])[0]').location_once_scrolled_into_view
    #print(element1)

    print("\n\n")

    #//*[@id="main"]/div/div/div[3]/div/div[2]/div/div[3]/div/div/div[2]/div[15]/button/div/div[2]/div/div/div/div[2]/span[2]/a
    
    SCROLL_PAUSE_TIME = 4.6
    #time.sleep(1)
    #for index in range(1):

    #scroll_height = "(Math.floor(document.body.scrollHeight / 3))"
    scroll_height = "document.body.scrollHeight"
    last_height = web.driver.execute_script(f"return document.body.scrollHeight")

    #web.driver.execute_script(f"window.scrollTo(0, {scroll_height});")

    body = web.visible('/html/body')
    body.send_keys(Keys.PAGE_DOWN)
    body.send_keys(Keys.PAGE_DOWN)
    body.send_keys(Keys.PAGE_DOWN)
    body.send_keys(Keys.PAGE_DOWN)
    body.send_keys(Keys.PAGE_DOWN)

    urls = []

    while True:
      #web.driver.execute_script(f"window.scrollTo(0, {scroll_height});")
      body = web.visible('/html/body')
      body.send_keys(Keys.PAGE_DOWN)
      #body.send_keys(Keys.ARROW_DOWN)

      # Wait to load page
      time.sleep(SCROLL_PAUSE_TIME)

      elements = web.elements('//*[@role="listitem"]')
      #print("Eleemnts:::")
      #print(elements)
      #print("\n\n")

      for elements_index in range(len(elements)):
        parent = elements[elements_index]
        #print("parent 1:::")
        #print(parent.get_attribute('innerHTML'))
        #print("\n\n")

        #try:
          #parent.location_once_scrolled_into_view
        #except Exception:
        #  pass

        #time.sleep(1)
        try:
          #link = web.sub_element(parent, './button/div/div[2]/div/div/div/div[2]/span[2]/a')
          link = web.sub_element(parent, './/button/div/div[2]/div/div/div/div[2]/span[2]/a')
          #sub_element = web.sub_element(parent, './/button/div/div[2]/div/div/div/div[2]/span[2]/a')
          #sub_element = WDW(parent, 10).until(EC.presence_of_element_located((By.XPATH, './button/div/div[2]/div/div/div/div[2]/span[2]/a')))
          #print("link7:::")
          #print(link)
          #print(link.get_attribute('innerHTML'))
          linkHref = link.get_attribute('href')
          #print("linkHref:::")
          #print(linkHref)
          #print("\n\n")
          if linkHref != '':
            urls.append(linkHref)

          #for sub_elements_index in range(len(sub_elements)):

            #link = web.visible('//*[@role="listitem"]/button/div/div[2]/div/div/div/div[2]/span[2]/a').location_once_scrolled_into_view
            #link.location_once_scrolled_into_view
            #linkHref = link.get_attribute('href')

        except Exception:
          pass

      # Calculate new scroll height and compare with last scroll height
      new_height = web.driver.execute_script(f"return document.body.scrollHeight")
      
      #if new_height >= 3000:
      #    break

      if new_height == last_height:
          break
      last_height = new_height

    # Be unique
    urls = list(set(urls))

    #f = open(, "w")
    #f.write("Woops! I have deleted the content!")
    #f.close()

    with open("./datas/urls.txt", 'w') as f:
      f.write('\n'.join(urls))
      f.close()

    time.sleep(3) # Sleep for 3 seconds
    web.driver.quit()  # Stop the webdriver.
    print(f'\n{green}All done! Your NFTs have been uploaded/sold.')