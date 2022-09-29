"""
Script for creating dolphin accounts in bulk
"""

from helpers import dolphin
from helpers import file_reader


def create_bulk_dolphin_profiles(dolphin_email: str, dolphin_pass: str, _proxies: list, _useragents: list):
    """
    Function for creating dolphin accounts in bulk based on proxies count
    :param dolphin_email: dolphin profile email
    :param dolphin_pass: dolphin profile pass
    :param _proxies: list of http proxies
    :param _useragents: list of useragents
    """

    print("Initializing dolphin account")
    dolphin_account = dolphin.DolphinAccount(dolphin_email, dolphin_pass)
    print("Dolphin account was initialized")

    dolphin_profiles = []
    for i, proxy in enumerate(_proxies):
        dolphin_profile = dolphin.DolphinProfile()
        dolphin_profile.create_new_profile(dolphin_account.authorization_token, str(i + 1), proxy, _useragents[i])

        dolphin_profiles.append(dolphin_profile)
        fr.append_txt_file("data/dolphin_profile_ids", dolphin_profile.browser_profile_id)
        print(f"Dolphin profile #{i+1} was created")


if __name__ == "__main__":
    fr = file_reader.FileManager

    config = fr.read_json_file("data/config")
    proxies = fr.read_txt_file("data/proxies")
    useragents = fr.read_txt_file("data/useragents")
    create_bulk_dolphin_profiles(config["dolphin_email"], config["dolphin_password"], proxies, useragents)
