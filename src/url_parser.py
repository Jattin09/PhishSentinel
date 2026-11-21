
from urllib.parse import urlsplit


def parse_url(url):
    """
    Extract basic components from a URL.
    """

    # Add a scheme if the user did not provide one
    if "://" not in url:
        url = "https://" + url

    parsed = urlsplit(url)

    return {
        "scheme": parsed.scheme,
        "hostname": parsed.hostname,
        "path": parsed.path,
        "query": parsed.query,
        "fragment": parsed.fragment
    }
