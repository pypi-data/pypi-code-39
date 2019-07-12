import json, logging, markdown, matrix_client, re, time
import matrix_client.client as mc
from matrix_client.room import Room
from matrix_client.user import User
from .cache import Cache

logger = logging.getLogger(__name__)


class MatrixBot:
    """
    Handles barebones details of connecting, joining rooms, responding to invites and
    setting up listeners. Users should override the process_message() method to make
    the bot respond to events.

    By default, the bot will automatically join all rooms it's invited to. If you wish
    to disable this feature, add something like the following to your subclass:

        def handle_invite(self, room_id, state):
            pass

    To cache data returned by APIs, wrap your calling function with self.cache.fetch():

        data = self.cache.fetch(
            "cache_key",
            lambda: my_api_call(arg1, arg2),
            timeout=expiry_seconds
        )
    """

    def __init__(
        self,
        host="matrix.org",
        display_name="MatrixBot",
        token=None,
        user_id=None,
        cache_db=None,
    ):
        """
        parameters:     host (str) - matrix homeserver's hostname
                        display_name (str) - bot account's display name
                        token (optional: str) - user access token
                        user_id (optional: str) - ex: "@username:example.com"
                        cache_db (optional: str) - path to sqlite db for cache
        """
        self.host = host
        self.display_name = display_name
        self.token = token
        self.user_id = user_id
        self.client = mc.MatrixClient(f"https://{host}", user_id=user_id, token=token)
        self.user = None
        if self.token is not None and self.user_id is not None:
            self.user = self.client.get_user(self.user_id)
            self.user.set_display_name(self.display_name)
            self.init_rooms(self.client.rooms)
            self.invite_listener = self.client.add_invite_listener(self.handle_invite)
        self.cache = Cache(dbfile=cache_db)

    def login(self, username, password):
        """
        Login with username/password if no token supplied

        parameters:     username (str)
                        password (str)
        returns:        True if login is successful, False otherwise
        return type:    bool
        """
        try:
            logger.debug("Logging in to {}".format(self.host))
            self.token = self.client.login(username, password, sync=True)
            self.user = self.client.get_user("@{}:{}".format(username, self.host))
            logger.debug("Setting display name to '{}'".format(self.display_name))
            self.init_rooms(self.client.rooms)
            self.invite_listener = self.client.add_invite_listener(self.handle_invite)
            return True
        except mc.MatrixRequestError as e:
            logger.error("Login failed: {}".format(e))
            return False

    def start(self):
        """
        Starts listening and loops until it should stop
        """
        self.start_listening()
        while self.client.should_listen:
            pass

    def start_listening(self):
        """
        Starts a background listener
        """
        logger.debug("Starting background listener")

        self.client.start_listener_thread()

    def stop_listening(self):
        """
        Stops the background listener
        """
        logger.debug("Stopping background listener")
        self.client.stop_listener_thread()

    def init_rooms(self, rooms):
        """
        Starts a message listener in each room. Accepts a single Room,
        a list of Room objects, or a dict such as returned by self.client.get_rooms()

        parameters:     rooms (Room, list or dict)
        """
        if isinstance(rooms, Room):
            room_list = [rooms]
        elif isinstance(rooms, list):
            room_list = rooms
        elif isinstance(rooms, dict):
            room_list = [r for r in rooms.values()]
        else:
            raise TypeError("Room list must be of type Room, list, or dict!")
        for room in room_list:
            logger.debug("Adding listener to room {}".format(room.room_id))
            room.add_listener(self.handle_event)

    def handle_invite(self, room_id, state):
        """
        Callback for self.client.add_invite_listener(). Override if you do not wish to
        automatically accept invites.
        """
        logger.info(f"Received invite to {room_id} from {state['events'][0]['sender']}")
        self.accept_invite(room_id)

    def accept_invite(self, room_id):
        """
        Auto-joins rooms when invited

        parameters:     room_id (str)
        """
        self.join_room(room_id)

    def join_room(self, room_id):
        """
        Joins a room, initializes it

        parameters:     room_id (str)
        """
        logger.info(f"Joining room: {room_id}")
        room = self.client.join_room(room_id)
        self.init_rooms(room)

    def room_is_empty(self, room):
        """
        Returns True if the bot is the only user in a room called "Empty room". Useful
        for when the bot is invited to a 1-on-1 room which is then abandoned

        parameters:     room (Room)
        """
        return room.display_name == "Empty room" and len(room.get_joined_members()) == 1

    def leave_if_empty(self, room):
        """
        Returns True and leaves the room if it's empty
        """
        if self.room_is_empty(room):
            logger.info(f"Leaving empty room {room.room_id} ({room.display_name})")
            room.leave()
            return True
        return False

    def handle_event(self, room, event):
        """
        Processes incoming room events

        parameters:     room (Room) - the room the event is linked to
                        event (dict) - the event returned by the listener
        """
        # don't talk to yourself
        if event["sender"] == self.user.user_id:
            return
        # sanity check to avoid possible spoofing
        if room.room_id == event["room_id"]:
            logger.debug(f"Incoming event data: {event['content']}")
            self.process_event(room, event)
        else:
            logger.warn(
                f"Event received from room {room.room_id} does not have a matching "
                + f"room_id: '{json.dumps(event)}'. Ignoring."
            )

    def process_event(self, room, event):
        """
        User-defined method to react to events

        parameters:     room (Room) - the room the event is linked to
                        event (dict) - the event returned by the listener
        """
        raise NotImplementedError(
            "You must define a process_event method in your subclass"
        )

    def mention(self, user):
        """
        Create a markdown-formatted user mention string

        parameters:     user (User or user_id (str))

        returns:        a user mention
        return type:    str
        """
        if isinstance(user, User):
            user_id = user.user_id
            display_name = user.get_display_name()
        elif isinstance(user, str):
            user_id = user
            display_name = self.client.get_user(user_id).get_display_name()
        else:
            raise TypeError("'user' parameter must be a User object or a user_id (str)")
        return f"[{display_name}](https://matrix.to/#/{user_id})"

    def say(self, room, message, mention=None):
        """
        Sends a message to a room

        parameters:     room (Room)
                        message (str) - plain, markdown or html
                        mention (user_id (str)) - prefix the message with a mention
        """
        if mention is not None:
            text = f"{self.mention(mention)} {message}"
        else:
            text = message
        html = markdown.markdown(text)
        room.send_html(html)

    def fetch(self, key, callback, timeout=300):
        """
        Shortcut for self.cache.fetch()
        """
        self.cache.fetch(key, callback, timeout=timeout)
