"""smsgates open more options to send your SMS the way U like

- smsgates.contrib provides the different smsgates support
- smsgates.extras all candies like vCard contacts parsing
- sendsms script full functional day-to-day use or good starting point

Base classes used later in smsgates.contrib and smsgates.extras.
"""
from collections import namedtuple

__version__ = '0.0.2'
__about__ = 'Send your SMS the way U like'
__all__ = ['BaseFactory', 'Contact', 'ContactBook', 'AbstractSMSGate']


class BaseFactory(object):
    """@todo: document the _choices @property (can return list/dict)"""
    _choices = dict()

    @classmethod
    def get_class(cls, name=None):
        return cls()._choices[name]

    def __iter__(self):
        return iter(self._choices)


class _LogSilencer(object):
    def write(self, *args):
        pass


class Contact(object):
    """Contact class represents single user metadata

    :param alias - if not available ot will be same as fullname
    :param mobile optional - but contacts without it are ignored
    :param fullname - name + surname

    @todo: consider adding  support for:

        - groups,
        - multiple telephones
        - firstname, surname
    """
    alias = None
    mobile = None

    def __init__(self, alias=None, mobile=None, **kwargs):
        self.fullname = kwargs.get('name', '')
        self.alias = alias if alias else self.fullname
        self.mobile = mobile if mobile else kwargs.get('telephones').get(
            'mobile')

    def __hash__(self):
        return hash(tuple(vars(self).items()))

    def __eq__(self, other):
        return vars(self) == vars(other)

    def __repr__(self):
        return "Contact:: %s" % vars(self)

    def __str__(self):
        """
        :return: simple serialized contact data
        @todo: using csv by default: ?

            csv_str = StringIO.StringIO()
            writer = csv.writer(csv_str, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([getattr(self, k).strip() for k in sorted(vars(self).
                keys())])
            return csv_str.getvalue().strip()
        """
        out = ",".join([getattr(self, k) for k in sorted(vars(self).keys())])
        return out.encode('utf-8')


class ContactBook(set):
    def __init__(self, contacts=None, from_file=None, factory=None):
        if from_file:
            with from_file as f:
                parser = factory.get_class(from_file.name)
                contacts = parser(f.read())
        self._filters = {
            'exact': lambda c, k, v: getattr(c, k, '') == v,
            'iexact': lambda c, k, v: getattr(c, k, '').lower() == v.lower(),
            'like': lambda c, k, v: v in getattr(c, k, ''),
            'ilike': lambda c, k, v: v.lower() in getattr(c, k, '').lower(),
            'startswith': lambda c, k, v: getattr(c, k, '').startswith(v),
            'istartswith': lambda c, k, v: getattr(c, k, '').lower().
                startswith(v.lower()),
        }
        super(ContactBook, self).__init__(contacts)

    def search(self, **kwargs):
        """

        :param kwargs: single key-value filter ``PROP__FILTER=VALUE`` where:

            - *PROP* is the property to base the filter
            - *FILTER* is ONE from:
            -- exact
            -- iexact
            -- like
            -- ilike
            -- startswith
            -- istartswith
            - *VALUE* to filter on
        :return: set of contacts satisfying the filter criteria
        """

        k, v = kwargs.items()[0]
        k, fname = k.split('__') if "__" in k else (k, 'exact')
        finder = self._filters[fname]
        params_finder = lambda c: finder(c, k, v)
        return set(filter(params_finder, self))


class AbstractSMSGate(object):
    """Abstract class for SMS gate

    Implements those public template methods that drive its behaviour.
    It is supposed to be used using the ``with`` statement:

        with MySMSGate() as gate:
            gate.send(some_text)

    @todo: add tests
    """
    MY_HTTP_AGENT = "Mozilla/5.0"

    def __init__(self, verbose=False, **kwargs):
        if not verbose:
            from twill import browser
            browser.OUT = _LogSilencer()
        self.setup(**kwargs)

    def setup(self, *args, **kwargs):
        """
        :return: object ready to fire ``send``
        """
        return self

    def send(self, msg, *send_to):
        """
        @todo: add support for chunking the message
        @todo: add support for templating
        """
        raise NotImplementedError("Must be implemented by it subclass")

    def close(self, error_info=None):
        return False if error_info else True

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        """This method is supposed to:

        - handle the exceptions risen authentication or ``send``
        - make any finalization/logout
        :return: Boolean to indicate implementing exception handling
        """
        if type:
            ErrorInfo = namedtuple('ErrorInfo', ['type', 'value', 'traceback'])
            error_info = ErrorInfo(type, value, traceback)
            val = self.close(error_info)
        else:
            val = self.close()

        return val

