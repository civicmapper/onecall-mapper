from app import FromIMAPMail, Publish, Scrape, log
from app import scrape_onecall_info_from_emails_and_publish_to_map_from
import json

from config import mailboxes

if __name__ == "__main__":
    for this_mailbox in mailboxes:
        scrape_onecall_info_from_emails_and_publish_to_map_from(this_mailbox)