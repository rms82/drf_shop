from threading import Thread
from django.core.mail import send_mail

class EmailThread(Thread):
    def __init__(self, email_obj):
        Thread.__init__(self)
        self.email_obj = email_obj
    
    def run(self):
        send_mail(
            "Subject here",
            "You have registered to the site.",
            "from@example.com",
            [f"{self.email_obj}"],
            fail_silently=False,
        )
        # self.email_obj.sends()
         