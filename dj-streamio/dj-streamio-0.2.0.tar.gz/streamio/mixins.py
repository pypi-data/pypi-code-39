from .streamio import get_client, StreamObject
from datetime import date, datetime


class StreamViewSetMixin:
    """
    A mixin for using with DRF viewsets.
    Provides a GET /:resource/:id/stream/ endpoint

    """
    from rest_framework.decorators import action

    @action(detail=True, methods=['GET'])
    def stream(self, request, pk=None):
        from rest_framework.response import Response
        options_fields = ['limit', 'offset', 'id_gt', 'id_gte', 'id_lt', 'id_lte', 'offset', 'ranking', 'enrich']
        extra_args = {}
        for field in options_fields:
            value = request.GET.get(field, None)
            if value is not None:
                extra_args[field] = value
                if field == 'enrich':
                    true_values = ['true', 'True', 't', '1', 1]
                    if value in true_values:
                        extra_args[field] = True
                    else:
                        extra_args[field] = False

        stream = self.get_object().get_feed(**extra_args)
        return Response(stream)

class StreamModelMixin:

    def track_action(self, verb, by = None, create_collection = True, force_update = False, date_field = None):
        """
        # minimal:
        todo.track_action('finish')
        """
        stream = StreamObject(self)
        enriched = None
        if create_collection:
            enriched = stream.enrich(force_update = force_update)

        if by is None:
            by = getattr(self, self.feed_actor_field)

        is_onceoff_action = verb in self.feed_once_off_actions

        custom_message = None
        if getattr(self, 'formatted_feed_message', None) is not None:
            custom_message = self.formatted_feed_message(verb=verb)

        activity = stream.perform_action(
            by,
            verb,
            is_onceoff_action=is_onceoff_action,
            custom_message=custom_message,
            date_field = date_field
        )
        return {
            "object": enriched,
            "activity": activity
        }

    def add_notification(self, verb, message, users_to_notify = None, forward = {}, *args, **kwargs):
        if users_to_notify is None:
            actor_id = getattr(self, self.feed_actor_field, None)
            if actor_id is not None:
                users_to_notify = [actor_id]

        stream = StreamObject(self)
        return stream.add_notification(
            users_to_notify = users_to_notify,
            verb = verb,
            message = message,
            forward = forward
        )

    def get_feed(self, **kwargs):
        options = {
            "enrich": True
        }
        options.update(kwargs)
        client = get_client()
        return client.feed(
            self.feed_name,
            self.pk
        ).get(**options)
