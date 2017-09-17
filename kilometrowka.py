import os
import sys
import requests
import datetime

def public_holidays(year, month):
    url = 'https://holidayapi.com/v1/holidays?key={}&country=PL&year={}&month={}'.format(
        os.getenv('HOLIDAY_API_KEY'),
        year,
        month,
    )
    response = requests.get(url)
    response.raise_for_status()

    json = response.json()
    holidays = json.get('holidays', [])
    return [datetime.datetime.strptime(holiday['date'], '%Y-%m-%d').date() for holiday in holidays]

def generate_data(year, month):
    holidays = set(public_holidays(year, month))

    date = datetime.date(year=year, month=month, day=1)
    days = []
    while date.month == month:
        if date not in holidays and date.weekday() <= 4:
            days.append(date)
        date += datetime.timedelta(days=1)

    print(days)

if __name__ == '__main__':
    year, month = map(int, sys.argv[1:3])
    generate_data(year, month)