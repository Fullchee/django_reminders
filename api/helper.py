import json
from urllib import parse, request
from re import search
from typing import Tuple, Optional

import logging

logger = logging.getLogger(__name__)


def parse_keywords(keywords):
    return list(map(lambda keyword: keyword["value"], keywords))


def get_youtube_id(url: str) -> str:
    """
    :param url: potentially encoded or shortened YouTube URL
    :return: the YouTube video ID
    """

    matches = get_youtube_url_matches(url)

    for match in matches:
        try:
            return match.groups()[0]
        except Exception as e:
            logger.debug(f"Match failed: {e}")
    return ""


def get_youtube_url_matches(url: str):
    desktop_match = search(
        "youtube\.com/watch\?v=([a-zA-Z0-9-_]{11})",
        url,
    )
    shortened_youtube_match = search(
        "https://youtu.be/([a-zA-Z0-9-_]{11})",
        url,
    )
    firefox_android_mobile_match = search(
        "m.youtube.com/watch%3Fv%3D([a-zA-Z0-9-_]{11})&",
        url,
    )
    firefox_android_desktop_match = search(
        "youtube.com%2Fwatch%3Fv%3D([a-zA-Z0-9-_]{11})",
        url,
    )
    youtube_short_match = search(
        "youtube.com/shorts/([a-zA-Z0-9-_]{11})",
        url,
    )
    return [
        desktop_match,
        shortened_youtube_match,
        firefox_android_mobile_match,
        firefox_android_desktop_match,
        youtube_short_match,
    ]

def get_youtube_time(url: str) -> int:
    time_match = search(
        "\?t=(\d+)$",
        url,
    )
    try:
        return int(time_match.groups()[0])
    except Exception:
        return 0


def extract_youtube_info(url: str) -> Tuple[str, Optional[int]]:
    """
    :param url: URL
    :return: (short YouTube URL, youtube start time)
             if not a YouTube URL, return (url, None)
    """
    youtube_id = get_youtube_id(url)
    if youtube_id:
        return f"https://youtu.be/{youtube_id}", get_youtube_time(url)
    return url, None


def generate_youtube_title(url: str) -> str:
    """
    https://stackoverflow.com/a/52664178/8479344
    :param url: YouTube URL
    :return: str - f"{author name}: {video title}"
    """
    youtube_id = get_youtube_id(url)
    if not youtube_id:
        return ""
    params = {
        "format": "json",
        "url": "https://www.youtube.com/watch?v=%s" % youtube_id,
    }

    url = "https://www.youtube.com/oembed"
    query_string = parse.urlencode(params)
    url = url + "?" + query_string

    with request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        return f"{data['author_name']}: {data['title']}"

