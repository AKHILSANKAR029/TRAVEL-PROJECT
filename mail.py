import smtplib

def email(recv,otp):
    sender = 'chodagamthanuja01@outlook.com'
    receivers = recv
    message = """
    Your One Time Password is: """+str(otp)+"""
    """
    smtp = smtplib.SMTP("smtp.office365.com",587)
    smtp.starttls()
    smtp.login('chodagamthanuja01@outlook.com', 'Thanujach@0810')
    smtp.sendmail(sender, receivers, message)

    