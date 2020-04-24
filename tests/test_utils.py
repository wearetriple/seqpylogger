import pytest
from seqpylogger import utils


@pytest.mark.parametrize(
    "input_url,expected",
    [
        ("http://example.com", "http://example.com/"),
        ("http://example.com?test=okey", "http://example.com?test=okey"),
        ("http://localhost:8794/", "http://localhost:8794/"),
        ("http://localhost:8794", "http://localhost:8794/"),
    ],
)
def test_url_add_trailing_slash(input_url, expected):
    # Arrange

    # Act
    result = utils.url_add_trailing_slash(input_url)

    # Assert
    assert result == expected
