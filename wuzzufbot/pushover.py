import logging

import aiohttp

from wuzzufbot.config import *

log = logging.getLogger(__name__)


async def push_notification(job_list):
    try:
        if not PUSHOVER_TOKEN or not PUSHOVER_USER:
            log.error(f'pushover credientials not found')
            return
        # prettify message
        message = '\n'.join([
            '💼 Job: {} || Posted At: {} 💼'.format(j['title'], j['postedAt'])
            for j in job_list
        ])
        async with aiohttp.ClientSession() as session:
            async with session.post("https://api.pushover.net/1/messages.json",
                                    data={
                                        "token": PUSHOVER_TOKEN,
                                        "user": PUSHOVER_USER,
                                        "message": message
                                    },
                                    timeout=30) as response:
                if response.status == 200:
                    log.info('pushover notification sent')
                else:
                    log.error(
                        f'pushover notification faild - status code {response.status}'
                    )
    except Exception as e:
        log.error(str(e))
