from urllib.parse import SplitResult

import pytest

from yarl import URL


class TestScheme:
    def test_scheme_path(self) -> None:
        u = URL("scheme:path")
        assert u.scheme == "scheme"
        assert u.host is None
        assert u.path == "path"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_scheme_path_other(self) -> None:
        u = URL("scheme:path:other")
        assert u.scheme == "scheme"
        assert u.host is None
        assert u.path == "path:other"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_complex_scheme(self) -> None:
        u = URL("allow+chars-33.:path")
        assert u.scheme == "allow+chars-33."
        assert u.host is None
        assert u.path == "path"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_scheme_only(self) -> None:
        u = URL("simple:")
        assert u.scheme == "simple"
        assert u.host is None
        assert u.path == ""
        assert u.query_string == ""
        assert u.fragment == ""

    def test_no_scheme1(self) -> None:
        u = URL("google.com:80")
        assert u.scheme == "google.com"
        assert u.host is None
        assert u.path == "80"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_no_scheme2(self) -> None:
        u = URL("google.com:80/root")
        assert u.scheme == "google.com"
        assert u.host is None
        assert u.path == "80/root"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_not_a_scheme1(self) -> None:
        u = URL("not_cheme:path")
        assert u.scheme == ""
        assert u.host is None
        assert u.path == "not_cheme:path"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_not_a_scheme2(self) -> None:
        u = URL("signals37:book")
        assert u.scheme == "signals37"
        assert u.host is None
        assert u.path == "book"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_scheme_rel_path1(self) -> None:
        u = URL(":relative-path")
        assert u.scheme == ""
        assert u.host is None
        assert u.path == ":relative-path"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_scheme_rel_path2(self) -> None:
        u = URL(":relative/path")
        assert u.scheme == ""
        assert u.host is None
        assert u.path == ":relative/path"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_scheme_weird(self) -> None:
        u = URL("://and-this")
        assert u.scheme == ""
        assert u.host is None
        assert u.path == "://and-this"
        assert u.query_string == ""
        assert u.fragment == ""


class TestHost:
    def test_canonical(self) -> None:
        u = URL("scheme://host/path")
        assert u.scheme == "scheme"
        assert u.host == "host"
        assert u.path == "/path"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_absolute_no_scheme(self) -> None:
        u = URL("//host/path")
        assert u.scheme == ""
        assert u.host == "host"
        assert u.path == "/path"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_absolute_no_scheme_complex_host(self) -> None:
        u = URL("//host+path")
        assert u.scheme == ""
        assert u.host == "host+path"
        assert u.path == "/"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_absolute_no_scheme_simple_host(self) -> None:
        u = URL("//host")
        assert u.scheme == ""
        assert u.host == "host"
        assert u.path == "/"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_weird_host(self) -> None:
        u = URL("//this+is$also&host!")
        assert u.scheme == ""
        assert u.host == "this+is$also&host!"
        assert u.path == "/"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_scheme_no_host(self) -> None:
        u = URL("scheme:/host/path")
        assert u.scheme == "scheme"
        assert u.host is None
        assert u.path == "/host/path"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_scheme_no_host2(self) -> None:
        u = URL("scheme:///host/path")
        assert u.scheme == "scheme"
        assert u.host is None
        assert u.path == "/host/path"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_no_scheme_no_host(self) -> None:
        u = URL("scheme//host/path")
        assert u.scheme == ""
        assert u.host is None
        assert u.path == "scheme//host/path"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_ipv4(self) -> None:
        u = URL("//127.0.0.1/")
        assert u.scheme == ""
        assert u.host == "127.0.0.1"
        assert u.path == "/"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_ipv6(self) -> None:
        u = URL("//[::1]/")
        assert u.scheme == ""
        assert u.host == "::1"
        assert u.path == "/"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_ipvfuture_address(self) -> None:
        u = URL("//[v1.-1]/")
        assert u.scheme == ""
        assert u.host == "v1.-1"
        assert u.path == "/"
        assert u.query_string == ""
        assert u.fragment == ""


class TestPort:
    def test_canonical(self) -> None:
        u = URL("//host:80/path")
        assert u.scheme == ""
        assert u.host == "host"
        assert u.port == 80
        assert u.path == "/path"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_no_path(self) -> None:
        u = URL("//host:80")
        assert u.scheme == ""
        assert u.host == "host"
        assert u.port == 80
        assert u.path == "/"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_no_host(self) -> None:
        u = URL("//:77")
        assert u.scheme == ""
        assert u.host == ""
        assert u.port == 77
        assert u.path == "/"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_double_port(self) -> None:
        with pytest.raises(ValueError):
            URL("//h:22:80/")

    def test_bad_port(self) -> None:
        with pytest.raises(ValueError):
            URL("//h:no/path")

    def test_another_bad_port(self) -> None:
        with pytest.raises(ValueError):
            URL("//h:22:no/path")

    def test_bad_port_again(self) -> None:
        with pytest.raises(ValueError):
            URL("//h:-80/path")


