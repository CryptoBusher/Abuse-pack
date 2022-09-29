"""
Class for manipulating Metamask wallet in browser
"""

import tkinter as tk

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec


class MetamaskAccount:
    """
    Class for metamask wallets manipulation
    """

    # for creating metamask accounts
    START_BUTTON = '/html/body/div[1]/div/div[2]/div/div/div/button'
    CREATE_NEW_WALLET_BUTTON = '//*[@id="app-content"]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/button'
    I_AGREE_BUTTON = '//button[@data-testid="page-container-footer-next"]'
    PASSWORD_INPUT = '//input[@autocomplete="new-password"]'
    CONFIRM_PASSWORD_INPUT = '//input[@autocomplete="confirm-password"]'
    AGREEMENT_CHECKBOX = '//div[@class="first-time-flow__checkbox"]'
    FINAL_CREATE_WALLET_BUTTON = '//button[@class="button btn--rounded btn-primary first-time-flow__button"]'
    CONTINUE_BUTTON = '//*[@id="app-content"]/div/div[2]/div/div/div[2]/div/div[1]/div[2]/button'
    REVEAL_SEED_FIELD = '//div[@class="reveal-seed-phrase__secret-blocker"]'
    SEEDPHRASE_DIV = '//*[@id="app-content"]/div/div[2]/div/div/div[2]/div[1]/div[1]/div[5]/div'
    REMIND_LATER_BUTTON = '//*[@id="app-content"]/div/div[2]/div/div/div[2]/div[2]/button[1]'
    PUBLIC_KEY_COPY_DIV = '//div[@class="selected-account__address"]'

    # for logging into metamask accounts
    WALLET_IMPORT_BUTTON = '//*[@id="app-content"]/div/div[2]/div/div/div[2]/div/div[2]/div[1]/button'
    NO_THX_BUTTON = '//button[@class="button btn--rounded btn-secondary page-container__footer-button"]'
    PASSWORD_INPUT_IMPORT = '//input[@id="password"]'
    CONFIRM_PASSWORD_INPUT_IMPORT = '//input[@id="confirm-password"]'
    AGREEMENT_CHECKBOX_IMPORT = '//input[@id="create-new-vault__terms-checkbox"]'
    FINAL_IMPORT_WALLET_BUTTON = '//button[@class="button btn--rounded btn-primary create-new-vault__submit-button"]'
    ALL_DONE_BUTTON = '//button[@class="button btn--rounded btn-primary first-time-flow__button"]'

    def __init__(self, password: str):
        self.public_key = None
        self.seed_phrase = None
        self.password = password

    def create_metamask_account(self, new_driver: webdriver):
        """
        Registers new metamask account using password from "config.json" file.
        :param new_driver: web-driver
        :return: bool
        """

        try:
            root = tk.Tk()
            wait = WebDriverWait(new_driver, 60)
            wait.until(ec.number_of_windows_to_be(2))

            new_driver.switch_to.window(new_driver.window_handles[1])

            wait.until(ec.element_to_be_clickable((By.XPATH, self.START_BUTTON))).click()
            wait.until(ec.element_to_be_clickable((By.XPATH, self.CREATE_NEW_WALLET_BUTTON))).click()
            wait.until(ec.element_to_be_clickable((By.XPATH, self.I_AGREE_BUTTON))).click()
            wait.until(ec.element_to_be_clickable((By.XPATH, self.PASSWORD_INPUT))).send_keys(self.password)
            new_driver.find_element(By.XPATH, self.CONFIRM_PASSWORD_INPUT).send_keys(self.password)
            new_driver.find_element(By.XPATH, self.AGREEMENT_CHECKBOX).click()
            wait.until(ec.element_to_be_clickable((By.XPATH, self.FINAL_CREATE_WALLET_BUTTON))).click()
            wait.until(ec.element_to_be_clickable((By.XPATH, self.CONTINUE_BUTTON))).click()
            wait.until(ec.element_to_be_clickable((By.XPATH, self.REVEAL_SEED_FIELD))).click()
            page_html = new_driver.execute_script('return document.getElementById("app-content").innerHTML')
            self.seed_phrase = page_html.split('<div class="reveal-seed-phrase__secret-words notranslate">')[1] \
                .split('</div>')[0]

            new_driver.find_element(By.XPATH, self.REMIND_LATER_BUTTON).click()
            wait.until(ec.presence_of_element_located((By.XPATH, self.PUBLIC_KEY_COPY_DIV))).click()
            self.public_key = root.clipboard_get()

            return True

        except:
            return False

    def login_to_metamask_account(self, new_driver: webdriver):
        """
        Registers new metamask account using password from "config.json" file.
        :param new_driver: web-driver
        :return: bool
        """

        try:
            wait = WebDriverWait(new_driver, 60)
            new_driver.get('chrome-extension://cfkgdnlcieooajdnoehjhgbmpbiacopjflbjpnkm/home.html#initialize/welcome')
            wait.until(ec.element_to_be_clickable((By.XPATH, self.START_BUTTON))).click()
            wait.until(ec.element_to_be_clickable((By.XPATH, self.WALLET_IMPORT_BUTTON))).click()
            wait.until(ec.element_to_be_clickable((By.XPATH, self.NO_THX_BUTTON))).click()

            splitted_seed = self.seed_phrase.split(' ')
            for i in range(12):
                xpath = f'/html/body/div[1]/div/div[2]/div/div/div[2]/form/div[1]/div[3]/div[{i+1}]/div[1]/div/input'
                word = splitted_seed[i]
                wait.until(ec.presence_of_element_located((By.XPATH, xpath))).send_keys(word)

            new_driver.find_element(By.XPATH, self.PASSWORD_INPUT_IMPORT).send_keys(self.password)
            new_driver.find_element(By.XPATH, self.CONFIRM_PASSWORD_INPUT_IMPORT).send_keys(self.password)
            new_driver.find_element(By.XPATH, self.AGREEMENT_CHECKBOX_IMPORT).click()
            wait.until(ec.element_to_be_clickable((By.XPATH, self.FINAL_IMPORT_WALLET_BUTTON))).click()
            wait.until(ec.element_to_be_clickable((By.XPATH, self.ALL_DONE_BUTTON))).click()

            return True

        except:
            return False