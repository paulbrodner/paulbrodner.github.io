#!/usr/bin/env python3
"""
SEO / GEO regression suite for paulbrodner.dev

Runs against the built Jekyll output (_site/) by default, or against a
live origin with --base-url.

    bundle exec jekyll build
    pytest tests/test_seo.py -v

    # or against production
    pytest tests/test_seo.py -v --base-url https://paulbrodner.dev

Requires: pytest, beautifulsoup4, lxml, requests, pillow
    pip install pytest beautifulsoup4 lxml requests pillow
"""

import json
import os
import re
import glob
from pathlib import Path
from urllib.parse import urlparse

import pytest
from bs4 import BeautifulSoup

SITE_DIR = Path(os.environ.get("SITE_DIR", "_site"))
EXPECTED_ORIGIN = "https://paulbrodner.dev"

# Pages that must be indexable. The first three were all noindex at one point;
# this test exists so they never silently go back.
MUST_BE_INDEXABLE = ["/", "/tags/", "/categories/", "/profile"]

# Paginated archives are intentionally excluded from indexing.
PAGINATION_RE = re.compile(r"^/page\d+/$")


# --------------------------------------------------------------------------
# fixtures / helpers
# --------------------------------------------------------------------------

@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--base-url")


# Standalone HTML artifacts (Markmap exports, embedded reports). These are
# static files copied verbatim, not Jekyll pages -- they have no layout and so
# no title/canonical/OG, and asserting against them is meaningless.
# /blog/ is a noindex redirect stub to / (old inbound links), same reasoning.
NON_PAGE_PREFIXES = ("/assets/", "/blog/")


def _local_pages():
    """Every .html file in _site, mapped to its site-relative URL."""
    if not SITE_DIR.is_dir():
        pytest.skip(f"{SITE_DIR} not found — run `bundle exec jekyll build` first")
    out = {}
    for path in SITE_DIR.rglob("*.html"):
        rel = path.relative_to(SITE_DIR).as_posix()
        url = "/" + rel.replace("index.html", "")
        if url.startswith(NON_PAGE_PREFIXES):
            continue
        out[url] = path
    return out


def _url_variants(url):
    """`permalink: /profile` builds profile.html, so the same page is reachable
    as /profile, /profile/ and /profile.html. Treat all three as one."""
    bare = url.rstrip("/")
    if bare.endswith(".html"):
        bare = bare[: -len(".html")]
    return {url, bare, bare + "/", bare + ".html", (bare or "/")}


def _resolves(pages, target):
    """True if `target` corresponds to something that was actually built."""
    return bool(_url_variants(target) & set(pages))


@pytest.fixture(scope="session")
def pages(base_url):
    if base_url:
        pytest.skip("page-level local tests skipped in --base-url mode")
    return _local_pages()


@pytest.fixture(scope="session")
def post_pages(pages):
    """Only article pages — permalink is /:year/:title/."""
    return {u: p for u, p in pages.items() if re.match(r"^/\d{4}/[^/]+/$", u)}


def soup_of(path):
    return BeautifulSoup(path.read_text(encoding="utf-8"), "lxml")


def meta(soup, name=None, prop=None):
    if name:
        tag = soup.find("meta", attrs={"name": name})
    else:
        tag = soup.find("meta", attrs={"property": prop})
    return tag.get("content") if tag else None


# --------------------------------------------------------------------------
# 1. indexability — the regression that started all this
# --------------------------------------------------------------------------

def _resolve(pages, url):
    """The built file for `url`, whichever variant Jekyll produced."""
    for candidate in _url_variants(url):
        if candidate in pages:
            return pages[candidate]
    return None


@pytest.mark.parametrize("url", MUST_BE_INDEXABLE)
def test_hub_pages_are_indexable(pages, url):
    path = _resolve(pages, url)
    assert path is not None, f"{url} was not built"
    robots = meta(soup_of(path), name="robots") or ""
    assert "noindex" not in robots.lower(), (
        f"{url} is noindex. Hub pages must be indexable or Google has no "
        f"internal link graph to crawl."
    )


