"""

"""


class Life:
    PERMANENT = -1


class PubSub:
    def __init__(self):
        self._hub = hub = {}
        return

    def pub(self, topic, content, *, life=Life.PERMANENT):
        hub = self._hub
        if topic not in hub:
            hub[topic] = {"content_list": [], "life": life, "callbacks": []}

        if hub[topic]["life"] is None:
            hub[topic]["life"] = life
        hub[topic]["life"] == Life.PERMANENT
        hub[topic]["content"] = content

        if hub[topic]["life"] == Life.PERMANENT:
            hub[topic]["content_list"].append(content)

        for c in hub[topic]["callbacks"]:
            c(content)
        return True

    def sub(self, *, topic=None, callback=None):
        hub = self._hub

        if not (topic or callback):
            return list(hub.keys())

        if not (topic and isinstance(topic, str)):
            raise TypeError('"topic" must be a string')

        if callback is None:
            matches = []

            for t in hub:
                if t.startswith(topic):
                    matches.append(t)
            return matches

        else:
            if not callable(callback):
                raise ValueError('"callback" must be a callable')
            if topic not in hub:
                hub[topic] = {"callbacks": [], "life": None, "content_list": []}
            hub[topic]["callbacks"].append(callback)

            if hub[topic]["life"] in [Life.PERMANENT]:

                for c in hub[topic]["content_list"]:
                    callback(c)
        return True
