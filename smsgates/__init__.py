__all__ = ['AbstractSMSGate', 'VFGate']
from twill.commands import go, formvalue, submit, agent, code, notfind, find, follow, sleep

class _LogSilencer(object):
    def write(self, msg):
        pass

class AbstractSMSGate(object):
    """Abstract class for SMS gate

    Implements those public template methods that drive its behaviour.
    It is supposed to be used using the ``with`` statement:

        with MySMSGate() as gate:
            gate.send(some_text)
    """
    MY_HTTP_AGENT="Mozilla/5.0"
    def __init__(self, verbose=False, **kwargs):
        if not verbose:
            from twill import browser
            browser.OUT = _LogSilencer()
        self.setup(**kwargs)

    def setup(self, **kwargs):
        """
        :return: object ready to fire ``send``
        """
        return self

    def send(self, msg):
        raise NotImplemented("Must be implemented by it subclass")

    def close(self):
        return True

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        """
        This method is supposed to:
        - handle the exceptions risen authentication or ``send``
        - make any finalization/logout

        :return: Boolean to indicate success default True
        """

#       @todo: Should pass e and then e.type, e.value, e.traceback
        val = self.close(type, value, traceback)
        return val if val is not None else True

class VFGate(AbstractSMSGate):
    """tested with vodafone.ie"""
    
    def setup(self,
              login=None,
              password=None,
              SERVICE_URL="/myv/messaging/webtext/index.jsp",
              LOGIN_URL="https://www.vodafone.ie/myv/services/login/index.jsp",
              LOGOUT_URL="/myv/services/logout/Logout.shtml"):

        self.SERVICE_URL = SERVICE_URL
        self.LOGIN_URL = LOGIN_URL
        self.LOGOUT_URL = LOGOUT_URL
        self.MY_PHONE_NUMBER = login
        self.MY_PASSWORD = password

        agent(self.MY_HTTP_AGENT)
        go(self.LOGIN_URL)
        code(200)
        formvalue("Login", "username", self.MY_PHONE_NUMBER)
        formvalue("Login", "password", self.MY_PASSWORD)
        submit()
        code(200)
        notfind("check your details")
        find(self.SERVICE_URL)

    def send(self, msg, to):
        """
        @todo: add support for chunking the message
        @todo: add support for multiple recipients
        """
        follow(self.SERVICE_URL)
        formvalue("WebText", "message", msg)
        formvalue("WebText", "recipient_0", to)
        sleep(2)
        submit()
        code(200)
        find("Message sent!")

    def close(self, *e_info):
        follow(self.LOGOUT_URL)
        code(200)
        find("Sign in to")