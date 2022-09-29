"""
Dolphin Anty manipulation
"""

import json

import requests


class DolphinAccount:
    """
    Class for init dolphin account object with credentials and generate access token.
    """

    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password
        self.authorization_token = None
        self.__authorise_account()

    def __authorise_account(self) -> bool:
        """
        Method for authorising account for future api calls.
        :return: is dolphin account initialized
        """

        url = 'https://anty-api.com/auth/login'
        payload = {'username': self.login, 'password': self.password}
        response = requests.post(url, data=payload)
        json_response = json.loads(response.text)

        self.authorization_token = json_response['token']


class DolphinProfile:
    """
    Class that contains methods for manipulating Dolphin profiles using local API.
    """

    def __init__(self):
        self.browser_profile_id = None
        self.window_port = None
        self.window_endpoint = None

    @staticmethod
    def __parse_proxy(proxy):
        proxy_host = proxy.split('@')[1].split(':')[0]
        proxy_port = proxy.split('@')[1].split(':')[1]
        proxy_login = proxy.split('@')[0].split('//')[1].split(':')[0]
        proxy_password = proxy.split('@')[0].split('//')[1].split(':')[1]

        return proxy_host, proxy_port, proxy_login, proxy_password

    def create_new_profile(self, authorization_token: str, name: str, proxy: str, useragent: str) -> bool:
        """
        Create new profile in Dolphin browser using local API.
        :param name: name of profile
        :param proxy: http proxy
        :param useragent: useragent
        :param authorization_token: str
        :return: is new profile created
        """

        proxy_host, proxy_port, proxy_login, proxy_password = self.__parse_proxy(proxy)

        url = 'https://anty-api.com/browser_profiles'
        headers = {'Authorization': authorization_token}
        payload = {
            'name': name,
            'platform': 'windows',
            'mainWebsite': 'crypto',
            'useragent[mode]': 'manual',
            'useragent[value]': useragent,
            'webrtc[mode]': 'altered',
            'canvas[mode]': 'real',
            'webgl[mode]': 'real',
            'webglInfo[mode]': 'noise',
            'timezone[mode]': 'auto',
            'locale[mode]': 'auto',
            'geolocation[mode]': 'auto',
            'cpu[mode]': 'real',
            'memory[mode]': 'real',
            'browserType': "['anty']",
            'proxy[type]': 'http',
            'proxy[host]': proxy_host,
            'proxy[port]': proxy_port,
            'proxy[login]': proxy_login,
            'proxy[password]': proxy_password,
            'proxy[name]': name
        }

        try:
            response = requests.post(url, headers=headers, data=payload)
            json_response = json.loads(response.text)

            if json_response['success'] != 1:
                return False
            else:
                self.browser_profile_id = json_response['browserProfileId']
                return True
        except:
            return False

    def delete_profile(self, authorization_token: str) -> bool:
        """
        Deletes profile in Dolphin browser.
        :return: is account deleted
        """

        url = f"https://anty-api.com/browser_profiles/{self.browser_profile_id}"
        authorization = f"Bearer {authorization_token}"
        headers = {'Authorization': authorization}
        response = requests.delete(url, headers=headers)

        try:
            json_response = json.loads(response.text)
            if json_response['success']:
                return True
        except:
            return False

    def start_profile(self) -> bool:
        """
        Starts profile in Dolphin browser.
        :return: is profile started
        """

        url = f'http://localhost:3001/v1.0/browser_profiles/{self.browser_profile_id}/start?automation=1'
        response = requests.get(url)
        json_response = json.loads(response.text)
        if json_response['success']:
            self.window_port = json_response['automation']['port']
            self.window_endpoint = json_response['automation']['wsEndpoint']
            return True
        else:
            return False

    def stop_profile(self) -> bool:
        """
        Stops profile in Dolphin browser.
        :return: is profile deleted
        """

        url = f'http://localhost:3001/v1.0/browser_profiles/{self.browser_profile_id}/stop'
        response = requests.get(url)
        json_response = json.loads(response.text)
        if json_response['success']:
            return True
        else:
            return False
