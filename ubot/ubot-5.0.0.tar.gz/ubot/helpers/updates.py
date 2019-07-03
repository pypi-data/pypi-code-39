update_types = [
    ('message', 'message'),
    ('edited_message', 'message'),
    ('channel_post', 'message'),
    ('edited_channel_post', 'message'),
    ('inline_query', 'inline_query'),
    ('chosen_inline_result', 'chosen_inline_result'),
    ('callback_query', 'callback_query'),
    ('shipping_query', 'shipping_query'),
    ('pre_checkout_query', 'pre_checkout_query')
]


def get_type_and_flavor(update):
    for _type, flavor in update_types:
        if _type in update:
            update['_type'] = _type
            update['_flavor'] = flavor
            return
    else:
        update['_type'] = None
        update['_flavor'] = None
