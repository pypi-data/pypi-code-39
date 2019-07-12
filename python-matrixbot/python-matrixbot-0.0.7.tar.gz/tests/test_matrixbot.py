#!/usr/bin/env python

import os, unittest
from unittest import mock
from matrix_client.client import MatrixClient
from matrix_client.user import User
from matrix_client.room import Room
from matrixbot.matrixbot import Cache, MatrixBot


class TestMatrixBot(unittest.TestCase):
    @mock.patch.object(MatrixClient, "_sync")
    @mock.patch.object(MatrixClient, "get_user")
    def test___init__(self, mock_get_user, mock_sync):
        cache_file = "/dev/shm/matrixbot_matrixbot_test.sqlite3"
        # test with defaults
        default = MatrixBot()
        self.assertEqual(default.host, "matrix.org")
        self.assertEqual(default.display_name, "MatrixBot")
        self.assertIsNone(default.token)
        self.assertIsNone(default.user_id)
        self.assertIsInstance(default.client, MatrixClient)
        self.assertIsNone(default.user)
        self.assertIsInstance(default.cache, Cache)
        # test with custom options
        custom = MatrixBot(
            host="example.com",
            display_name="ExampleBot",
            token="12345",
            user_id="@user:example.com",
            cache_db=cache_file,
        )
        self.assertEqual(custom.host, "example.com")
        self.assertEqual(custom.display_name, "ExampleBot")
        self.assertEqual(custom.token, "12345")
        self.assertEqual(custom.user_id, "@user:example.com")
        mock_get_user.assert_called_with("@user:example.com")
        self.assertIsInstance(custom.cache, Cache)
        # clean up
        os.remove(cache_file)

    @mock.patch.object(MatrixClient, "login")
    def test_login(self, mock_login):
        bot = MatrixBot()
        mock_login.return_value = "12345"
        self.assertTrue(bot.login("test", "password123"))
        mock_login.assert_called_with("test", "password123", sync=True)
        self.assertEqual(bot.token, "12345")
        self.assertIsInstance(bot.user, User)

    @mock.patch.object(MatrixBot, "start_listening")
    def test_start(self, mock_start_listening):
        bot = MatrixBot()
        bot.start()
        mock_start_listening.assert_called_with()

    @mock.patch.object(MatrixClient, "start_listener_thread")
    def test_start_listening(self, mock_start_listener_thread):
        bot = MatrixBot()
        bot.start_listening()
        mock_start_listener_thread.assert_called_with()

    @mock.patch.object(MatrixClient, "stop_listener_thread")
    def test_stop_listening(self, mock_stop_listener_thread):
        bot = MatrixBot()
        bot.stop_listening()
        mock_stop_listener_thread.assert_called_with()

    @mock.patch.object(Room, "add_listener")
    def test_init_rooms(self, mock_add_listener):
        # passing a single Room
        room_bot = MatrixBot()
        room_bot.init_rooms(Room(room_bot.client, "!foo:example.com"))
        mock_add_listener.assert_called_with(room_bot.handle_event)
        # passing a list of Rooms
        list_bot = MatrixBot()
        list_bot.init_rooms([Room(list_bot.client, "!foo:example.com")])
        mock_add_listener.assert_called_with(list_bot.handle_event)
        # passing a dict of Rooms
        dict_bot = MatrixBot()
        dict_bot.init_rooms(
            {"!foo:example.com": Room(dict_bot.client, "!foo:example.com")}
        )
        mock_add_listener.assert_called_with(dict_bot.handle_event)
        # passing an invalid type
        err_bot = MatrixBot()
        with self.assertRaises(TypeError):
            err_bot.init_rooms("strings don't work")

    @mock.patch.object(MatrixBot, "accept_invite")
    def test_handle_invite(self, mock_accept_invite):
        bot = MatrixBot()
        state = {"events": [{"sender": "derp"}]}
        bot.handle_invite("!foo:example.com", state)
        mock_accept_invite.assert_called_with("!foo:example.com")

    @mock.patch.object(MatrixBot, "join_room")
    def test_accept_invite(self, mock_accept_invite):
        bot = MatrixBot()
        bot.accept_invite("!foo:example.com")
        mock_accept_invite.assert_called_with("!foo:example.com")

    @mock.patch.object(MatrixBot, "init_rooms")
    @mock.patch.object(MatrixClient, "join_room")
    def test_join_room(self, mock_join_room, mock_init_rooms):
        bot = MatrixBot()
        bot.join_room("!foo:example.com")
        mock_join_room.assert_called_with("!foo:example.com")
        mock_init_rooms.assert_called()

    @mock.patch("matrix_client.room.Room")
    def test_room_is_empty(self, mock_room):
        bot = MatrixBot()
        room = mock_room()
        self.assertFalse(bot.room_is_empty(room))
        # set the display name to "Empty room" but the membership to > 1
        room.display_name = "Empty room"
        room.get_joined_members.return_value = [1, 2]
        self.assertFalse(bot.room_is_empty(room))
        # now set the membership == 1
        room.get_joined_members.return_value = [1]
        self.assertTrue(bot.room_is_empty(room))

    @mock.patch("matrix_client.room.Room")
    @mock.patch.object(MatrixBot, "room_is_empty")
    def test_leave_if_empty(self, mock_room_is_empty, mock_room):
        bot = MatrixBot()
        room = mock_room()
        mock_room_is_empty.return_value = False
        self.assertFalse(bot.leave_if_empty(room))
        mock_room_is_empty.return_value = True
        self.assertTrue(bot.leave_if_empty(room))
        room.leave.assert_called()

    @mock.patch.object(MatrixBot, "process_event")
    @mock.patch.object(MatrixClient, "_sync")
    @mock.patch.object(MatrixClient, "get_user")
    def test_handle_event(self, mock_get_user, mock_sync, mock_process_event):
        bot = MatrixBot(user_id="@user:example.com", token="12345")
        room = Room(bot.client, "!foo:example.com")
        event = {
            "sender": "@otheruser:example.com",
            "room_id": "!foo:example.com",
            "content": "foo",
        }
        # if the event user is the client user, we should see this return None and
        # should not see if call `process event`
        bot.user.user_id = "@user:example.com"
        self.assertIsNone(bot.handle_event(room, {"sender": "@user:example.com"}))
        mock_process_event.assert_not_called()
        # otherwise, we should see `process_event` called
        self.assertIsNone(bot.handle_event(room, event))
        mock_process_event.assert_called_with(room, event)

    def test_process_event(self):
        bot = MatrixBot()
        room = Room(bot.client, "!foo:example.com")
        with self.assertRaises(NotImplementedError):
            bot.process_event(room, {})

    @mock.patch.object(User, "get_display_name")
    @mock.patch.object(User, "__init__")
    def test_mention(self, mock_user_init, mock_get_display_name):
        mock_user_init.return_value = None
        mock_get_display_name.return_value = "Neo"
        bot = MatrixBot()
        user = User()
        user_id = "@user:example.com"
        mention = "[Neo](https://matrix.to/#/@user:example.com)"
        user.user_id = user_id
        # with a User
        self.assertEqual(bot.mention(user), mention)
        # with a string
        self.assertEqual(bot.mention(user_id), mention)
        # with something inappropriate
        with self.assertRaises(TypeError):
            bot.mention([])

    @mock.patch.object(MatrixBot, "mention")
    @mock.patch("matrix_client.room.Room")
    def test_say(self, mock_room, mock_mention):
        bot = MatrixBot()
        room = mock_room()
        # say with plaintext
        mock_mention.return_value = "@user:example.com"
        bot.say(room, "foo")
        room.send_html.assert_called_with("<p>foo</p>")
        # plaintext with a mention
        bot.say(room, "foo", mention="@user:example.com")
        room.send_html.assert_called_with("<p>@user:example.com foo</p>")
        # markdown
        bot.say(room, "# foo")
        room.send_html.assert_called_with("<h1>foo</h1>")

    @mock.patch.object(Cache, "fetch")
    def test_fetch(self, mock_fetch):
        bot = MatrixBot()
        callback = lambda: None
        bot.fetch("key", callback)
        mock_fetch.assert_called_with("key", callback, timeout=300)
