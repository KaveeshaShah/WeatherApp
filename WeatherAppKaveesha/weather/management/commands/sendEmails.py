from django.core.management.base import BaseCommand, CommandError
import requests
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from weather.models import User,Location
import os

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        locations={}
        sender_email = "klaviyoweatherapp6@gmail.com"
        API_KEY=os.environ["my_api_key"]
        password = input("Type your password and press enter:")
        
        #store required info for all unique locations so that we don't call the api multiple times redundantly
        for user in User.objects.all():
            if user.location.id not in locations:
                current_api_link='http://api.weatherbit.io/v2.0/current?city={}&key={}'.format(user.location.city,API_KEY)
                forecast_api_link= 'https://api.weatherbit.io/v2.0/forecast/daily?city={}&key={}'.format(user.location.city,API_KEY)
                response1 = requests.get(current_api_link)
                response2 = requests.get(forecast_api_link)
                #Save the current temperature, forecasted temperature, weather code in the location dictionary
                locations[user.location]=[response1.json()['data'][0]['temp'],response2.json()['data'][0]['temp'],int(response1.json()['data'][0]['weather']['code']),response1.json()['data'][0]['weather']['description']]
                
        print(locations)
        
        for user in User.objects.all():
            receiver_email = user.email_id
            curr_temp=locations[user.location][0]
            forecasted_temp=locations[user.location][1]
            weather_code=locations[user.location][2]
            diff_temp=curr_temp-forecasted_temp
            description=locations[user.location][3]
            
            message = MIMEMultipart("alternative")
            
            if diff_temp>=5 or weather_code==800:
                message["Subject"] = "It's nice out! Enjoy a discount on us."
            elif diff_temp<=-5 or (weather_code%100 in [2,3,5,6,9]):
                message["Subject"] = "Not so nice out? That's okay, enjoy a discount on us."
            else:
                message["Subject"] = "Enjoy a discount on us."
                
            message["From"] = sender_email
            message["To"] = receiver_email
            
            # Create the plain-text and HTML version of your message
            html = """\
            <html>
              <body>
                <p>Hi,<br>
                   How are you?<br>
                   Looks like the temperature in {} is {} degrees Celsius today.<br> Tomorrow its going to be {} degrees Celsius.<br> The weather today has {}.<br>
                   Looking for something interesting to do in this weather? Come visit the <a href="https://www.klaviyo.com/">Klaviyo website</a> 
                </p>
                <img src="https://getvectorlogo.com/wp-content/uploads/2019/07/klaviyo-vector-logo.png">
              </body>
            </html>
            """.format(user.location.city,curr_temp,forecasted_temp,description)

            # Turn these into plain/html MIMEText objects
            part2 = MIMEText(html, "html")

            # Add HTML/plain-text parts to MIMEMultipart message
            # The email client will try to render the last part first
            message.attach(part2)

            # Create secure connection with server and send email
            #context = ssl.create_default_context()
            smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo()
            smtpserver.login(sender_email, password)
            smtpserver.sendmail(sender_email, receiver_email, message.as_string())

                