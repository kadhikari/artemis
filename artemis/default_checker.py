from flask.ext.restful import fields
from artemis.utils import Checker, WhiteListMask, BlackListMask, SubsetComparator, RetrocompatibilityMask

"""
The default behaviour for journeys is to check only a subset journey

the mask create a new dict filtering only the wanted elt
"""


section = {
    "duration": fields.Raw,
    "departure_date_time": fields.Raw,
    "arrival_date_time": fields.Raw,
    'from': fields.Raw(attribute='from.name'),
    'to': fields.Raw(attribute='to.name'),
    'type': fields.Raw,
}

journey = {
    'duration': fields.Raw,
    'nb_transfers': fields.Raw,
    'departure_date_time': fields.Raw,
    'arrival_date_time': fields.Raw,
    'sections': fields.List(fields.Nested(section)),
    'type': fields.Raw,
}

default_journey_checker = Checker(filters=[WhiteListMask(
    mask={"journeys": fields.List(fields.Nested(journey))}
)])


def replace_hyperlink(text):
    # we don't want full urls in the response, since it will change depending on where the test in run
    # so we remove the server address
    import re
    return re.sub("http:\\\\/\\\\/.+?\\\\/v1\\\\/",
                  "http:\\/\\/SERVER_ADDR\\/v1\\/", text)


nullify_elem = lambda x: None

# Note: two dots between '$' and 'disruptions[*]' will match ALL (even nested) disruptions under root
DEFAULT_BLACKLIST_MASK = (('$..disruptions[*].disruption_uri', nullify_elem),
                          ('$..disruptions[*].disruption_id', nullify_elem),
                          ('$..disruptions[*].impact_id', nullify_elem),
                          ('$..disruptions[*].uri', nullify_elem),
                          ('$..disruptions[*].id', nullify_elem),
                          ('$..disruptions[*].updated_at', nullify_elem),
                          ('$..ref', replace_hyperlink))

default_checker = Checker(filters=[RetrocompatibilityMask(),
                                   BlackListMask(DEFAULT_BLACKLIST_MASK)],
                          comparator=SubsetComparator())
