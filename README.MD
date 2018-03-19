# PA OneCall Mapper

This routine gets PA One Call tickets from an e-mail inbox publishes them to a geodata web service so they it can be viewed on a map.

It's designed to listen for new One Call e-mails on one or more inboxes and publish to one or more geodata service endpoints. It checks what has been published already, and so won't re-publish/duplicate old tickets if the inbox gets messy.

Currently:

* only Esri AGOL Feature Services are supported as endpoints;
* it only parses and publishes the request Serial Number, Mapped Type, and Mapped Lat/Lon information from the ticket. Other information is linked in via a related table in the published service.

We may extend the scope of the project in the future; e.g., support for other types of geodata services endpoints and formats (e.g., geojson in a GitHub repository, a table in CARTO, etc.)

## Software

This is built with Python 3.6 and uses the Python Requests library. We use `pipenv` for a python package and virtual environment management.

We run it as a CRON job every six hours; it could also easily be run as a Windows task.
