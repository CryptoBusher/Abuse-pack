"""
Script for generating a list of random useragents
"""

from user_agent import generate_user_agent

from helpers import file_reader


def generate_useragents(amount: int, _chrome_version: str):
    """
    Function for generating random useragents
    :param amount: amount of user agents to be generated
    :param _chrome_version: chrome driver version
    """

    fr = file_reader.FileManager

    for i in range(amount):
        while True:
            user_agent = generate_user_agent(os='mac')
            if f'Chrome/' in user_agent:
                useragent_list = user_agent.split(' ')
                useragent_list[-2] = f'Chrome/{_chrome_version}'
                new_useragent = (" ".join(useragent_list))

                fr.append_txt_file("data/useragents", new_useragent)
                break

    print(f"Saved {amount} useragents to txt file")


if __name__ == "__main__":
    amount_of_useragents = int(input("Enter amount of useragents to be generated: "))
    chrome_version = str(input("Enter chrome driver version: "))
    generate_useragents(amount_of_useragents, chrome_version)
