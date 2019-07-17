from collections import namedtuple


class Tags(list):
    """
    Tags are a list of Tag() instances.

    These tags are then used on every `add` and `save` request for the
    duration of the session.
    Each individual tag is instantiated as a Tag instance to handle validation
    to ensure they are in the correct format.
    To add new tags to a session do `session.tags.add(name='<name>',
                                                      value='<value>')`
    """
    def __init__(self, *args, **kwargs):

        # args = [Tag(tag) for tag in args]
        super(Tags, self).__init__(*args, **kwargs)

        self._mutate_iterable(self)
        #TODO: #3171 Prevalidate tags when adding

    def _make_tag(self, name, value):
        """
        Helper method for converting a name & value into a namedtupled and
        then to a dictionary to be added to `Tags`
        :param name: The value for the `name` key on a Tag
        :param value: The value for the `value` key on a Tag
        :return: An OrderedDict
        """
        return Tag(name=name, value=value)._asdict()

    def _mutate_iterable(self, iterable):
        for index, tag in enumerate(iterable):
            iterable[index] = self._make_tag(**tag)

    def add(self, name, value):
        """
        A helper method to make it easier for users to add tags.
        :param name: The name of the tag
        :param value: The value of the tag
        """
        super(Tags, self).append(self._make_tag(name=name, value=value))

    def append(self, object):
        super(Tags, self).append(self._make_tag(**object))

    def insert(self, index, p_object):
        super(Tags, self).insert(index, self._make_tag(**p_object))

    def extend(self, iterable):
        self._mutate_iterable(iterable)
        super(Tags, self).extend(iterable)

    def __add__(self, iterable):
        self._mutate_iterable(iterable)
        super(Tags, self).__add__(iterable)

    def __iadd__(self, iterable):
        self._mutate_iterable(iterable)
        super(Tags, self).__iadd__(iterable)


# An individual tag is just a namedtuple with a "name" and "value" key.
# These get converted to `OrderedDict` when being added to `Tags`
Tag = namedtuple('Tag', ['name', 'value'])
