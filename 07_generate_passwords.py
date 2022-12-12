"""
Script for generating passwords
"""

import random
import string


def get_random_password(symbols_count: int):
    """
    Returns password with length based on symbols count passed.
    There will be mandatory lowercase letter, uppercase letter, digit and special symbol.
    :param symbols_count: symbols count
    :return: generated password
    """

    random_source = string.ascii_letters + string.digits + string.punctuation

    _password = random.choice(string.ascii_lowercase)
    _password += random.choice(string.ascii_uppercase)
    _password += random.choice(string.digits)
    _password += random.choice(string.punctuation)

    for i in range(symbols_count - len(_password)):
        _password += random.choice(random_source)

    password_list = list(_password)
    random.SystemRandom().shuffle(password_list)
    _password = ''.join(password_list)
    return _password


if __name__ == "__main__":
    min_length = int(input("Enter minimum password length: "))
    max_length = int(input("Enter maximum password length: "))
    amount = int(input("Enter amount of passwords to be generated: "))

    all_passwords = []
    for password in range(amount):
        length = random.randint(min_length, max_length)
        all_passwords.append(get_random_password(length))

    with open('data/generated_passwords.txt', 'w') as f:
        for password in all_passwords:
            f.write(password + '\n')