def test_posts_are_indexable(post_pages):
    assert post_pages, "no post pages found — check the permalink pattern"
    for url, path in post_pages.items():
        robots = meta(soup_of(path), name="robots") or ""
        assert "noindex" not in robots.lower(), f"{url} is noindex"


def test_pagination_is_noindex_follow(pages):
    """Paginated archives duplicate the homepage listing, so they must not be
    indexed -- but they MUST stay crawlable. The homepage shows 5 of 28 posts;
    posts 6-28 are reachable only via pagination, tags and categories. See
    SEO/PLAN.md 2.1."""
    paginated = [u for u in pages if PAGINATION_RE.match(u)]
    if not paginated:
        pytest.skip("no paginated archives built")
    for url in paginated:
        robots = (meta(soup_of(pages[url]), name="robots") or "").lower()
        assert "noindex" in robots, (
            f"{url} is indexable and duplicates the homepage listing"
        )
        assert "nofollow" not in robots, (
            f"{url} is nofollow -- this severs the crawl path to posts 6-28"
        )


def test_pagination_is_not_disallowed_in_robots_txt(pages):
    """A Disallow blocks crawling entirely, which is strictly worse than
    noindex,follow: crawlers would never traverse to the older posts."""
    robots_txt = SITE_DIR / "robots.txt"
    if not robots_txt.exists():
        pytest.skip("no robots.txt")
    text = robots_txt.read_text(encoding="utf-8")
    offenders = re.findall(r"^\s*Disallow:\s*(/page.*)$", text, re.MULTILINE | re.IGNORECASE)
    assert not offenders, (
        "robots.txt disallows paginated archives "
        f"({', '.join(offenders)}) -- use noindex,follow instead"
    )


# --------------------------------------------------------------------------
# 2. Open Graph / Twitter — must be absolute, must exist on disk
# --------------------------------------------------------------------------

ABSOLUTE_URL_METAS = [
    ("prop", "og:image"),
    ("prop", "og:url"),
    ("name", "twitter:image"),
]


def test_social_image_urls_are_absolute(pages):
    """Relative og:image is the single most common silent breakage.
    LinkedIn and Twitter will not resolve it."""
    failures = []
    for url, path in pages.items():
        s = soup_of(path)
        for kind, key in ABSOLUTE_URL_METAS:
            val = meta(s, name=key) if kind == "name" else meta(s, prop=key)
            if val is None:
                failures.append(f"{url}: {key} missing")
            elif not urlparse(val).scheme:
                failures.append(f"{url}: {key} is relative ({val})")
    assert not failures, "\n".join(failures)


def test_social_image_file_exists_and_is_correctly_sized(pages):
    from PIL import Image

    seen = {}
    for url, path in pages.items():
        val = meta(soup_of(path), prop="og:image")
        if not val:
            continue
        rel = val.replace(EXPECTED_ORIGIN, "").lstrip("/")
        seen.setdefault(rel, []).append(url)

    for rel, using in seen.items():
        f = SITE_DIR / rel
        assert f.exists(), f"og:image {rel} does not exist (used by {using[0]})"
        w, h = Image.open(f).size
        assert w >= 1200 and h >= 600, (
            f"og:image {rel} is {w}x{h}. Target 1200x630 — anything smaller "
            f"renders as a thumbnail or not at all. Used by {len(using)} page(s)."
        )


def test_twitter_card_is_large_image(pages):
    for url, path in pages.items():
        card = meta(soup_of(path), name="twitter:card")
        assert card == "summary_large_image", f"{url}: twitter:card is {card!r}"


# --------------------------------------------------------------------------
# 3. canonical
# --------------------------------------------------------------------------

def test_canonical_is_present_absolute_and_self_referential(pages):
    failures = []
    for url, path in pages.items():
        if PAGINATION_RE.match(url):
            continue
        link = soup_of(path).find("link", rel="canonical")
        if not link or not link.get("href"):
            failures.append(f"{url}: no canonical")
            continue
        href = link["href"]
        if not urlparse(href).scheme:
            failures.append(f"{url}: canonical is relative ({href})")
        elif urlparse(href).path not in _url_variants(url):
            failures.append(f"{url}: canonical points elsewhere ({href})")
    assert not failures, "\n".join(failures)


