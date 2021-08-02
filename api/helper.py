from re import search


def parse_keywords(keywords):
    return list(map(lambda keyword: keyword["value"], keywords))


def shorten_youtube_link(link: str):
    match = search(
        "youtube\.com/watch\?v=([a-zA-Z0-9-_]{11})",
        link,
    )
    try:
        youtube_id = match.groups()[0]
        return f"https://youtu.be/{youtube_id}"
    except Exception:
        return link
