from threading import Thread


class EmailThread(Thread):
    def __init__(self, email_obj):
        Thread.__init__(self)
        self.email_obj = email_obj

    def run(self):
        self.email_obj.send()
