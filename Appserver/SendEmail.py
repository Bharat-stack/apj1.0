import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def SendOtp(sender_email, receiver_email, password, otp):

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
 
    #    sender_email = "gk.411995@gmail.com"  # Enter your address
    #    receiver_email = "gk.441995@gmail.com"  # Enter receiver address
    #   password = "12wedfvbabc"
    try:
        message = MIMEMultipart("Welocome to celebrate")
        message["Subject"] = "Welocome to celebrate"
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create the plain-text and HTML version of your message

        html = """\
        <html>
        <body>
            <p>Hi,<br>
            Please find your OTP below<br> 
            {otp}
            </p>
        </body>
        </html>
        """.format(otp=otp)

        # Turn these into plain/html MIMEText objects
    
        part1 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        
        message.attach(part1)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
        
        return {"status":"success"}

    except Exception as e:
        return {
            "status":"fail",
            "reason":str(e)
        }

   