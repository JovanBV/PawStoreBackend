import os
import resend
from dotenv import load_dotenv


load_dotenv()

if not os.environ["RESEND_API_KEY"]:
    raise EnvironmentError("RESEND_API_KEY is missing.")

resend.api_key = os.getenv("RESEND_API_KEY")

def send_email(user_email, cart_info):
    try:
        message = "<p>Confirmacion de compra en PawStore!</p>"
        for item in cart_info['items']:
            message += f"<p>{item['name']}: {item['price']} x {item['amount']}</p>"
        message += f"<p>Gracias por comprar con nosotros!</p>"
        
        email = resend.Emails.send({
            "from": "PawStore <onboarding@resend.dev>",
            "to": [f"{user_email}"],
            "subject": "Your recent purchase in PawStore",
            "html": f"{message}"
        })
        print("Email send successfully: ", email)
    except Exception as e:
        print("Error sending email: ", e)
