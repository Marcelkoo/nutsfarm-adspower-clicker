import logging
import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException
from browser_manager import BrowserManager
from utils import update_balance_table

class TelegramBotAutomation:
    def __init__(self, serial_number):
        self.serial_number = serial_number
        self.browser_manager = BrowserManager(serial_number)
        logging.info(f"Initializing automation for account {serial_number}")
        self.browser_manager.start_browser()
        self.driver = self.browser_manager.driver

    def navigate_to_bot(self):
        try:
            self.driver.get('https://web.telegram.org/k/')
            logging.info(f"Account {self.serial_number}: Navigated to Telegram web.")
        except Exception as e:
            logging.exception(f"Account {self.serial_number}: Exception in navigating to Telegram bot: {str(e)}")
            self.browser_manager.close_browser()
            
    def switch_to_iframe(self):
        self.driver.switch_to.default_content()
        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
        if iframes:
            self.driver.switch_to.frame(iframes[0])
            logging.info(f"Account {self.serial_number}: Switched to iframe.")
            return True
        return False
    
    def send_message(self, message):
        chat_input_area = self.wait_for_element(By.XPATH, '/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/input[1]')
        chat_input_area.click()
        chat_input_area.send_keys(message)

        search_area = self.wait_for_element(By.XPATH, '/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/ul[1]/a[1]/div[1]')
        search_area.click()
        logging.info(f"Account {self.serial_number}: Group searched.")
        sleep_time = random.randint(5, 7)
        logging.info(f"Sleeping for {sleep_time} seconds.")
        time.sleep(sleep_time)

    def click_link(self):
        try:
            link = self.wait_for_element(By.CSS_SELECTOR, "a[href*='https://t.me/nutsfarm_bot/nutscoin?startapp=ref_marcelkow']")
            link.click()
            time.sleep(2)
        except NoSuchElementException:
            logging.error(f"Account {self.serial_number}: Link not found.")
            return
        except WebDriverException as e:
            logging.info(f"Account {self.serial_number}: has WebDriverException")
            return

        try:
            launch_button = self.wait_for_element(By.CSS_SELECTOR, "button.popup-button.btn.primary.rp", timeout=5)
            launch_button.click()
            logging.info(f"Account {self.serial_number}: Launch button clicked.")
        except TimeoutException:
            logging.info(f"Account {self.serial_number}: Launch button not found, proceeding.")

        logging.info(f"Account {self.serial_number}: NUTSFARM STARTED")
        sleep_time = random.randint(15, 20)
        logging.info(f"Sleeping for {sleep_time} seconds.")
        time.sleep(sleep_time)
        self.switch_to_iframe()

    def wait_for_element(self, by, value, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )

    def preparing_account(self):
        try:
            click_now_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Click now')]")
            click_now_button.click()
            sleep_time = random.randint(5, 7)
            logging.info(f"Sleeping for {sleep_time} seconds.")
            time.sleep(sleep_time)
        except NoSuchElementException:
            logging.info(f"Account {self.serial_number}: 'Click now' button is unnecessary.")

        try:
            time.sleep(8)
            welcome_claim_button = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/button")
            welcome_claim_button.click()
            time.sleep(3)
            logging.info(f"Account {self.serial_number}: Claimed welcome bonus: 1337 NUTS")
        except NoSuchElementException:
            logging.info(f"Account {self.serial_number}: Welcome bonus already claimed.")

    def get_balance(self):
        try:
            parent_block = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'flex items-center font-tt-hoves')]"))
            )
            
            visible_balance_elements = parent_block.find_elements(By.XPATH, ".//span[contains(@class, 'index-module_num__j6XH3') and not(@aria-hidden='true')]")
            balance_text = ''.join([element.get_attribute("textContent").strip() for element in visible_balance_elements])

            if len(balance_text) > 2:
                balance_text = balance_text[:-2] + '.' + balance_text[-2:]

            logging.info(f"Account {self.serial_number}: Current balance: {balance_text}")
            update_balance_table(self.serial_number, balance_text)

        except NoSuchElementException:
            logging.info(f"Account {self.serial_number}: Balance element not found.")
            update_balance_table(self.serial_number, 0)

    def get_time(self):
        try:
            parent_block = self.driver.find_element(By.XPATH, "//div[contains(@class, 'flex h-12 flex-1 items-center justify-center')]")
            visible_time_elements = parent_block.find_elements(By.XPATH, ".//span[contains(@class, 'index-module_num__j6XH3') and not(@aria-hidden='true')]")
            
            time_text = ''.join([element.get_attribute("textContent").strip() for element in visible_time_elements])
            formatted_time = f"{time_text[:2]}:{time_text[2:4]}:{time_text[4:6]}"

            logging.info(f"Account {self.serial_number}: Start farm will be available after: {formatted_time}")

        except NoSuchElementException:
            logging.info(f"Account {self.serial_number}: Time element not found.")


    def farming(self):
        try:
            start_farming_button = self.driver.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/main[1]/div[5]/button[1] | /html[1]/body[1]/div[1]/div[1]/main[1]/div[4]/button[1]/div[1]")
            start_farming_button.click()
            sleep_time = random.randint(3, 4)
            time.sleep(sleep_time)
        except NoSuchElementException:
            logging.info(f"Account {self.serial_number}: 'Start farming' button is not active. Farm probably already started.")

        try:
            collect_button = self.driver.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/main[1]/div[5]/button[1] | /html[1]/body[1]/div[1]/div[1]/main[1]/div[4]/button[1]/div[1]")
            collect_button.click()
            sleep_time = random.randint(3, 4)
            time.sleep(sleep_time)
            logging.info(f"Account {self.serial_number}: 'Collect' button clicked.")
        except NoSuchElementException:
            logging.info(f"Account {self.serial_number}: 'Collect' button is not active. Farm probably already started.")

        try:
            start_farming_button = self.driver.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/main[1]/div[5]/button[1] | /html[1]/body[1]/div[1]/div[1]/main[1]/div[4]/button[1]/div[1]")
            start_farming_button.click()
            sleep_time = random.randint(3, 4)
            time.sleep(sleep_time)
        except NoSuchElementException:
            logging.info(f"Account {self.serial_number}: 'Start farming' button is not active. Farm probably already started.")
