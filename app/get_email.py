import time
from itertools import chain
import email
import imaplib
import datetime
import json

from .logger import log
from .utils import Utils


# ------------------------------------------------------
# CONFIGURATION


class FromIMAPMail(Utils):

    def __init__(
        self,
        IMAP_SSL_HOST,
        IMAP_SSL_PORT,
        MAILBOX_USERNAME,
        MAILBOX_PASSWORD,
        MAIL_FOLDER,
        MAIL_FROM,
        MAIL_SUBJECT
    ):
        self.imap_ssl_host = IMAP_SSL_HOST
        self.imap_ssl_port = IMAP_SSL_PORT
        self.username = MAILBOX_USERNAME
        self.password = MAILBOX_PASSWORD
        self.folder = MAIL_FOLDER

        # Restrict mail search. Be very specific.
        # Machine should be very selective to receive messages.
        self.mail_search_criteria = {
            'FROM': MAIL_FROM,
            'SUBJECT': MAIL_SUBJECT
            # 'BODY': MAIL_BODY_SIGNATURE,
        }

        self.mails = []

    # ------------------------------------------------------
    # HELPERS

    # def _get_uids_from_log(self, key='uids'):
    #     with open(SCRAPER_LOG, 'r') as fp:
    #         d = json.load(fp)
    #     return d[key]

    # def _append_uids_to_log(self, uids, key='uids'):
    #     d = None
    #     with open(SCRAPER_LOG, 'r') as fp:
    #         d = json.load(fp)
    #     if d:
    #         d[key].extend(uids)
    #         with open(SCRAPER_LOG, 'w') as fp:
    #             json.dump(d, fp)

    def _imap_search_string(self, uid_max, criteria):
        """Produce full search string in IMAP format:
        e.g. (FROM "me@gmail.com" SUBJECT "abcde" BODY "123456789" UID 9999:*)

        Arguments:
            uid_max {int} -- ...
            criteria {dict} -- FROM, SUBJECT, and BODY in a dictionry

        Returns:
            {string} -- search string in IMAP format
        """
        c = list(
            map(lambda t: (t[0], '"' + str(t[1]) + '"'), criteria.items())
        ) + [('UID', '%d:*' % (uid_max + 1))]
        r = '(%s)' % ' '.join(chain(* c))
        print(r, type(r))
        return r

    def _imap_search_string_lite(self, criteria):
        # c = '(FROM "{0}" SUBJECT "{1}")'.format(
        #     criteria['FROM'],
        #     criteria['SUBJECT']
        # )
        c = '(FROM "{0}")'.format(
            criteria['FROM']
        )
        return c

    def _get_first_text_block(self, msg):
        type = msg.get_content_maintype()

        if type == 'multipart':
            for part in msg.get_payload():
                if part.get_content_maintype() == 'text':
                    return part.get_payload()
        elif type == 'text':
            return msg.get_payload()

    # ------------------------------------------------------
    # WORK

    def retrieve(self):
        log.info("CHECKING MAIL...")
        # get list of message uids that we've logged
        # logged_uids = self._get_uids_from_log()
        # print("logged_uids", logged_uids)

        # get uids from server

        # Have to login/logout each time because that's the only way to get fresh results.
        server = imaplib.IMAP4_SSL(self.imap_ssl_host, self.imap_ssl_port)
        server.login(self.username, self.password)
        server.select(self.folder)

        # find messages in the INBOX meeting the search criteria
        # result, data = server.uid('search', None, _imap_search_string(self.mail_search_criteria))
        result, data = server.search(
            None,
            self._imap_search_string_lite(self.mail_search_criteria)
        )
        # print(result, data)
        uids_on_server = [int(s) for s in data[0].split()]
        log.info(
            "{0} matching e-mails found on the server".format(
                len(uids_on_server))
        )

        # new_uids = list(set(uids_on_server) - set(logged_uids))
        # print("new_uids", new_uids)

        for uid in uids_on_server:
            log.info('Getting message {0} :::::::::::::::::::::'.format(uid))

            result, data = server.uid(
                'fetch', str(uid), '(RFC822)')  # fetch entire message
            if data and data[0]:
                msg = email.message_from_string(data[0][1].decode())

                # parse the email here:
                mail = self._get_first_text_block(msg)

                # log.info(text)
                # parse_email.go(text.split("\n"))
                self.mails.append(mail)

                # record the uid in the db here
                # append_uids_to_log([uid])

        server.logout()

        return self.mails
