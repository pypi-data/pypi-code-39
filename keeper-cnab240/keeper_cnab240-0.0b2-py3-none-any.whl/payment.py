import json


class Payment:
    PaymentsStatus = None

    def __init__(self, payments_status=None, **kwargs):
        self.attributes = dict(
            type=None,
            pay_date=None,
            effective_pay_date=None,
            favored_name=None,
            favored_document_number=None,
            favored_bank=None,
            agency=None,
            account=None,
            account_digit=None,
            our_number=None,
            currency_type='REA',
            your_number=None,
            ispb_code=None,
            goal_detail=None,
            payment_document_number=None,
            doc_goal=None,
            ted_goal=None,
            nf_document=None,
            identify_type=2,
            barcode=None,
            dv=None,
            due_rule=None,
            amount=None,
            free_field=None,
            due_date=None,
            title_amount=None,
            discounts=None,
            additions=None,
            payment_amount=None,
            effective_paid_amount=None,
            favored_message=None,
            occurrences=None,
            move_type=None,
            assembly=None,
            payer_document_type=None,
            payer_document_number=None,
            payer_name=None,
            recipient_document_type=None,
            recipient_document_number=None,
            recipient_name=None,
            payee_document_type=None,
            payee_document_number=None,
            payee_name=None,
        )

        kwargs_keys = kwargs.keys()
        for attr_name in self.attributes.keys():
            if attr_name in kwargs_keys:
                self.attributes[attr_name] = kwargs[attr_name]

        self.PaymentsStatus = payments_status

    def get_attribute(self, attr_name):
        if attr_name in self.attributes.keys():
            return self.attributes[attr_name]
        raise Exception('Payment does not have attribute called "' + attr_name + '"')

    def set_attribute(self, attr_name, attr_value):
        self.attributes[attr_name] = attr_value

    def get_attributes(self):
        return self.attributes

    def get_dict(self):
        return self.get_attributes()

    def get_json(self):
        return json.dumps(self.get_attributes())

    def status(self):
        occurrences = self.get_attribute('occurrences') if self.get_attribute('occurrences') not in (0, 00, '00')\
            else 'ZEROS'

        return occurrences if self.PaymentsStatus is None or not hasattr(self.PaymentsStatus, occurrences)\
            else self.PaymentsStatus(occurrences).get()


class StatusModel:
    is_error = None
    is_processed = None
    is_income = None
    is_info = None
    is_outcome = None
    is_reverted = None
    message = None

    def __init__(self, processed: bool, move: str, message: str = None):
        self.is_error = not processed
        self.is_processed = processed
        self.is_income = move == 'in' or move == 'revert'
        self.is_info = move == 'info'
        self.is_outcome = move == 'out'
        self.is_reverted = move == 'revert'
        self.error_type = message if self.is_error else None
        self.message = message

    def __str__(self):
        return '<StatusModel is_error={} is_processed={} is_income={} is_info={} is_outcome={} ' \
               'is_reverted={} error_type={} message={}>'.format(self.is_error,
                                                                 self.is_processed,
                                                                 self.is_income,
                                                                 self.is_info,
                                                                 self.is_outcome,
                                                                 self.is_reverted,
                                                                 self.error_type,
                                                                 self.message)
