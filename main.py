import logging
import random
import time
from telegram_bot_automation import TelegramBotAutomation
from utils import read_accounts_from_file, write_accounts_to_file, reset_balances, print_balance_table

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_accounts():
    while True:
        reset_balances()
        accounts = read_accounts_from_file()
        random.shuffle(accounts)
        write_accounts_to_file(accounts)

        for account in accounts:
            retry_count = 0
            success = False

            while retry_count < 3 and not success:
                bot = TelegramBotAutomation(account)
                try:
                    bot.navigate_to_bot()
                    bot.send_message("https://t.me/secrettelegramchannelalllinks")
                    bot.click_link()
                    bot.preparing_account()
                    bot.get_balance()
                    bot.farming()
                    bot.get_time()
                    bot.get_balance()
                    logging.info(f"Account {account}: Processing completed successfully.")
                    success = True  
                except Exception as e:
                    logging.warning(f"Account {account}: Error occurred on attempt {retry_count + 1}: {e}")
                    retry_count += 1  
                finally:
                    logging.info("-------------END-----------")
                    bot.browser_manager.close_browser()
                    logging.info("-------------END-----------")
                    sleep_time = random.randint(5, 15)
                    logging.info(f"Sleeping for {sleep_time} seconds.")
                    time.sleep(sleep_time)
                
                if retry_count >= 3:
                    logging.warning(f"Account {account}: Failed after 3 attempts.")

            if not success:
                logging.warning(f"Account {account}: Moving to next account after 3 failed attempts.")

        print_balance_table()
        logging.info("All accounts processed. Waiting 8 hours before restarting.")
        for hour in range(8):
            logging.info(f"Waiting... {8 - hour} hours left till restart.")
            time.sleep(60 * 60)

if __name__ == "__main__":
    process_accounts()