class TestUserInfo:
    def test_canonical(self) -> None:
        u = URL("sch://user@host/")
        assert u.scheme == "sch"
        assert u.user == "user"
        assert u.host == "host"
        assert u.path == "/"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_user_pass(self) -> None:
        u = URL("//user:pass@host")
        assert u.scheme == ""
        assert u.user == "user"
        assert u.password == "pass"
        assert u.host == "host"
        assert u.path == "/"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_complex_userinfo(self) -> None:
        u = URL("//user:pas:and:more@host")
        assert u.scheme == ""
        assert u.user == "user"
        assert u.password == "pas:and:more"
        assert u.host == "host"
        assert u.path == "/"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_no_user(self) -> None:
        u = URL("//:pas:@host")
        assert u.scheme == ""
        assert u.user is None
        assert u.password == "pas:"
        assert u.host == "host"
        assert u.path == "/"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_weird_user(self) -> None:
        u = URL("//!($&')*+,;=@host")
        assert u.scheme == ""
        assert u.user == "!($&')*+,;="
        assert u.password is None
        assert u.host == "host"
        assert u.path == "/"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_weird_user2(self) -> None:
        u = URL("//user@info@ya.ru")
        assert u.scheme == ""
        assert u.user == "user@info"
        assert u.password is None
        assert u.host == "ya.ru"
        assert u.path == "/"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_weird_user3(self) -> None:
        u = URL("//%5Bsome%5D@host")
        assert u.scheme == ""
        assert u.user == "[some]"
        assert u.password is None
        assert u.host == "host"
        assert u.path == "/"
        assert u.query_string == ""
        assert u.fragment == ""


class TestQuery_String:
    def test_simple(self) -> None:
        u = URL("?query")
        assert u.scheme == ""
        assert u.user is None
        assert u.password is None
        assert u.host is None
        assert u.path == ""
        assert u.query_string == "query"
        assert u.fragment == ""

    def test_scheme_query(self) -> None:
        u = URL("http:?query")
        assert u.scheme == "http"
        assert u.user is None
        assert u.password is None
        assert u.host is None
        assert u.path == ""
        assert u.query_string == "query"
        assert u.fragment == ""

    def test_abs_url_query(self) -> None:
        u = URL("//host?query")
        assert u.scheme == ""
        assert u.user is None
        assert u.password is None
        assert u.host == "host"
        assert u.path == "/"
        assert u.query_string == "query"
        assert u.fragment == ""

    def test_abs_url_path_query(self) -> None:
        u = URL("//host/path?query")
        assert u.scheme == ""
        assert u.user is None
        assert u.password is None
        assert u.host == "host"
        assert u.path == "/path"
        assert u.query_string == "query"
        assert u.fragment == ""

    def test_double_question_mark(self) -> None:
        u = URL("//ho?st/path?query")
        assert u.scheme == ""
        assert u.user is None
        assert u.password is None
        assert u.host == "ho"
        assert u.path == "/"
        assert u.query_string == "st/path?query"
        assert u.fragment == ""

    def test_complex_query(self) -> None:
        u = URL("?a://b:c@d.e/f?g#h")
        assert u.scheme == ""
        assert u.user is None
        assert u.password is None
        assert u.host is None
        assert u.path == ""
        assert u.query_string == "a://b:c@d.e/f?g"
        assert u.fragment == "h"

    def test_query_in_fragment(self) -> None:
        u = URL("#?query")
        assert u.scheme == ""
        assert u.user is None
        assert u.password is None
        assert u.host is None
        assert u.path == ""
        assert u.query_string == ""
        assert u.fragment == "?query"


class TestFragment:
    def test_simple(self) -> None:
        u = URL("#frag")
        assert u.scheme == ""
        assert u.user is None
        assert u.password is None
        assert u.host is None
        assert u.path == ""
        assert u.query_string == ""
        assert u.fragment == "frag"

    def test_scheme_frag(self) -> None:
        u = URL("http:#frag")
        assert u.scheme == "http"
        assert u.user is None
        assert u.password is None
        assert u.host is None
        assert u.path == ""
        assert u.query_string == ""
        assert u.fragment == "frag"

    def test_host_frag(self) -> None:
        u = URL("//host#frag")
        assert u.scheme == ""
        assert u.user is None
        assert u.password is None
        assert u.host == "host"
        assert u.path == "/"
        assert u.query_string == ""
        assert u.fragment == "frag"

    def test_scheme_path_frag(self) -> None:
        u = URL("//host/path#frag")
        assert u.scheme == ""
        assert u.user is None
        assert u.password is None
        assert u.host == "host"
        assert u.path == "/path"
        assert u.query_string == ""
        assert u.fragment == "frag"

    def test_scheme_query_frag(self) -> None:
        u = URL("//host?query#frag")
        assert u.scheme == ""
        assert u.user is None
        assert u.password is None
        assert u.host == "host"
        assert u.path == "/"
        assert u.query_string == "query"
        assert u.fragment == "frag"

    def test_host_frag_query(self) -> None:
        u = URL("//ho#st/path?query")
        assert u.scheme == ""
        assert u.user is None
        assert u.password is None
        assert u.host == "ho"
        assert u.path == "/"
        assert u.query_string == ""
        assert u.fragment == "st/path?query"

    def test_complex_frag(self) -> None:
        u = URL("#a://b:c@d.e/f?g#h")
        assert u.scheme == ""
        assert u.user is None
        assert u.password is None
        assert u.host is None
        assert u.path == ""
        assert u.query_string == ""
        assert u.fragment == "a://b:c@d.e/f?g#h"


