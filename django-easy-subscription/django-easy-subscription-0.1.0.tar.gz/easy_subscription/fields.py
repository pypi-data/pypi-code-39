import DNS
import logging
import smtplib
from django.forms import EmailField, ValidationError
from django.utils.translation import gettext_lazy as _


logger = logging.getLogger(__name__)

MX_DNS_CACHE = {}


class ValidatedEmailField(EmailField):
    @staticmethod
    def _get_mx_records(domain):
        # Get host MX records
        if domain not in MX_DNS_CACHE:
            try:
                MX_DNS_CACHE[domain] = DNS.mxlookup(domain)
                return MX_DNS_CACHE[domain]
            except DNS.ServerError:
                MX_DNS_CACHE[domain] = None
        return MX_DNS_CACHE[domain]

    def clean(self, value):
        value = super().clean(value)
        domain = value.split('@')[1]
        servers = self._get_mx_records(domain)

        if servers is None:
            raise ValidationError(_('Invalid email domain'))

        for server in servers:
            # Contact server to validate email
            try:
                smtp = smtplib.SMTP(timeout=5)
                smtp.set_debuglevel(0)
                smtp.connect(server[1])
                status, response = smtp.helo()
                if status != 250:
                    smtp.quit()
                else:
                    smtp.mail('')
                    code, response = smtp.rcpt(value)
                    smtp.quit()
                    if code == 250:
                        return value
                    elif code == 550:
                        raise ValidationError(_('Invalid email'))
            except Exception as e:
                logger.error(str(e))

        # if email couldn't be validated return email
        return value
