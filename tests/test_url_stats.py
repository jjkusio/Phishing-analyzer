import pytest

from features.URL_stats import (
    check_at,
    check_characters,
    check_distance,
    check_http,
    check_ip,
    check_keywords,
    check_latin,
    check_length,
    check_numbers,
    check_shannon_entropy,
    check_subdomains,
    check_sus_domains,
    check_tld,
    features,
    is_free_hosting,
    is_shortened,
)


def test_check_http():
    assert check_http("http://example.com") == 1
    assert check_http("https://example.com") == 0


def test_check_length():
    assert check_length("https://example.com") == 7
    assert check_length("https://sub.example.com/path") == 7


def test_check_tld():
    assert check_tld("https://example.com") == 1
    assert check_tld("https://example.dev") == 0


def test_check_ip():
    assert check_ip("http://192.168.1.10/login") == 1
    assert check_ip("https://example.com") == 0


def test_check_latin():
    assert check_latin("https://example.com") == 0
    assert check_latin("https://zółw.pl") == 1


def test_check_shannon_entropy():
    assert check_shannon_entropy("https://aaaa.com") == 0
    assert check_shannon_entropy("https://ab.com") == pytest.approx(1.0)


def test_check_at():
    assert check_at("https://example.com@evil.com") == 1
    assert check_at("https://example.com") == 0


def test_check_characters():
    assert check_characters("https://login-secure.example.com/path") == 1
    assert check_characters("https://example.com/path?x=1") == 0


def test_check_numbers():
    assert check_numbers("https://login123.example.com") == 3
    assert check_numbers("https://example.com/path/123") == 0


def test_check_subdomains():
    assert check_subdomains("https://example.com") == 0
    assert check_subdomains("https://a.b.example.com") == 2


def test_check_suspicious_domains():
    assert check_sus_domains("https://example.xyz") == 1
    assert check_sus_domains("https://example.com") == 0


def test_check_keywords():
    url = "https://secure-login.example.com/account/reset"

    assert check_keywords(url) == 4
    assert check_keywords("https://example.com/home") == 0


def test_check_distance():
    popular_domains = {"google", "github"}

    assert check_distance("https://goggle.com", popular_domains) == 1
    assert check_distance("https://github.com", popular_domains) == 0


def test_is_free_hosting():
    assert is_free_hosting("https://my-project.github.io") == 1
    assert is_free_hosting("https://example.com") == 0


def test_is_shortened():
    assert is_shortened("https://bit.ly/example") == 1
    assert is_shortened("https://example.com/path") == 0


def test_features_returns_complete_static_vector():
    result = features("http://login1.example.xyz", {"example"})

    assert set(result) == {
        "HTTP",
        "URL Length",
        "Popular tld in URL",
        "IP",
        "Non-latin characters",
        "Entropy",
        "@ in url",
        "Suspicious characters",
        "Digits",
        "Subdomains",
        "Sus domains",
        "Number of phishing words",
        "Levenshtein Distance",
        "URL is shortened",
    }
    assert result["HTTP"] == 1
    assert result["Digits"] == 1
    assert result["Subdomains"] == 1
    assert result["Sus domains"] == 1
    assert result["Levenshtein Distance"] == 0

