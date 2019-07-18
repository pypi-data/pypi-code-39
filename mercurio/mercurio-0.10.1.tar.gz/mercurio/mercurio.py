#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
import mimetypes

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


class mercurio:
    """Libreria che permette di creare mail e inviarle a destinatari multipli """

    def __init__(self, host, port=25, smtp_user=None, smtp_pwd=None):
        """Definizione delle credenziali di accesso all'host

        Args:
            host (str): Host a cui connettersi
            port (int, optional): Porta di accesso all'host. Defaults to 22.
            smtp_user (str, optional): Username richiesto per accedere all'host. Defaults to None.
            smtp_pwd (optional): Password richiesta per accedere all'host. Defaults to None.
        """
        self.host = host
        self.port = port
        self.smtp_user = smtp_user
        self.smtp_pwd = smtp_pwd

        logger.debug("Creating an instance of sendEmail")

    def send(
        self,
        fromaddress,
        recipients: list,
        reply_to_address: str,
        text,
        sbj,
        attachments=[],
        cid_attachments={},
    ) -> None:

        """Invia la mail ai destinatari indicati in input e chiude la connnessione all'host

        Args:
            fromaddress (str): Indirizzo E-mail del mittente
            recipients (list): Lista contenente gli indirizzi e-mail dei destinatari
            reply_to_address (str):
            text (str): Messaggio di testo della mail
            sbj (str): Soggetto della mail
            attachments (list, optional): Lista di file da allegare.
                Defaults to [].
            cid_attachments (dict, optional): Dizionario contenente i file da allegare
                in cui la chiave corrisponde al content_id.
                Defaults to {}.
        """

        if not isinstance(recipients, list):
            raise ValueError("Recipients must be an istance of list")

        connection = self.make_connection()

        logger.debug(fromaddress)

        for recipient in recipients:
            logger.debug("Sending to {}".format(recipient))
            message = self.make_message(
                fromaddress,
                recipient,
                reply_to_address,
                text,
                sbj,
                attachments,
                cid_attachments,
            )
            connection.sendmail(fromaddress, recipient, message.as_string())
            logger.debug("Sent")

        connection.quit()

    def attach_file_to_multipart_message(self, message, filename, content_id=None):
        """Inserisce file di testo o multimediale come allegato alla mail

        Args:
            message (str): Messagggio da inviare via mail
            filename (str): Nome del file in allegato
            content_id (str, optional): Stringa identificativa del file allegato. Defaults to None.
        """

        content_type, encoding = mimetypes.guess_type(filename)

        if content_type is None or encoding is not None:
            content_type = "application/octet-stream"

        main_type, sub_type = content_type.split("/", 1)

        logger.debug(
            "Attaching {filename}, as {main_type}, {sub_type}".format(
                filename=filename, main_type=main_type, sub_type=sub_type
            )
        )

        if main_type == "text":
            fp = open(filename, "rb")
            part = MIMEText(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == "image":
            fp = open(filename, "rb")
            part = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == "audio":
            fp = open(filename, "rb")
            part = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(filename, "rb")
            part = MIMEBase(main_type, _subtype=sub_type)
            part.set_payload(fp.read())
            encoders.encode_base64(part)
            fp.close()

        filename = os.path.basename(filename)

        part.add_header("Content-Disposition", "attachment", filename=filename)

        if content_id:
            part.add_header("Content-ID", "<%s>" % content_id)

        message.attach(part)

    def make_connection(self):
        """Connessione all'host tramite credenziali"""
        logger.debug("Opening connection")
        smtp_connection = smtplib.SMTP(host=self.host, port=self.port)
        if self.smtp_user:
            smtp_connection.starttls()
            smtp_connection.login(self.smtp_user, self.smtp_pwd)
        return smtp_connection

    def make_message(
        self,
        fromaddress,
        recipient,
        reply_to_address,
        text,
        sbj,
        attachments=[],
        cid_attachments={},
    ):
        """Crea mail da inviare definendone mittente, destinatari, soggetto, testo e file da allegare

        Args:
            fromaddress (str): Indirizzo e-mail del mittente
            recipient (str): Lista contenente gli indirizzi e-mail dei destinatari
            reply_to_address (str):
            text (str): Messaggio di testo della mail
            sbj (str): Soggetto della mail
            attachments (list, optional): Lista di file da allegare. Defaults to [].
            cid_attachments (dict, optional): Dizionario contenente i file da allegare in cui la chiave corrisponde al content_id. Defaults to {}.

        Raises:
            ValueError: Restituisce errore se attachment non è una lista
            ValueError: Restituisce errore se cid_attachment non è un dizionario
        """

        if not isinstance(attachments, list):
            raise ValueError("attachments must be an istance of list")

        if not isinstance(cid_attachments, dict):
            raise ValueError("cid_attachments must be an istance of dict")

        logger.debug("Preparing message")

        msg = MIMEMultipart()
        msg["Subject"] = sbj
        msg["From"] = fromaddress
        msg["To"] = recipient
        msg.add_header("reply-to", reply_to_address)

        testo = MIMEText(text, "html", "utf-8")
        msg.attach(testo)

        for attachment in attachments:
            self.attach_file_to_multipart_message(msg, attachment)

        for code in cid_attachments:
            self.attach_file_to_multipart_message(msg, cid_attachments[code], code)

        return msg
