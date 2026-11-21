
from src.feature_extractor import get_url_length
from src.feature_extractor import count_suspicious_keywords
from src.feature_extractor import has_ip_address
from src.feature_extractor import count_subdomains
from src.feature_extractor import count_special_characters
from src.feature_extractor import uses_https
from src.feature_extractor import extract_features
from src.url_parser import parse_url


from src.feature_extractor import (
    get_domain_length,
    count_hostname_digits,
    count_hostname_hyphens
)


def test_parse_url():
    result = parse_url("https://login.example.com/account?id=10")

    assert result["scheme"] == "https"
    assert result["hostname"] == "login.example.com"
    assert result["path"] == "/account"
    assert result["query"] == "id=10"


def test_url_without_scheme():
    result = parse_url("example.com")

    assert result["scheme"] == "https"
    assert result["hostname"] == "example.com"


def test_get_url_length():
    result = get_url_length("https://example.com")

    assert result == 19

def test_ip_address_detection():
    assert has_ip_address("http://192.168.1.10/login") is True
    assert has_ip_address("https://example.com/login") is False

def test_suspicious_keyword_detection():
    assert count_suspicious_keywords("https://example.com/login") == 1

    assert count_suspicious_keywords(
        "https://example.com/login/verify/account"
    ) == 3

    assert count_suspicious_keywords("https://example.com/home") == 0

def test_subdomain_count():
    assert count_subdomains("https://example.com") == 0

    assert count_subdomains("https://login.example.com") == 1

    assert count_subdomains(
        "https://login.account.example.com"
    ) == 2

def test_special_character_count():
    assert count_special_characters(
        "https://example.com/login"
    ) == 0

    assert count_special_characters(
        "https://secure-example.com/login?id=10"
    ) == 2

    assert count_special_characters(
        "https://example.com/user_name"
    ) == 1

def test_https_detection():
    assert uses_https("https://example.com") is True
    assert uses_https("http://example.com") is False
    assert uses_https("example.com") is False

def test_extract_features():
    result = extract_features("https://example.com")

    assert result["url_length"] == 19
    assert result["has_ip_address"] is False
    assert result["suspicious_keyword_count"] == 0
    assert result["subdomain_count"] == 0
    assert result["special_character_count"] == 0
    assert result["uses_https"] is True

def test_domain_features():
    url = "https://example123-test.com"

    assert get_domain_length(url) == 19
    assert count_hostname_digits(url) == 3
    assert count_hostname_hyphens(url) == 1