class TestStripEmptyParts:
    def test_all_empty_http(self) -> None:
        with pytest.raises(ValueError):
            URL("http://@:?#")

    def test_all_empty(self) -> None:
        u = URL("//@:?#")
        assert u.scheme == ""
        assert u.user is None
        assert u.password is None
        assert u.host == ""
        assert u.path == ""
        assert u.query_string == ""
        assert u.fragment == ""

    def test_path_only(self) -> None:
        u = URL("///path")
        assert u.scheme == ""
        assert u.user is None
        assert u.password is None
        assert u.host is None
        assert u.path == "/path"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_empty_user(self) -> None:
        u = URL("//@host")
        assert u.scheme == ""
        assert u.user is None
        assert u.password is None
        assert u.host == "host"
        assert u.path == "/"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_empty_port(self) -> None:
        u = URL("//host:")
        assert u.scheme == ""
        assert u.user is None
        assert u.password is None
        assert u.host == "host"
        assert u.path == "/"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_empty_port_and_path(self) -> None:
        u = URL("//host:/")
        assert u.scheme == ""
        assert u.user is None
        assert u.password is None
        assert u.host == "host"
        assert u.path == "/"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_empty_path_only(self) -> None:
        u = URL("/")
        assert u.scheme == ""
        assert u.user is None
        assert u.password is None
        assert u.host is None
        assert u.path == "/"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_relative_path_only(self) -> None:
        u = URL("path")
        assert u.scheme == ""
        assert u.user is None
        assert u.password is None
        assert u.host is None
        assert u.path == "path"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_path(self) -> None:
        u = URL("/path")
        assert u.scheme == ""
        assert u.user is None
        assert u.password is None
        assert u.host is None
        assert u.path == "/path"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_empty_query_with_path(self) -> None:
        u = URL("/path?")
        assert u.scheme == ""
        assert u.user is None
        assert u.password is None
        assert u.host is None
        assert u.path == "/path"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_empty_query(self) -> None:
        u = URL("?")
        assert u.scheme == ""
        assert u.user is None
        assert u.password is None
        assert u.host is None
        assert u.path == ""
        assert u.query_string == ""
        assert u.fragment == ""

    def test_empty_query_with_frag(self) -> None:
        u = URL("?#frag")
        assert u.scheme == ""
        assert u.user is None
        assert u.password is None
        assert u.host is None
        assert u.path == ""
        assert u.query_string == ""
        assert u.fragment == "frag"

    def test_path_empty_frag(self) -> None:
        u = URL("/path#")
        assert u.scheme == ""
        assert u.user is None
        assert u.password is None
        assert u.host is None
        assert u.path == "/path"
        assert u.query_string == ""
        assert u.fragment == ""

    def test_empty_path(self) -> None:
        u = URL("#")
        assert u.scheme == ""
        assert u.user is None
        assert u.password is None
        assert u.host is None
        assert u.path == ""
        assert u.query_string == ""
        assert u.fragment == ""


@pytest.mark.parametrize(
    ("scheme"),
    [
        ("http"),
        ("https"),
        ("ws"),
        ("wss"),
        ("ftp"),
    ],
)
def test_schemes_that_require_host(scheme: str) -> None:
    """Verify that schemes that require a host raise with empty host."""
    expect = (
        "Invalid URL: host is required for " f"absolute urls with the {scheme} scheme"
    )
    with pytest.raises(ValueError, match=expect):
        URL(f"{scheme}://:1")


@pytest.mark.parametrize(
    ("url", "hostname", "hostname_without_brackets"),
    [
        ("http://[::1]", "[::1]", "::1"),
        ("http://[::1]:8080", "[::1]", "::1"),
        ("http://127.0.0.1:8080", "127.0.0.1", "127.0.0.1"),
        (
            "http://xn--jxagkqfkduily1i.eu",
            "xn--jxagkqfkduily1i.eu",
            "xn--jxagkqfkduily1i.eu",
        ),
    ],
)
def test_url_round_trips(
    url: str, hostname: str, hostname_without_brackets: str
) -> None:
    """Verify that URLs round-trip correctly."""
    parsed = URL(url)
    assert SplitResult(*parsed._val).hostname == hostname_without_brackets
    assert parsed.raw_host == hostname_without_brackets
    assert parsed.host_subcomponent == hostname
    assert str(parsed) == url
    assert str(URL(str(parsed))) == url
