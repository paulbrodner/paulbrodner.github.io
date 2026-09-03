"""pytest configuration for the SEO regression suite.

`pytest_addoption` is only honoured in a conftest.py -- defining it inside
test_seo.py silently fails to register the option, and every test that touches
the `base_url` fixture then errors with "no option named '--base-url'".
"""


def pytest_addoption(parser):
    parser.addoption(
        "--base-url",
        action="store",
        default=None,
        help="Run against a live origin instead of the local _site/ build.",
    )
