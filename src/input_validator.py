
from urllib.parse import urlsplit
import ipaddress
import re


def validate_url(url):
    """Check whether the submitted URL has a valid structure."""

    if not isinstance(url, str) or not url.strip():
        return False, "Please enter a URL."

    url = url.strip()

    if any(character.isspace() for character in url):
        return False, "URL must not contain spaces."

    if len(url) > 2048:
        return False, "URL is too long."

    try:
        parsed = urlsplit(url)

        if parsed.scheme.lower() not in ("http", "https"):
            return False, "Only HTTP and HTTPS URLs are supported."

        if not parsed.hostname:
            return False, "URL must contain a hostname."

        try:
            parsed.port
        except ValueError:
            return False, "URL contains an invalid port."

        hostname = parsed.hostname

        try:
            ipaddress.ip_address(hostname)
            return True, "Valid URL structure."
        except ValueError:
            pass

        hostname = hostname.rstrip(".")

        if len(hostname) > 253:
            return False, "Hostname is too long."

        labels = hostname.split(".")

        if len(labels) < 2:
            return False, "Hostname must contain a domain and extension."

        for label in labels:
            if (
                not label
                or len(label) > 63
                or not re.fullmatch(
                    r"[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?",
                    label
                )
            ):
                return False, "Hostname format is invalid."

        return True, "Valid URL structure."

    except ValueError:
        return False, "Invalid URL format."
