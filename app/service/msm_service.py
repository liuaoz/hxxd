import asyncio

import requests

from config.msm_config import YP_BASE_URL


def fetch_url(url, data):
    return requests.post(url, data=data)


async def single_send(text, mobile):
    loop = asyncio.get_event_loop()
    url = f'{YP_BASE_URL}/single_send.json'
    resp = await loop.run_in_executor(None, lambda: fetch_url(url, {'text': text, 'mobile': mobile}))
    return resp.json()


if __name__ == '__main__':
    asyncio.run(single_send('Hello', '1234567890'))
