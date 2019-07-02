from django.dispatch import Signal

change_payment_status = Signal(providing_args=['payment_external_id',
                                               'status'])
