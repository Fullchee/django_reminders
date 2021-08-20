from re import search

import urllib.request
import json
import urllib
import pprint


def parse_keywords(keywords):
    return list(map(lambda keyword: keyword["value"], keywords))


def get_youtube_id(url: str) -> str:
    desktop_match = search(
        "youtube\.com/watch\?v=([a-zA-Z0-9-_]{11})",
        url,
    )

    shortened_youtube_match = search(
        "https://youtu.be/([a-zA-Z0-9-_]{11})",
        url,
    )
    google_mobile_match = search(
        "m.youtube.com/watch%3Fv%3D([a-zA-Z0-9-_]{11})&sa",
        url,
    )

    try:
        return desktop_match.groups()[0]
    except Exception:
        try:
            return google_mobile_match.groups()[0]
        except Exception:
            try:
                return shortened_youtube_match.groups()[0]
            except Exception:
                return ""


def get_youtube_time(url: str) -> str:
    time_match = search(
        "(\?t=\d+)$",
        url,
    )
    try:
        return time_match.groups()[0]
    except Exception:
        return ""


def shorten_youtube_url(url: str) -> str:
    youtube_id = get_youtube_id(url)
    if youtube_id:
        return f"https://youtu.be/{youtube_id}{get_youtube_time(url)}"
    return url


def generate_youtube_title(url: str) -> str:
    """
    https://stackoverflow.com/a/52664178/8479344
    :param url: str
    :return: str - author name: video title
    """
    youtube_id = get_youtube_id(url)
    if not youtube_id:
        return ""
    params = {
        "format": "json",
        "url": "https://www.youtube.com/watch?v=%s" % youtube_id,
    }

    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string

    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        return f"{data['author_name']}: {data['title']}"
