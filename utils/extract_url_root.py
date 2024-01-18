from urllib.parse import ParseResult, urlparse


def extract_url_root(url: str) -> str:
    parsed_url: ParseResult = urlparse(url)
    root: str = parsed_url.netloc
    return root
