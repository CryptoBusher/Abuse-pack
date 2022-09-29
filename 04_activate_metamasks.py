"""
Script for activating Metamask accounts in dolphin profiles
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from helpers import metamask
from helpers import file_reader
from helpers import dolphin


fr = file_reader.FileManager


def init_dolphin_profile(dolphin_profile_id: str):
    """
    Function for initializing dolphin profile object with given dolphin profile id
    :param dolphin_profile_id: id of dolphin profile
    :return: DolphinProfile object
    """

    _dolphin_profile = dolphin.DolphinProfile()
    _dolphin_profile.browser_profile_id = dolphin_profile_id

    return _dolphin_profile


def init_selenium_driver(window_port: str):
    """
    Init selenium webdriver for connecting to Dolphin profile.
    :param window_port: window port for connection
    :return: selenium driver object
    """

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("debuggerAddress", f'127.0.0.1:{window_port}')

    ser = Service("./chromedriver.exe")
    return webdriver.Chrome(service=ser, options=chrome_options)


def activate_metamask_accounts(_dolphin_profile_ids: list, _metamask_password: str, _metamask_seeds: list):
    """
    Function for logging to metamask accounts in bulk
    :param _metamask_seeds: seeds as list
    :param _dolphin_profile_ids: list of dolphin profile ids
    :param _metamask_password: password for all metamask accounts
    """

    for _i, dolphin_profile_id in enumerate(_dolphin_profile_ids):
        print(f"Working with account #{_i + 1}")

        metamask_account = metamask.MetamaskAccount(_metamask_password)
        metamask_account.seed_phrase = _metamask_seeds[_i]

        _dolphin_profile = init_dolphin_profile(dolphin_profile_id)
        profile_started = _dolphin_profile.start_profile()

        if not profile_started:
            print(f"Failed to start profile with id {dolphin_profile_id}, skipping")
            continue

        _webdriver = init_selenium_driver(_dolphin_profile.window_port)
        logged_to_metamask_account = metamask_account.login_to_metamask_account(_webdriver)

        if not logged_to_metamask_account:
            print(f"Failed to login to metamask account for profile {dolphin_profile_id}")
        else:
            print(f"Successfully logged to metamask account in profile {dolphin_profile_id}")

        profile_stopped = _dolphin_profile.stop_profile()

        if not profile_stopped:
            print(f"Failed to stop profile with id {dolphin_profile_id}, do it manually")
            continue

    print(f"Finished logging to metamask accounts")


if __name__ == "__main__":
    config = fr.read_json_file("data/config")
    dolphin_profile_ids = fr.read_txt_file("data/dolphin_profile_ids")
    metamask_data = fr.read_txt_file("data/generated_metamasks")

    metamask_seeds = []

    for account in metamask_data:
        metamask_seeds.append((account.split(':')[1]))

    start = int(input('Enter starting point: '))
    end = int(input("Enter ending point: "))

    activate_metamask_accounts(dolphin_profile_ids[start-1:end], config["metamask_password"],
                               metamask_seeds[start-1:end])
