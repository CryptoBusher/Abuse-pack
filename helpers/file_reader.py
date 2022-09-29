"""
For manipulating txt and json files
"""

import json


class FileManager:
    """
    Class contains functions for manipulating txt and json files.
    """

    @staticmethod
    def read_json_file(file_name: str):
        """
        Method for reading json files
        :param file_name: str
        :return: json data
        """
        with open(f'{file_name}.json') as json_file:
            return json.load(json_file)

    @staticmethod
    def read_txt_file(file_name: str):
        """
        Method for reading txt files
        :param file_name: str
        :return: list
        """
        with open(f'{file_name}.txt') as file:
            return [line.rstrip() for line in file]

    @staticmethod
    def append_txt_file(file_name: str, data: str):
        """
        Method for saving txt files
        :param file_name: str
        :param data: str
        """

        with open(f'{file_name}.txt', 'a') as file:
            file.write(f'{data}\n')