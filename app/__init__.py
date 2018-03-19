import os
import json
from .get_email import FromIMAPMail
from .parse_email import Scrape
from .publish_geodata import Publish
from .logger import log


def scrape_onecall_info_from_emails_and_publish_to_map_from(config):
            # get emails
    retrieved_mail = FromIMAPMail(
        IMAP_SSL_HOST=config["get_from"]['IMAP_SSL_HOST'],
        IMAP_SSL_PORT=config["get_from"]['IMAP_SSL_PORT'],
        MAILBOX_USERNAME=config["get_from"]['MAILBOX_USERNAME'],
        MAILBOX_PASSWORD=config["get_from"]['MAILBOX_PASSWORD'],
        MAIL_FOLDER=config["get_from"]['MAIL_FOLDER'],
        MAIL_FROM=config["get_from"]['MAIL_FROM'],  # Delivery@pa1call.net
        MAIL_SUBJECT=config["get_from"]['MAIL_SUBJECT']
    ).retrieve()

    # scrape the e-mails
    all_scraped_data = []
    for each_mail in retrieved_mail:
        each = Scrape(each_mail)
        all_scraped_data.append(each.data)

    if all_scraped_data:
        # publish scraped data to feature service
        Publish(records=all_scraped_data).to_esri_agol_feature_service(
            ESRI_APP_CLIENT_ID=config["publish_to"]['ESRI_APP_CLIENT_ID'],
            ESRI_APP_CLIENT_SECRET=config["publish_to"]['ESRI_APP_CLIENT_SECRET'],
            ESRI_APP_TOKEN_EXPIRATION=3600,
            ESRI_AGOL_FEATURE_SERVICE_URL=config["publish_to"]['ESRI_AGOL_FEATURE_SERVICE_URL']
        )
    else:
        log.info("No new One Call notifications received.")
