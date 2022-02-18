import json
import logging
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup
import shelve

from wuzzufbot.config import *

log = logging.getLogger(__name__)


def _parse_jobs():
    try:
        request = requests.get(WUZZUF_JOBS_URL)

        bs4 = BeautifulSoup(request.content, "html.parser")

        match = re.search(r"Wuzzuf\.initialStoreState = (.*);", str(bs4))
        json_str = match.group(1)
        json_obj = json.loads(json_str)
        jobs = json_obj['entities']['job']['collection']
        parsed_jobs = []

        for key in jobs:
            job = jobs[key]['attributes']
            datetime_object = datetime.strptime(job['postedAt'],
                                                '%m/%d/%Y %H:%M:%S')
            timestamp = datetime.timestamp(datetime_object)
            parsed_jobs.append({
                'id': key,
                'title': job['title'],
                'postedAt': job['postedAt'],
                'timestamp': timestamp
            })

        return parsed_jobs

    except Exception as e:
        log.error(str(e))
        return {}


def _get_last_job_data():
    with shelve.open(CONFIG_PATH) as db:
        try:
            data = {
                'id': db['last_job_id'],
                'timestamp': db['last_job_timestamp']
            }
            return data
        except:
            return None


def _set_last_job_data(id, timestamp):
    with shelve.open(CONFIG_PATH) as db:
        db['last_job_id'] = id
        db['last_job_timestamp'] = timestamp


def parse_jobs():
    """function to parse wuzzuf jobs from url in config.py

    Returns:
        list: list of jobs sorted by time
    """
    jobs = _parse_jobs()
    sorted_jobs = sorted(jobs, key=lambda j: j['timestamp'])
    return sorted_jobs


def parse_new_jobs():
    """function to parse only new jobs

    Returns:
        list: list of new jobs sorted by time
    """
    jobs = _parse_jobs()

    last_job_data = _get_last_job_data()

    if last_job_data:
        jobs = filter(lambda j: j['timestamp'] > last_job_data['timestamp'],
                      jobs)

    sorted_new_jobs = sorted(jobs, key=lambda j: j['timestamp'])

    if len(sorted_new_jobs) > 0:
        _set_last_job_data(sorted_new_jobs[-1]['id'],
                           sorted_new_jobs[-1]['timestamp'])
    return sorted_new_jobs