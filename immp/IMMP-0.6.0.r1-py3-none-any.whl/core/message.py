from copy import copy
from datetime import datetime, timezone
from enum import Enum
import re

import aiohttp

from .util import _no_escape, escape, pretty_str, unescape


@pretty_str
class User:
    """
    Generic class to represent senders of messages.

    Attributes:
        id (str):
            Plug-specific user identifier.
        plug (.Plug):
            Source plug instance, representing the domain this user comes from.
        username (str):
            User's chosen or allocated display name.
        real_name (str):
            User's preferred and/or family name.
        avatar (str):
            URL of the user's profile picture.
        link (str):
            Public profile URL, or identifier used for invites.
        suggested (bool):
            ``True`` if the display of this user is not important.  Useful for bot messages where
            displaying the author is superfluous -- plugs may choose to show the user only if
            required by the network to show something.
        raw:
            Optional plug-specific underlying user object.
    """

    def __init__(self, *, id=None, plug=None, username=None, real_name=None, avatar=None,
                 link=None, suggested=False, raw=None):
        self.id = str(id) if id else None
        self.plug = plug
        self.username = username
        self.real_name = real_name
        self.avatar = avatar
        if not isinstance(getattr(self.__class__, "link", None), property):
            # Subclasses may implement as a property, in which case the attribute set would fail.
            self.link = link
        self.suggested = suggested
        self.raw = raw

    async def is_system(self):
        """
        Equivalent to :meth:`.Plug.user_is_system`.

        Returns:
            bool:
                ``True`` if the user relates to the plug itself.
        """
        return await self.plug.user_is_system(self)

    async def private_channel(self):
        """
        Equivalent to :meth:`.Plug.channel_for_user`.

        Returns:
            .Channel:
                Private channel for this user.
        """
        return await self.plug.channel_for_user(self)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.plug and not (other.plug and self.plug.name == other.plug.name):
            return False
        if self.id:
            return self.id == other.id
        else:
            return ((self.id, self.username, self.real_name, self.link) ==
                    (other.id, other.username, other.real_name, other.link))

    def __hash__(self):
        if self.id:
            return hash(self.id)
        else:
            return hash((self.username, self.real_name, self.link))

    def __repr__(self):
        return "<{}: {} {}>".format(self.__class__.__name__, repr(self.id),
                                    repr(self.real_name or self.username))


class Segment:
    """
    Substring of message text with consistent formatting.

    Calling :meth:`str` on an instance will return the segment text.  Similarly, the length of a
    segment is just the length of the contained text.

    Attributes:
        text (str):
            Plain segment text.
        bold (bool):
            Whether this segment should be formatted bold.
        italic (bool):
            Whether this segment should be emphasised.
        underline (bool):
            Whether this segment should be underlined.
        strike (bool):
            Whether this segment should be struck through.
        code (bool):
            Whether this segment should be monospaced.
        pre (bool):
            Whether this segment should be preformatted.
        link (str):
            Anchor URL if this segment represents a clickable link.
        mention (.User):
            Target user mentioned in this segment.
    """

    _bool_tags = ("bold", "italic", "underline", "strike", "code", "pre")

    def __init__(self, text, *, bold=False, italic=False, underline=False, strike=False,
                 code=False, pre=False, link=None, mention=None):
        self.text = text
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.strike = strike
        self.code = code
        self.pre = pre
        self.link = link
        self.mention = mention

    def __len__(self):
        return len(self.text)

    @property
    def _tuple(self):
        return (self.text, self.bold, self.italic, self.underline, self.strike, self.code,
                self.pre, self.link, self.mention)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self._tuple == other._tuple

    def __hash__(self):
        return hash(self._tuple)

    def __str__(self):
        return self.text

    def __repr__(self):
        attrs = [" {}".format(attr) for attr in ("bold", "italic", "underline", "strike", "code",
                                                 "pre", "link", "mention") if getattr(self, attr)]
        return "<{}: {}{}>".format(self.__class__.__name__, repr(self.text), "".join(attrs))


