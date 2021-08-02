from re import search


def parse_keywords(keywords):
    return list(map(lambda keyword: keyword["value"], keywords))


def get_youtube_id(link: str):
    desktop_match = search(
        "youtube\.com/watch\?v=([a-zA-Z0-9-_]{11})",
        link,
    )
    google_mobile_match = search(
        "m.youtube.com/watch%3Fv%3D([a-zA-Z0-9-_]{11})&sa",
        'https://www.google.com/url?q=https://m.youtube.com/watch%3Fv%3DDME1vicSb1M&sa=U&ved=2ahUKEwj16IOFipPyAhVUVc0KHUTmDS8QtwIwAXoECGMQAQ&usg=AOvVaw1HRSqGljWzAmoELBbLHDdm'
    )

    try:
        return desktop_match.groups()[0]
    except Exception:
        try:
            return google_mobile_match.groups()[0]
        except Exception:
            return None


def shorten_youtube_link(link: str):
    youtube_id = get_youtube_id(link)
    if youtube_id:
        return f"https://youtu.be/{youtube_id}"
    return link
