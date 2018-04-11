from google.appengine.ext import ndb


class Organization(ndb.Model):
    """
    Models an individual Organization with a domain.
    id should be set to the encoded organization id
    """
    domain = ndb.StringProperty()