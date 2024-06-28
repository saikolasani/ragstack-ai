from dataclasses import dataclass
from typing import TYPE_CHECKING, Set, Union
from urllib.parse import urldefrag, urljoin, urlparse

from ragstack_langchain.graph_store.links import Link, add_links

from .link_extractor import LinkExtractor

if TYPE_CHECKING:
    from bs4 import BeautifulSoup


def _parse_url(link, page_url, drop_fragments: bool = True):
    href = link.get("href")
    if href is None:
        return None
    url = urlparse(href)
    if url.scheme not in ["http", "https", ""]:
        return None

    # Join the HREF with the page_url to convert relative paths to absolute.
    url = urljoin(page_url, href)

    # Fragments would be useful if we chunked a page based on section.
    # Then, each chunk would have a different URL based on the fragment.
    # Since we aren't doing that yet, they just "break" links. So, drop
    # the fragment.
    if drop_fragments:
        return urldefrag(url).url
    else:
        return url


def _parse_hrefs(
    soup: "BeautifulSoup", url: str, drop_fragments: bool = True
) -> Set[str]:
    links = soup.find_all("a")
    links = {
        _parse_url(link, page_url=url, drop_fragments=drop_fragments) for link in links
    }

    # Remove entries for any 'a' tag that failed to parse (didn't have href,
    # or invalid domain, etc.)
    links.discard(None)

    # Remove self links.
    links.discard(url)

    return links


@dataclass
class HtmlInput:
    content: Union[str, "BeautifulSoup"]
    base_url: str


class HtmlLinkExtractor(LinkExtractor[HtmlInput]):
    def __init__(self, *, kind: str = "hyperlink", drop_fragments: bool = True):
        """Extract hyperlinks from HTML content.

        Expects the input to be an HTML string or a `BeautifulSoup` object.

        Args:
            kind: The kind of edge to extract. Defaults to "hyperlink".
            drop_fragments: Whether fragments in URLs and links shoud be
                dropped. Defaults to `True`.
        """
        try:
            import bs4  # noqa:F401
        except ImportError:
            raise ImportError(
                "BeautifulSoup4 is required for HtmlLinkExtractor. "
                "Please install it with `pip install beautifulsoup4`."
            )

        self._kind = kind
        self.drop_fragments = drop_fragments

    def extract_one(
        self,
        input: HtmlInput,
    ) -> Set[Link]:
        content = input.content
        if isinstance(content, str):
            from bs4 import BeautifulSoup

            content = BeautifulSoup(content, "html.parser")

        base_url = input.base_url
        if self.drop_fragments:
            base_url = urldefrag(base_url).url

        hrefs = _parse_hrefs(content, base_url, self.drop_fragments)

        links = {Link.outgoing(kind=self._kind, tag=url) for url in hrefs}
        links.add(Link.incoming(kind=self._kind, tag=base_url))
        return links