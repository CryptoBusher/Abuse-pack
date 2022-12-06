"""
Script for logging into discord accounts via token
"""

import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

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


def login_to_discord_accounts(_dolphin_profile_ids: list, _discord_tokens: str):
    """
    Function for logging to discord accounts via token in bulk
    :param _dolphin_profile_ids: list of dolphin profile ids
    :param _discord_tokens: list of discord tokens
    """

    for _i, dolphin_profile_id in enumerate(_dolphin_profile_ids):
        print(f"Working with account #{_i + 1}")

        _dolphin_profile = init_dolphin_profile(dolphin_profile_id)
        profile_started = _dolphin_profile.start_profile()

        if not profile_started:
            print(f"Failed to start profile with id {dolphin_profile_id}, skipping")
            continue

        _webdriver = init_selenium_driver(_dolphin_profile.window_port)
        # LOGIN TO DISCORD

        script = """
                function login(token) {
                setInterval(() => {
                document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token=`"${token}"`
                }, 50);
                setTimeout(() => {
                location.reload();
                }, 2500);
                }   
                """

        _webdriver.get("https://discordapp.com/login")
        _webdriver.execute_script(script + f'\nlogin("{_discord_tokens[_i]}")')

        time.sleep(2)

        while True:
            if _webdriver.current_url == 'https://discord.com/channels/@me':
                print(f"Successfully logged in to discord account {dolphin_profile_id}")
                time.sleep(2)
                break

        profile_stopped = _dolphin_profile.stop_profile()

        if not profile_stopped:
            print(f"Failed to stop profile with id {dolphin_profile_id}, do it manually")
            continue

    print(f"Finished logging to metamask accounts")


if __name__ == "__main__":
    config = fr.read_json_file("data/config")
    dolphin_profile_ids = fr.read_txt_file("data/dolphin_profile_ids")
    discord_tokens = fr.read_txt_file("data/discord_tokens")

    login_to_discord_accounts(dolphin_profile_ids, discord_tokens)
