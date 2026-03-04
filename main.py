# To run and test the code you need to update 4 places:
# 1. Change MY_EMAIL/MY_PASSWORD to your own details.
# 2. Go to your email provider and make it allow less secure apps.
# 3. Update the SMTP ADDRESS to match your email provider.
# 4. Update birthdays.csv to contain today's month and day.
# See the solution video in the 100 Days of Python Course for explainations.


# from datetime import datetime
# import pandas
# import random
# import smtplib
# import os

# # import os and use it to get the Github repository secrets
# MY_EMAIL = os.environ.get("MY_EMAIL")
# MY_PASSWORD = os.environ.get("MY_PASSWORD")

# today = datetime.now()
# today_tuple = (today.month, today.day)

# data = pandas.read_csv("birthdays.csv")
# birthdays_dict = {(data_row["month"], data_row["day"])                  : data_row for (index, data_row) in data.iterrows()}
# if today_tuple in birthdays_dict:
#     birthday_person = birthdays_dict[today_tuple]
#     file_path = f"letter_templates/letter_{random.randint(1, 3)}.txt"
#     with open(file_path) as letter_file:
#         contents = letter_file.read()
#         contents = contents.replace("[NAME]", birthday_person["name"])

#     with smtplib.SMTP("YOUR EMAIL PROVIDER SMTP SERVER ADDRESS") as connection:
#         connection.starttls()
#         connection.login(MY_EMAIL, MY_PASSWORD)
#         connection.sendmail(
#             from_addr=MY_EMAIL,
#             to_addrs=birthday_person["email"],
#             msg=f"Subject:Happy Birthday!\n\n{contents}"
#         )

import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
import os

API_KEY = os.environ.get("OWM_API_KEY")
OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast?"
params = {
    "lat" : 39.952583,
    "lon" : -75.165222,
    "appid" : API_KEY,
    "cnt" : 4,
}

TWILIO_FAILSAFE = "TXRTAJ88NU5K1QMM8GAQVT1L"

account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")

# URL = f"https://api.openweathermap.org/data/2.5/weather?q=conroe,texas&appid={API_KEY}"

response = requests.get(url=OWM_ENDPOINT,params=params)
print(response.raise_for_status())

weather_data = response.json()

will_rain = False
for hour_data in weather_data["list"]:
    condition_code = int(hour_data["weather"][0]["id"])
    if condition_code <700:
        will_rain = True
if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token,http_client=proxy_client)
    message = client.messages.create(
        from_="whatsapp:+14155238886",
        body="It is going to rain today!. Carry an umbrella!",
        to="whatsapp:+19367665010",
    )

    print(message.body)

