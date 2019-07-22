from .streamio import get_client, StreamObject
from datetime import date, datetime


class StreamModelMixin:

    def get_stream_object(self):
        return StreamObject(self)

    def track_action(self, verb, by = None, create_collection = True, force_update = False, time = None, date_field = None, extra_data = None):
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
            date_field = date_field,
            time = time,
            extra_data=extra_data
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

    def add_reaction(self, activity_kind, activity_id, data={}, by=None, target_feeds=None):
        stream = StreamObject(self)
        if by is None:
            by = str(getattr(self, self.feed_actor_field))
        if target_feeds is None:
            target_feeds = stream.get_to_feeds()

        return stream.client.reactions.add(
            activity_kind,
            activity_id,
            user_id=by,
            data=data,
            target_feeds=target_feeds
        )

    def get_reactions(self, activity_id, activity_kind = None):
        stream = StreamObject(self)
        data = {
            "activity_id": activity_id,
        }
        if activity_kind is not None:
            data['kind'] = activity_kind

        return stream.client.reactions.filter(**data)


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