class RichText:
    """
    Common standard for formatted message text, akin to Hangouts' message segments.  This is a
    container designed to hold instances of :class:`.Segment`.

    Calling :meth:`str` on an instance will return the entire text without formatting.

    Instances may be indexed or sliced, which will apply to the segments.  The :attr:`slice.step`
    argument is overloaded to be boolean; if ``True``, slicing will apply to characters of the text
    content rather than the segments.  Length is always based on the content.

    Attributes:
        size (int):
            Number of segments in the text.
    """

    _tag_regex = re.compile(r"{}(.*?){}".format(_no_escape("<"), _no_escape(">")))
    _split_regex = re.compile(_no_escape(","))

    def __init__(self, segments=None):
        self._segments = (list(segments) if segments else None) or []

    @property
    def size(self):
        return len(self._segments)

    def normalise(self):
        """
        Make a copy of this message with formatting applied from text boundaries.

        For example::

            Some[b] bold [/b]text.

        The bold boundaries would be moved to surround "bold" excluding the spaces.

        Returns:
            .RichText:
                Normalised message text instance.
        """
        normalised = []
        for segment in self._segments:
            clone = copy(segment)
            match = re.match(r"(\s*)(.*?)(\s*)$", clone.text, re.DOTALL)
            before, clone.text, after = match.groups()
            if before:
                normalised.append(Segment(before))
            if clone.text:
                normalised.append(clone)
            if after:
                normalised.append(Segment(after))
        return RichText(normalised)

    def clone(self):
        """
        Make a copy of this message text and all its segments.

        Returns:
            .RichText:
                Cloned message text instance.
        """
        return RichText([copy(segment) for segment in self._segments])

    def prepend(self, *segments):
        """
        Insert one or more segments at the beginning of the text.

        Args:
            segments (.Segment list):
                New segments to lead the message text.
        """
        self._segments = list(segments) + self._segments

    def append(self, *segments):
        """
        Insert one or more segments at the end of the text.

        Args:
            segments (.Segment list):
                New segments to tail the message text.
        """
        self._segments += segments

    def indent(self, chars="  "):
        """
        Prefix each line of text with another string.

        Args:
            chars (str):
                Prefix characters to prepend to each line.

        Returns:
            .RichText:
                Indented message text instance.
        """
        clone = RichText()
        if not self:
            return clone
        clone.append(Segment(chars))
        for segment in self:
            for i, line in enumerate(segment.text.split("\n")):
                if i > 0:
                    clone.append(Segment("\n{}".format(chars)))
                if line:
                    new = copy(segment)
                    new.text = line
                    clone.append(new)
        return clone

    def offset(self, pos):
        """
        Find the position within a segment corresponding to a point along the whole text.

        Args:
            pos (int):
                Position within the represented text.

        Returns:
            (int, int) tuple:
                Segment and offset within it.
        """
        if pos < 0 or pos > len(self):
            raise IndexError("Position {} out of bounds".format(pos))
        total = 0
        for i, segment in enumerate(self):
            total += len(segment)
            if total > pos:
                return i, len(segment) - (total - pos)
        else:
            return i + 1, 0

    def trim(self, length):
        """
        Reduce a long message text to a snippet with an ellipsis.

        Args:
            length (int):
                Maximum length of the message text.

        Returns:
            .RichText:
                Trimmed message text instance.
        """
        if len(self) <= length:
            return self
        clone = self[:length:True]
        clone[-1].text = clone[-1].text[:-2]
        clone.append(Segment("..."))
        return clone

    @classmethod
    def unraw(cls, text, host=None):
        """
        Inverse of :meth:`raw`, parse a string with formatting syntax into a rich instance.

        Args:
            text (str):
                Plain text with formatting syntax.
            host (.Host):
                Optional host instance, needed to resolve mention tags.

        Returns:
            .RichText:
                Parsed message text instance.
        """
        rich = cls()
        current = {}
        while True:
            match = cls._tag_regex.search(text)
            if not match:
                break
            start = match.start()
            end = match.end()
            last, text = text[:start], text[end:]
            if last or rich:
                rich.append(Segment(unescape(last, "<"), **current))
            current = {}
            tags = cls._split_regex.split(match.group(1))
            for tag in tags:
                # Bare link tags will use the segment text as the link, filled in at the end.
                for target in Segment._bool_tags + ("link",):
                    if tag in (target, target[0]):
                        current[target] = True
                        break
                else:
                    if tag.startswith(("link=", "l=")):
                        current["link"] = unescape(tag.split("=", 1)[1], ",", ">")
                    elif tag.startswith(("mention=", "m=")) and host:
                        parts = re.split(_no_escape("/"), tag.split("=", 1)[1], 2)
                        plug = unescape(parts[0], "/", ",", ">")
                        user = unescape(parts[1], "/", ",", ">")
                        name = unescape(parts[2], ",", ">")
                        current["mention"] = User(id=user, plug=host.plugs[plug],
                                                  real_name=name)
        if text:
            rich.append(Segment(unescape(text, "<"), **current))
        for segment in rich:
            if segment.link is True:
                segment.link = segment.text
        return rich

    def raw(self):
        """
        Serialise formatted text into a string representation, suitable for storage or transmission
        as plain text.

        Returns:
            str:
                Plain text with formatting syntax.
        """
        raw = ""
        last = "/"
        for segment in self:
            tags = []
            for tag in Segment._bool_tags:
                if getattr(segment, tag):
                    tags.append(tag[0])
            if segment.link:
                if segment.text == segment.link:
                    tags.append("l")
                else:
                    tags.append("l={}".format(escape(segment.link, ",", ">")))
            if segment.mention:
                tags.append("m={}/{}/{}"
                            .format(escape(segment.mention.plug.name, "/", ",", ">"),
                                    escape(segment.mention.id, "/", ",", ">"),
                                    escape(segment.mention.real_name or segment.mention.username,
                                           ",", ">")))
            current = ",".join(tags) or "/"
            if current != last:
                raw += "<{}>".format(current)
            last = current
            raw += escape(segment.text, "<")
        if last != "/":
            raw += "</>"
        return raw

    def __iter__(self):
        return iter(self._segments)

    def __len__(self):
        return sum(len(segment) for segment in self._segments)

    def __getitem__(self, key):
        if isinstance(key, slice):
            if key.step is not None and not isinstance(key.step, bool):
                raise TypeError("RichText slice step must be boolean")
            elif not key.step:
                return RichText(self._segments[key.start:key.stop])
            start, end = key.start, key.stop
            if start is None and end is None:
                return self.clone()
            elif start is None:
                start = 0
            elif end is None:
                end = len(self)
            start_segment, start_offset = self.offset(start % len(self))
            end_segment, end_offset = self.offset(((end - 1) % len(self)) + 1)
            stop_segment = end_segment + 1 if end_offset else end_segment
            stop_offset = end_offset - start_offset if start_segment == end_segment else end_offset
            clone = RichText()
            for segment in self[start_segment:stop_segment]:
                clone.append(copy(segment))
            if start_offset:
                clone[0].text = clone[0].text[start_offset:]
            if end_offset:
                clone[-1].text = clone[-1].text[:stop_offset]
            return clone
        elif isinstance(key, int):
            return self._segments[key]
        else:
            raise TypeError("RichText indices must be integers or slices")

    def __add__(self, other):
        return RichText(self._segments + list(other))

    def __iadd__(self, other):
        self._segments += other
        return self

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and len(self) == len(other) and
                all(x == y for x, y in zip(self, other)))

    def __hash__(self):
        return hash(tuple(self._segments))

    def __str__(self):
        # Fallback implementation: just return the message text without formatting.
        return "".join(str(segment) for segment in self._segments)

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, repr(self._segments))


