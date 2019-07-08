# flake8: noqa

from .endpoints import AnswerInlineQuery
from .input_message_content import Text as InputTextMessageContent, \
    Location as InputLocationMessageContent, \
    Venue as InputVenueMessageContent, \
    Contact as InputContactMessageContent
from .query_results import Article as InlineQueryResultArticle, \
    Photo as InlineQueryResultPhoto, \
    CachedPhoto as InlineQueryResultCachedPhoto, \
    Gif as InlineQueryResultGif, \
    CachedGif as InlineQueryResultCachedGif, \
    Mpeg4Gif as InlineQueryResultMpeg4Gif, \
    CachedMpeg4Gif as InlineQueryResultCachedMpeg4Gif, \
    Video as InlineQueryResultVideo, \
    CachedVideo as InlineQueryResultCachedVideo, \
    Audio as InlineQueryResultAudio, \
    CachedAudio as InlineQueryResultCachedAudio, \
    Voice as InlineQueryResultVoice, \
    CachedVoice as InlineQueryResultCachedVoice, \
    Document as InlineQueryResultDocument, \
    CachedDocument as InlineQueryResultCachedDocument, \
    Location as InlineQueryResultLocation, \
    Venue as InlineQueryResultVenue, \
    Contact as InlineQueryResultContact, \
    Game as InlineQueryResultGame, \
    CachedSticker as InlineQueryResultCachedSticker
