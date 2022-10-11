"""
Script for checking proxy validity
"""

from multiprocessing.dummy import Pool

import requests

good_proxies = []
bad_proxies = []

with open("data/proxies.txt", "r") as f:
    proxies = [line.rstrip() for line in f]


def check_proxy(_proxy: str):
    """
    Function for checking proxy
    :param _proxy: http proxy
    """

    try:
        print(f'Checking proxy: {_proxy}')
        url = 'https://api.ipify.org'
        _proxies = {
            'http': _proxy,
            'https': _proxy
        }
        response = requests.get(url, proxies=_proxies, timeout=timeout)

        if response.text == _proxy.split('@')[1].split(':')[0]:
            good_proxies.append(_proxy)
        else:
            bad_proxies.append(_proxy)
    except:
        bad_proxies.append(_proxy)


if __name__ == "__main__":
    threads = int(input("Enter amount of threads: "))
    timeout = float(input("Enter timeout in seconds: "))

    with Pool(processes=threads) as executor:
        executor.map(check_proxy, proxies)

    with open("data/good_proxies.txt", 'a') as f:
        for proxy in good_proxies:
            f.write(f'{proxy}\n')

    with open("data/bad_proxies.txt", 'a') as f:
        for proxy in bad_proxies:
            f.write(f'{proxy}\n')

    print("Finished checking proxies")