@pretty_str
class File:
    """
    Base file attachment object.

    Attributes:
        title (str):
            Name of file, if the plug supports names.
        type (.Type):
            Basic type of the file.
        source (str):
            Public URL to the original file location, if one is available.
    """

    class Type(Enum):
        """
        Possible file attachment types.

        Attributes:
            unknown:
                Default file type if not otherwise specified.
            image:
                Picture in a standard recognised format (e.g. PNG, JPEG).
        """
        unknown = 0
        image = 1

    def __init__(self, title=None, type=Type.unknown, source=None):
        self.title = title
        self.type = type
        self.source = source

    async def get_content(self, sess=None):
        """
        Stream the contents of the file, suitable for writing to a file or uploading elsewhere.

        The default implementation will try to fetch a file by the source field.  It may be
        overridden to add authentication or other metadata, but the method must remain callable
        with only a session passed to it.

        Args:
            sess (aiohttp.ClientSession):
                Existing HTTP session with which to make any requests.

        Returns:
            io.IOBase:
                Readable stream of the raw file.
        """
        sess = sess or aiohttp.ClientSession()
        return await sess.get(self.source)

    def __str__(self):
        if self.title and self.source:
            return "{} ({})".format(self.title, self.source)
        else:
            return self.title or self.source

    def __repr__(self):
        return "<{}: {} {}>".format(self.__class__.__name__, repr(self.title), self.type.name)


