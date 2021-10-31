import logging

import requests


async def send_packet(url: str, data: dict):
    logging.info(url)
    answer = requests.post(url, json=data)
    answer = answer.json()
    return 1 if answer['status'] == 200 else 0