# --------------------------------------------------------------------------
# 4. structured data
# --------------------------------------------------------------------------

REQUIRED_BLOGPOSTING_FIELDS = [
    "headline", "description", "image", "datePublished",
    "dateModified", "author", "url",
]


def test_posts_have_valid_blogposting_jsonld(post_pages):
    for url, path in post_pages.items():
        blocks = soup_of(path).find_all("script", type="application/ld+json")
        assert blocks, f"{url}: no JSON-LD"

        parsed = []
        for b in blocks:
            try:
                parsed.append(json.loads(b.string))
            except json.JSONDecodeError as e:
                pytest.fail(f"{url}: JSON-LD does not parse — {e}")

        posting = next((d for d in parsed if d.get("@type") == "BlogPosting"), None)
        assert posting, f"{url}: no BlogPosting block"

        missing = [f for f in REQUIRED_BLOGPOSTING_FIELDS if not posting.get(f)]
        assert not missing, f"{url}: BlogPosting missing {missing}"

        assert posting["author"].get("name"), f"{url}: author has no name"
        assert urlparse(posting["image"]).scheme, f"{url}: JSON-LD image is relative"


def test_profile_has_person_jsonld_with_sameas(pages):
    path = pages.get("/profile")
    if not path:
        pytest.skip("/profile not built")
    blocks = soup_of(path).find_all("script", type="application/ld+json")
    people = [json.loads(b.string) for b in blocks]
    person = next((d for d in people if d.get("@type") == "Person"), None)
    assert person, "/profile: no Person JSON-LD — entity resolution depends on this"
    same_as = person.get("sameAs", [])
    assert len(same_as) >= 3, (
        "/profile: sameAs needs LinkedIn + GitHub + Twitter so engines can "
        "resolve 'Paul Brodner' as one entity"
    )


# --------------------------------------------------------------------------
# 5. title & description hygiene
# --------------------------------------------------------------------------

def test_titles_are_present_unique_and_reasonable_length(pages):
    titles = {}
    for url, path in pages.items():
        # Paginated archives are noindex and legitimately share one title.
        if PAGINATION_RE.match(url):
            continue
        t = soup_of(path).find("title")
        assert t and t.text.strip(), f"{url}: no title"
        titles.setdefault(t.text.strip(), []).append(url)

    dupes = {t: u for t, u in titles.items() if len(u) > 1}
    assert not dupes, f"duplicate titles: {dupes}"

    # Soft signal, not a hard SERP cutoff — but worth flagging.
    long_ones = [(t, len(t)) for t in titles if len(t) > 65]
    if long_ones:
        print(f"\n  note: {len(long_ones)} title(s) over 65 chars, will truncate in SERPs")


def test_descriptions_are_present_and_not_the_site_default(post_pages):
    """Every post should have its own excerpt, not fall back to site.description."""
    generic = "Drawing the lines AI must follow"
    failures = []
    for url, path in post_pages.items():
        d = meta(soup_of(path), name="description")
        if not d:
            failures.append(f"{url}: no description")
        elif d.strip() == generic:
            failures.append(f"{url}: falling back to site.description — add an excerpt")
        elif len(d) < 50:
            failures.append(f"{url}: description only {len(d)} chars")
    assert not failures, "\n".join(failures)


# --------------------------------------------------------------------------
# 6. sitemap & robots
# --------------------------------------------------------------------------

def test_sitemap_covers_every_post(post_pages):
    sm = SITE_DIR / "sitemap.xml"
    assert sm.exists(), "sitemap.xml not built"
    xml = sm.read_text(encoding="utf-8")
    listed = {urlparse(loc).path for loc in re.findall(r"<loc>\s*(.*?)\s*</loc>", xml)}
    missing = [u for u in post_pages if u not in listed]
    assert not missing, f"posts absent from sitemap: {missing}"


def test_sitemap_urls_all_resolve_to_built_files(pages):
    sm = SITE_DIR / "sitemap.xml"
    if not sm.exists():
        pytest.skip("no sitemap")
    locs = re.findall(r"<loc>\s*(.*?)\s*</loc>", sm.read_text(encoding="utf-8"))
    assert locs, "sitemap has no <loc> entries"
    for loc in locs:
        path = urlparse(loc).path
        assert _resolves(pages, path), (
            f"sitemap lists {loc} but it was not built (404 risk)"
        )