@pretty_str
class Location:
    """
    Attributes:
        latitude (float):
            North-South coordinate of the location in degrees.
        longitude (float):
            East-West coordinate of the location in degrees.
        coordintes (float):
            Read-only ``(latitude, longitude)`` pair.
        name (str):
            Name of the place represented by this location.
        address (str):
            Full street address of this place.
        google_map_url (str):
            URL to Google Maps centred on this place.
    """

    def __init__(self, latitude=None, longitude=None, name=None, address=None):
        self.latitude = latitude
        self.longitude = longitude
        self.name = name
        self.address = address

    @property
    def coordinates(self):
        return (self.latitude, self.longitude)

    @property
    def google_map_url(self):
        return "https://www.google.com/maps/place/{},{}".format(self.latitude, self.longitude)

    def google_image_url(self, width, height=None):
        """
        Generate a static map image URL centred on this place.

        Args:
            width (int):
                Width of the image.
            height (int):
                Height of the image, matches the width (for a square image) if not specified.

        Returns:
            str:
                Corresponding image URL from the Google Maps API.
        """
        return ("https://maps.googleapis.com/maps/api/staticmap?center={0},{1}&"
                "markers=color:red%7C{0},{1}&size={2}x{3}"
                .format(self.latitude, self.longitude, width, height or width))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.coordinates == other.coordinates

    def __hash__(self):
        return hash(self.coordinates)

    def __str__(self):
        out = self.address or "{}, {}".format(*self.coordinates)
        if self.name:
            out = "{} ({})".format(self.name, out)
        return out

    def __repr__(self):
        return "<{}: {}, {}{}>".format(self.__class__.__name__, self.latitude, self.longitude,
                                       " {}".format(repr(self.name)) if self.name else "")


@pretty_str
class Message:
    """
    Base message content container, understood by all plugs.

    Attributes:
        text (.RichText):
            Representation of the message text content.
        user (.User):
            User profile that sent the message.
        action (bool):
            Whether this message should be presented as an action involving its user.
        reply_to (.Message):
            Parent message, which this message replies to.
        joined (.User list):
            Collection of users that just joined the channel.
        left (.User list):
            Collection of users that just parted the channel.
        title (str):
            New channel title, if this message represents a rename.
        attachments (.Attachment list):
            Additional data included in the message.
        raw:
            Optional plug-specific underlying message or event object.
    """

    def __init__(self, *, text=None, user=None, action=False, reply_to=None, joined=None,
                 left=None, title=None, attachments=None, raw=None):
        self.text = text
        self.user = user
        self.action = action
        self.reply_to = reply_to
        self.joined = joined or []
        self.left = left or []
        self.title = title
        self.attachments = attachments or []
        self.raw = raw

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if value is None or isinstance(value, RichText):
            self._text = value
        elif isinstance(value, str):
            self._text = RichText([Segment(value)])
        else:
            raise ValueError("Message text must be RichText or plain str")

    def render(self, *, real_name=True, link_name=True, edit=False, delimiter="\n",
               quote_reply=False, strip_links=False, trim=None):
        """
        Add the sender's name (if present) to the start of the message text, suitable for sending
        as-is on plugs that need all the textual message content in the body.

        Args:
            real_name (bool):
                ``True`` (default) to display real names, or ``False`` to prefer usernames.  If
                only one kind of name is available, it will be used regardless of this setting.
            link_name (bool):
                ``True`` (default) to link the author's name to their profile, if a link exists.
            edit (bool):
                Whether this render should show an ``[edit]`` tag next to the author.
            delimiter (str):
                Characters added between the sender's name and the message text (a new line by
                default).
            quote_reply (bool):
                ``True`` to quote the parent message before the current one, prefixed with a
                box-drawing vertical line (not quoted by default).
            strip_links (bool):
                ``True`` to skip over links in the message text (links left intact by default).
            trim (int):
                Show an ellipsed snippet if the text exceeds this length, or ``None`` (default) for
                no trimming.

        Returns:
            .RichText:
                Rendered message body.
        """
        output = RichText()
        name = link = None
        action = self.action
        if self.user and not self.user.suggested:
            if real_name:
                name = self.user.real_name or self.user.username
            else:
                name = self.user.username or self.user.real_name
            if link_name:
                link = self.user.link
        if self.text:
            if isinstance(self.text, RichText):
                text = self.text
                if strip_links:
                    text = text.clone()
                    for segment in text:
                        segment.link = None
            else:
                text = RichText([Segment(self.text)])
            if trim:
                text = text.trim(trim)
            output.append(*text)
        elif self.attachments:
            action = True
            count = len(self.attachments)
            what = "{} files".format(count) if count > 1 else "this file"
            output.append(Segment("sent {}".format(what)))
        if name:
            if action:
                output.prepend(Segment(" "))
            else:
                output.prepend(Segment(delimiter))
                output.prepend(Segment(":", bold=True))
            if edit:
                output.prepend(Segment(" [edit]"))
            output.prepend(Segment(name, bold=True, link=link))
        elif edit:
            output.prepend(Segment("[edit] "))
        if action:
            for segment in output:
                segment.italic = True
        if quote_reply and self.reply_to:
            if isinstance(self.reply_to, Message):
                quoted = self.reply_to.render(real_name=real_name, link_name=link_name,
                                              delimiter=delimiter, strip_links=True, trim=32)
                output.prepend(*(quoted.indent("\N{BOX DRAWINGS LIGHT VERTICAL} ")), Segment("\n"))
        return output

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return ((self.text, self.user, self.action, self.reply_to) ==
                (other.text, other.user, other.action, other.reply_to))

    def __hash__(self):
        return hash((self.user, self.text, self.action, self.reply_to))

    def _repr_parts(self):
        return " ".join(filter(None, (repr(self.user) if self.user else None,
                                      repr(str(self.text)) if self.text else None,
                                      "join" if self.joined else None,
                                      "leave" if self.left else None,
                                      ("+{}".format(len(self.attachments))
                                       if self.attachments else None))))

    def __repr__(self):
        parts = self._repr_parts()
        return "<{}{}>".format(self.__class__.__name__, ": {}".format(parts) if parts else "")


