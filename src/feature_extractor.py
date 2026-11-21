
from urllib.parse import urlsplit
import ipaddress


# Suspicious keywords to look for in URLs
SUSPICIOUS_KEYWORDS = [
    "login",
    "verify",
    "secure",
    "update",
    "account",
    "password",
    "signin",
    "banking"
]


def get_url_length(url):
    """Return the total number of characters in a URL."""
    return len(url)


def has_ip_address(url):
    """Check whether the URL uses an IP address as its hostname."""

    if "://" not in url:
        url = "https://" + url

    hostname = urlsplit(url).hostname

    if hostname is None:
        return False

    try:
        ipaddress.ip_address(hostname)
        return True

    except ValueError:
        return False


def count_suspicious_keywords(url):
    """Count suspicious keywords found in a URL."""

    url = url.lower()
    count = 0

    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in url:
            count += 1

    return count


def count_subdomains(url):
    """Count the number of subdomains in a URL."""

    if "://" not in url:
        url = "https://" + url

    hostname = urlsplit(url).hostname

    if hostname is None:
        return 0

    parts = hostname.split(".")

    return max(0, len(parts) - 2)


def count_special_characters(url):
    """Count selected special characters in a URL."""

    special_characters = ["@", "-", "_", "%", "="]

    count = 0

    for character in special_characters:
        count += url.count(character)

    return count


def uses_https(url):
    """Check whether a URL uses HTTPS."""

    if "://" not in url:
        return False

    return url.lower().startswith("https://")


def get_domain_length(url):
    """Return the hostname length."""

    if "://" not in url:
        url = "https://" + url

    hostname = urlsplit(url).hostname or ""

    return len(hostname)


def count_hostname_digits(url):
    """Count digits in the hostname."""

    if "://" not in url:
        url = "https://" + url

    hostname = urlsplit(url).hostname or ""

    return sum(character.isdigit() for character in hostname)


def count_hostname_hyphens(url):
    """Count hyphens in the hostname."""

    if "://" not in url:
        url = "https://" + url

    hostname = urlsplit(url).hostname or ""

    return hostname.count("-")


def extract_features(url):
    """Extract all nine URL analysis features."""

    features = {
        "url_length": get_url_length(url),
        "has_ip_address": has_ip_address(url),
        "suspicious_keyword_count": count_suspicious_keywords(url),
        "subdomain_count": count_subdomains(url),
        "special_character_count": count_special_characters(url),
        "uses_https": uses_https(url),
        "domain_length": get_domain_length(url),
        "hostname_digit_count": count_hostname_digits(url),
        "hostname_hyphen_count": count_hostname_hyphens(url)
    }

    return features
