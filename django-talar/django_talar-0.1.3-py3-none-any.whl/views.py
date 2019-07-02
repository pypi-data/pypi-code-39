from django.views.decorators.csrf import csrf_exempt

from . import signals


@csrf_exempt
def change_payment_status(request, external_id):
    data = request.data
    try:
        status = data['status']
    except KeyError:
        raise Exception('No status provided in request body.')
    signals.change_payment_status.send(
        sender=None,
        payment_external_id=external_id, status=status
    )