def test_sitemap_lists_no_noindex_urls(pages):
    """Listing a noindex URL in the sitemap sends Google two contradictory
    signals: 'crawl this' and 'do not index this'. Paginated archives are the
    usual culprit -- they are generated from index.html, so they inherit
    nothing from its front matter."""
    sm = SITE_DIR / "sitemap.xml"
    if not sm.exists():
        pytest.skip("no sitemap")
    locs = re.findall(r"<loc>\s*(.*?)\s*</loc>", sm.read_text(encoding="utf-8"))
    offenders = []
    for loc in locs:
        path = _resolve(pages, urlparse(loc).path)
        if path is None:
            continue
        if "noindex" in (meta(soup_of(path), name="robots") or "").lower():
            offenders.append(loc)
    assert not offenders, f"sitemap lists noindex URLs: {offenders}"


def test_robots_txt_exists_and_declares_sitemap():
    r = SITE_DIR / "robots.txt"
    assert r.exists(), "no robots.txt"
    text = r.read_text(encoding="utf-8")
    declared = re.search(r"^Sitemap:\s*(\S+)$", text, re.MULTILINE)
    assert declared, "robots.txt does not declare the sitemap"
    assert declared.group(1).endswith("/sitemap.xml"), (
        f"robots.txt Sitemap line is {declared.group(1)!r}"
    )


AI_CRAWLERS = ["GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended"]


def test_ai_crawlers_are_not_blocked():
    """GEO depends on these having access. Fails loudly if someone
    pastes in a boilerplate robots.txt that blocks them."""
    r = SITE_DIR / "robots.txt"
    if not r.exists():
        pytest.skip("no robots.txt")
    text = r.read_text(encoding="utf-8")
    for agent in AI_CRAWLERS:
        block = re.search(
            rf"User-agent:\s*{re.escape(agent)}\s*\n((?:(?!User-agent:).*\n)*)",
            text, re.IGNORECASE,
        )
        if block and re.search(r"Disallow:\s*/\s*$", block.group(1), re.MULTILINE):
            pytest.fail(f"{agent} is disallowed — this blocks generative-engine citation")


# --------------------------------------------------------------------------
# 7. front matter discipline (source-level, not build output)
# --------------------------------------------------------------------------

@pytest.mark.xfail(
    reason="SEO/PLAN.md step 2.2: 1200x630 cards in images/og/ not produced yet. "
           "Flips to XPASS (and can lose the marker) once all 28 posts declare image:",
    strict=False,
)
def test_every_post_declares_an_image():
    """Without `image:` in front matter, og:image silently falls back to the
    default and every article shares one social card."""
    posts = glob.glob("_posts/*.md")
    if not posts:
        pytest.skip("_posts not found — run from repo root")
    missing = []
    for p in posts:
        head = Path(p).read_text(encoding="utf-8").split("---")[1]
        if not re.search(r"^image:\s*\S", head, re.MULTILINE):
            missing.append(Path(p).name)
    assert not missing, (
        f"{len(missing)} post(s) with no image: front matter:\n  "
        + "\n  ".join(missing)
    )


# --------------------------------------------------------------------------
# 8. internal links
# --------------------------------------------------------------------------

def test_no_broken_internal_links(pages):
    """Catches the /2026/slug/ → renamed-slug class of rot."""
    broken = []
    static = {
        p.relative_to(SITE_DIR).as_posix()
        for p in SITE_DIR.rglob("*") if p.is_file()
    }
    for url, path in pages.items():
        for a in soup_of(path).find_all("a", href=True):
            href = a["href"]
            if href.startswith(("http", "mailto:", "#", "//")):
                continue
            target = urlparse(href).path
            if not target.startswith("/"):
                continue
            if _resolves(pages, target):
                continue
            if target.lstrip("/") in static:
                continue
            if (target.lstrip("/") + "index.html") in static:
                continue
            broken.append(f"{url} → {href}")
    assert not broken, "broken internal links:\n  " + "\n  ".join(broken)
