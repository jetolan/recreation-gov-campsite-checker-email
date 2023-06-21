import camping
import datetime
from email.message import EmailMessage
import smtplib,ssl
import json
import time



def send_email(message, sender_email, password, receiver_email):
    #https://realpython.com/python-send-email/
    #https://support.google.com/accounts/answer/185833?hl=en

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


def check_site(park_id, start_date, end_date, sender_email, password, receiver_email):
    # https://github.com/banool/recreation-gov-campsite-checker
    success=False
    while not success:
        try:
            num_avail, total, _, name=camping.check_park(park_id=park_id, start_date=start_date, end_date=end_date, campsite_type=None)
            success=True
        except RuntimeError:
            time.sleep(20)
    cur_time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    message = f"{num_avail} sites available at {name} on {start_date} [{cur_time}]"
    print(message)
    if num_avail>0:
        #send email
        print('sending email')
        message = f"{num_avail} sites available at {name} on {start_date}"
        print(message)
        send_email(message, sender_email, password, receiver_email)
    return message
    
if __name__=="__main__":
    #nb this is system dependent
    path="/Users/jetolan/src/recreation-gov-campsite-checker-email"

    with open(f'{path}/cred.json') as src:
        data = json.load(src)
    sender_email=data['sender_email']
    password=data['password']
    receiver_email=data['receiver_email']

    outfile=f'{path}/log.csv'
    
    
    park_id=232466 #cougar rock campground
    start_date=datetime.date(2023, 8, 19)
    end_date=datetime.date(2023, 8, 20)

    message=check_site(park_id, start_date, end_date, sender_email, password, receiver_email)
    with open(outfile, 'a') as f:
        f.write(f"{message},\n")
    
    park_id=246855 #colonial creek north campground
    start_date=datetime.date(2023, 8, 26)
    end_date=datetime.date(2023, 8, 27)

    message=check_site(park_id, start_date, end_date, sender_email, password, receiver_email)
    with open(outfile, 'a') as f:
        f.write(f"{message},\n")
    
    park_id=255201 #colonial creek south campground
    start_date=datetime.date(2023, 8, 26)
    end_date=datetime.date(2023, 8, 27)

    message=check_site(park_id, start_date, end_date, sender_email, password, receiver_email)
    with open(outfile, 'a') as f:
        f.write(f"{message},\n")
    
    park_id=234039 #manzanita lake
    start_date=datetime.date(2023, 7, 2)
    end_date=datetime.date(2023, 7, 3)
    
    message=check_site(park_id, start_date, end_date, sender_email, password, receiver_email)
    with open(outfile, 'a') as f:
        f.write(f"{message},\n")

