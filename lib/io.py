from ics import Calendar, Event
import requests


def read_calendar(link: str) -> Calendar:
    return Calendar(requests.get(link).text)
