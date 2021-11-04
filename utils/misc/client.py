import logging

import requests


async def send_packet(url: str, data: dict):
    """
    :param url: str - user server address
    :param data: dict - user computer mac address
    :returns None or info about incorrect data:
    function, which will be start set server address state
    """
    answer = requests.post(url, json=data)
    return 1 if answer.status_code == 200 else 0