@pretty_str
class Receipt:
    """
    Reference to a physical message received from a plug.  This provides metadata for identifying
    a source message, in addition to the actual content attributes.

    Attributes:
        id (str):
            Unique (to the plug) message identifier, which should persist across edits and deletes.
        channel (.Channel):
            Source channel of this message.
        at (datetime.datetime):
            Timestamp of the message according to the external server, defaults to the current time
            at creation if unset.
        revision (str):
            Key to uniquely identify updates to a previous message, defaults to :attr:`id`.  Need
            not be in the same format as the main identifier.
        edited (bool):
            Whether the message content has been changed.
        deleted (bool):
            Whether the message was deleted from its source.
    """

    def __init__(self, id, channel, *, at=None, revision=None, edited=False, deleted=False):
        self.id = str(id)
        self.channel = channel
        self.at = at or datetime.now(timezone.utc)
        self.revision = str(revision or id)
        self.edited = edited
        self.deleted = deleted

    async def delete(self):
        """
        Equivalent to :meth:`.Plug.delete`.
        """
        return await self.channel.plug.delete(self)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.id, self.revision, self.channel) == (other.id, other.revision, other.channel)

    def __hash__(self):
        return hash((self.id, self.revision, self.channel))

    def __repr__(self):
        return "<{}: {} @ {} {}{}{}>".format(self.__class__.__name__, self.id, self.at,
                                             repr(self.channel), " edited" if self.edited else "",
                                             " deleted" if self.deleted else "")


class SentMessage(Receipt, Message):
    """
    Combination of :class:`.Receipt` and :class:`.Message`.
    """

    def __init__(self, id, channel, *, at=None, revision=None, edited=False, deleted=False,
                 text=None, user=None, action=False, reply_to=None, joined=None, left=None,
                 title=None, attachments=None, raw=None):
        Receipt.__init__(self, id=id, channel=channel, revision=revision, at=at, edited=edited,
                         deleted=deleted)
        Message.__init__(self, text=text, user=user, action=action, reply_to=reply_to,
                         joined=joined, left=left, title=title, attachments=attachments, raw=raw)

    def __repr__(self):
        parts = self._repr_parts()
        receipt = super().__repr__()
        return "{}{}{}".format(receipt[:-1], " {}".format(parts) if parts else "", receipt[-1])
