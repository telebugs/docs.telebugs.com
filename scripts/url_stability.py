#!/usr/bin/env python3
"""Capture and verify the public URL contract for docs.telebugs.com."""

from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote, urljoin, urlsplit


ORIGIN = "https://docs.telebugs.com"
SCHEMA_VERSION = 1
DEFAULT_BASELINE = "url-stability-baseline.json"
TEXT_SUFFIXES = {
    ".conf",
    ".css",
    ".hbs",
    ".html",
    ".js",
    ".json",
    ".md",
    ".txt",
    ".toml",
    ".xml",
}
DOCS_URL_RE = re.compile(
    r"https://docs\.telebugs\.com(?:/[^\s<>\"'`\\\[\]{}()]*)?"
)
CSS_URL_RE = re.compile(
    r"url\(\s*(?P<quote>['\"]?)(?P<url>.*?)(?P=quote)\s*\)", re.IGNORECASE
)
SITEMAP_LOC_RE = re.compile(
    r"<loc>\s*(?P<url>.*?)\s*</loc>", re.IGNORECASE | re.DOTALL
)
REDIRECT_RE = re.compile(
    r"location\s*=\s*(?P<source>\S+)\s*\{"
    r"(?P<body>.*?)"
    r"\}",
    re.DOTALL,
)
RETURN_RE = re.compile(
    r"return\s+(?P<status>30[1278])\s+(?P<target>[^;]+);"
)
HEADING_TAGS = {f"h{level}" for level in range(1, 7)}
RESOURCE_ATTRIBUTES = {
    "audio": ("src",),
    "embed": ("src",),
    "iframe": ("src",),
    "img": ("src", "srcset"),
    "input": ("src",),
    "object": ("data",),
    "script": ("src",),
    "source": ("src", "srcset"),
    "track": ("src",),
    "video": ("poster", "src"),
}


def sorted_unique(values: Iterable[str]) -> list[str]:
    return sorted(set(values))


def unique_dicts(values: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    serialized = {json.dumps(value, sort_keys=True): value for value in values}
    return [serialized[key] for key in sorted(serialized)]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def clean_docs_url(url: str) -> str:
    return url.rstrip(".,;:")


def split_srcset(value: str) -> list[str]:
    return [
        candidate.strip().split()[0]
        for candidate in value.split(",")
        if candidate.strip()
    ]


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.in_title = False
        self.current_heading: dict[str, Any] | None = None
        self.headings: list[dict[str, Any]] = []
        self.ids: list[str] = []
        self.anchors: list[str] = []
        self.resources: list[dict[str, str]] = []
        self.metas: list[dict[str, str]] = []
        self.canonicals: list[str] = []

    def handle_starttag(
        self, tag: str, attributes: list[tuple[str, str | None]]
    ) -> None:
        tag = tag.lower()
        attrs = {key.lower(): value or "" for key, value in attributes}

        if attrs.get("id"):
            self.ids.append(attrs["id"])

        if tag == "title":
            self.in_title = True

        if tag in HEADING_TAGS:
            self.current_heading = {
                "level": int(tag[1]),
                "id": attrs.get("id", ""),
                "text_parts": [],
            }

        if tag == "a" and "href" in attrs:
            self.anchors.append(attrs["href"])

        if tag == "form" and attrs.get("action"):
            self.anchors.append(attrs["action"])

        if tag == "meta":
            self.metas.append(dict(sorted(attrs.items())))

        if tag == "link":
            relations = {value.lower() for value in attrs.get("rel", "").split()}
            if "canonical" in relations and attrs.get("href"):
                self.canonicals.append(attrs["href"])
            elif attrs.get("href"):
                self.resources.append(
                    {"tag": tag, "attribute": "href", "url": attrs["href"]}
                )

        for attribute in RESOURCE_ATTRIBUTES.get(tag, ()):
            value = attrs.get(attribute)
            if not value:
                continue
            urls = split_srcset(value) if attribute == "srcset" else [value]
            for url in urls:
                self.resources.append(
                    {"tag": tag, "attribute": attribute, "url": url}
                )

    def handle_startendtag(
        self, tag: str, attributes: list[tuple[str, str | None]]
    ) -> None:
        self.handle_starttag(tag, attributes)

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)
        if self.current_heading is not None:
            self.current_heading["text_parts"].append(data)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self.in_title = False
        if tag in HEADING_TAGS and self.current_heading is not None:
            heading = self.current_heading
            self.headings.append(
                {
                    "level": heading["level"],
                    "id": heading["id"],
                    "text": " ".join(
                        "".join(heading["text_parts"]).split()
                    ),
                }
            )
            self.current_heading = None

    @property
    def title(self) -> str:
        return " ".join("".join(self.title_parts).split())


def parse_page(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    parser.close()
    return parser


def public_url_path(relative_path: str) -> str:
    return "/" + relative_path


def resolve_internal_url(
    raw_url: str, source_path: str
) -> dict[str, str] | None:
    raw_url = raw_url.strip()
    if not raw_url:
        raw_url = public_url_path(source_path)

    split = urlsplit(raw_url)
    if split.scheme.lower() in {"data", "javascript", "mailto", "tel"}:
        return None
    if split.scheme and split.scheme.lower() not in {"http", "https"}:
        return None
    if split.netloc and split.netloc.lower() != "docs.telebugs.com":
        return None

    base = f"{ORIGIN}/{source_path}"
    resolved = urlsplit(urljoin(base, raw_url))
    if resolved.netloc.lower() != "docs.telebugs.com":
        return None

    decoded_path = unquote(resolved.path)
    had_trailing_slash = decoded_path.endswith("/")
    normalized_path = posixpath.normpath(decoded_path)
    if normalized_path in {".", "/"}:
        normalized_path = ""
    else:
        normalized_path = normalized_path.lstrip("/")
    if had_trailing_slash and normalized_path:
        normalized_path += "/"

    return {
        "raw": raw_url,
        "target_path": normalized_path,
        "target_fragment": unquote(resolved.fragment),
    }


def parse_redirects(server_path: Path) -> list[dict[str, Any]]:
    server_text = server_path.read_text(encoding="utf-8")
    redirects: list[dict[str, Any]] = []
    for location in REDIRECT_RE.finditer(server_text):
        returned = RETURN_RE.search(location.group("body"))
        if returned is None:
            continue
        redirects.append(
            {
                "source": location.group("source"),
                "status": int(returned.group("status")),
                "target": returned.group("target").strip(),
            }
        )
    return sorted(redirects, key=lambda redirect: redirect["source"])


def iter_inventory_text_files(root: Path, public_dir: Path) -> Iterable[Path]:
    roots = [root / "src", public_dir, root / "theme", root / "config"]
    for candidate_root in roots:
        if not candidate_root.exists():
            continue
        for path in candidate_root.rglob("*"):
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
                yield path
    for name in ("README.md", "book.toml"):
        path = root / name
        if path.is_file():
            yield path


def scan_absolute_docs_links(
    root: Path, public_dir: Path
) -> list[dict[str, str]]:
    links: list[dict[str, str]] = []
    for path in iter_inventory_text_files(root, public_dir):
        text = path.read_text(encoding="utf-8", errors="ignore")
        try:
            display_path = path.relative_to(root).as_posix()
        except ValueError:
            display_path = (
                Path("public") / path.relative_to(public_dir)
            ).as_posix()
        for match in DOCS_URL_RE.finditer(text):
            links.append(
                {"file": display_path, "url": clean_docs_url(match.group(0))}
            )
    return unique_dicts(links)


def robots_directives(parser: PageParser) -> list[dict[str, str]]:
    directives: list[dict[str, str]] = []
    for meta in parser.metas:
        name = meta.get("name", "").lower()
        if name in {"robots", "googlebot", "bingbot"}:
            directives.append(
                {"agent": name, "content": meta.get("content", "")}
            )
    return unique_dicts(directives)


def page_metadata(parser: PageParser) -> dict[str, Any]:
    descriptions = [
        meta.get("content", "")
        for meta in parser.metas
        if meta.get("name", "").lower() == "description"
    ]
    open_graph = [
        {
            "property": meta.get("property", ""),
            "content": meta.get("content", ""),
        }
        for meta in parser.metas
        if meta.get("property", "").lower().startswith("og:")
    ]
    return {
        "title": parser.title,
        "descriptions": descriptions,
        "canonicals": sorted_unique(parser.canonicals),
        "open_graph": unique_dicts(open_graph),
        "robots": robots_directives(parser),
        "meta_tags": unique_dicts(parser.metas),
    }


def capture_inventory(
    root: Path, public_dir: Path, server_path: Path
) -> dict[str, Any]:
    if not public_dir.is_dir():
        raise FileNotFoundError(f"Public directory does not exist: {public_dir}")
    if not server_path.is_file():
        raise FileNotFoundError(f"Server config does not exist: {server_path}")

    public_paths = sorted(
        path.relative_to(public_dir).as_posix()
        for path in public_dir.rglob("*")
        if path.is_file() and path.name != ".DS_Store"
    )
    html_paths = [path for path in public_paths if path.endswith(".html")]
    pages: dict[str, Any] = {}
    fragment_links: list[dict[str, str]] = []

    for relative_path in html_paths:
        parser = parse_page(public_dir / relative_path)
        internal_links = [
            resolved
            for raw_url in parser.anchors
            if (resolved := resolve_internal_url(raw_url, relative_path))
            is not None
        ]
        resources = [
            {
                **resource,
                **resolved,
            }
            for resource in parser.resources
            if (
                resolved := resolve_internal_url(
                    resource["url"], relative_path
                )
            )
            is not None
        ]
        page_fragment_links = [
            {
                "source_path": relative_path,
                **link,
            }
            for link in internal_links
            if link["target_fragment"]
        ]
        fragment_links.extend(page_fragment_links)
        pages[relative_path] = {
            "ids": sorted_unique(parser.ids),
            "headings": parser.headings,
            "internal_links": unique_dicts(internal_links),
            "resources": unique_dicts(resources),
            "metadata": page_metadata(parser),
        }

    css_resources: list[dict[str, str]] = []
    for relative_path in public_paths:
        if not relative_path.endswith(".css"):
            continue
        text = (public_dir / relative_path).read_text(
            encoding="utf-8", errors="replace"
        )
        for match in CSS_URL_RE.finditer(text):
            raw_url = match.group("url")
            resolved = resolve_internal_url(raw_url, relative_path)
            if resolved is not None:
                css_resources.append(
                    {"source_path": relative_path, **resolved}
                )

    absolute_docs_links = scan_absolute_docs_links(root, public_dir)
    absolute_docs_urls = sorted_unique(
        link["url"] for link in absolute_docs_links
    )
    problem_type_urls = [
        url
        for url in absolute_docs_urls
        if url.startswith(f"{ORIGIN}/rest-api/problems/")
        and url != f"{ORIGIN}/rest-api/problems/index.html"
    ]
    noindex_pages = sorted(
        relative_path
        for relative_path, page in pages.items()
        if any(
            "noindex"
            in {
                token.strip().lower()
                for token in directive["content"].split(",")
            }
            for directive in page["metadata"]["robots"]
        )
    )

    robots_files = []
    sitemap_files = []
    for relative_path in public_paths:
        lower_name = Path(relative_path).name.lower()
        if lower_name == "robots.txt":
            robots_files.append(
                {
                    "path": relative_path,
                    "sha256": sha256(public_dir / relative_path),
                    "content": (public_dir / relative_path).read_text(
                        encoding="utf-8", errors="replace"
                    ),
                }
            )
        if lower_name.startswith("sitemap"):
            sitemap_text = (public_dir / relative_path).read_text(
                encoding="utf-8", errors="replace"
            )
            sitemap_files.append(
                {
                    "path": relative_path,
                    "sha256": sha256(public_dir / relative_path),
                    "urls": sorted_unique(
                        match.group("url").strip()
                        for match in SITEMAP_LOC_RE.finditer(sitemap_text)
                    ),
                }
            )

    return {
        "schema_version": SCHEMA_VERSION,
        "origin": ORIGIN,
        "counts": {
            "html_paths": len(html_paths),
            "public_paths": len(public_paths),
            "redirects": len(parse_redirects(server_path)),
            "internal_links": sum(
                len(page["internal_links"]) for page in pages.values()
            ),
            "heading_ids": sum(
                1
                for page in pages.values()
                for heading in page["headings"]
                if heading["id"]
            ),
            "fragment_links": len(unique_dicts(fragment_links)),
            "absolute_docs_links": len(absolute_docs_links),
            "problem_type_urls": len(problem_type_urls),
        },
        "html_paths": html_paths,
        "public_paths": public_paths,
        "redirects": parse_redirects(server_path),
        "pages": pages,
        "fragment_links": unique_dicts(fragment_links),
        "css_resources": unique_dicts(css_resources),
        "absolute_docs_links": absolute_docs_links,
        "problem_type_urls": problem_type_urls,
        "problem_html_paths": [
            path
            for path in html_paths
            if path.startswith("rest-api/problems/")
        ],
        "seo": {
            "noindex_pages": noindex_pages,
            "robots_files": robots_files,
            "sitemap_files": sitemap_files,
        },
    }


def redirect_map(redirects: list[dict[str, Any]]) -> dict[str, str]:
    return {
        redirect["source"].lstrip("/"): redirect["target"]
        for redirect in redirects
    }


def find_public_target(
    target_path: str,
    public_paths: set[str],
    redirects: dict[str, str],
) -> str | None:
    target_path = target_path.lstrip("/")
    seen: set[str] = set()
    while target_path in redirects and target_path not in seen:
        seen.add(target_path)
        target_path = urlsplit(redirects[target_path]).path.lstrip("/")

    candidates = []
    if not target_path:
        candidates.append("index.html")
    elif target_path.endswith("/"):
        candidates.append(target_path + "index.html")
    else:
        candidates.extend(
            [target_path, target_path + ".html", target_path + "/index.html"]
        )
    return next(
        (candidate for candidate in candidates if candidate in public_paths),
        None,
    )


def canonical_errors(inventory: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    public_paths = set(inventory["public_paths"])
    redirects = redirect_map(inventory["redirects"])
    for page_path, page in inventory["pages"].items():
        for canonical in page["metadata"]["canonicals"]:
            split = urlsplit(canonical)
            if split.netloc and split.netloc.lower() != "docs.telebugs.com":
                errors.append(
                    f"{page_path}: canonical points outside docs.telebugs.com: "
                    f"{canonical}"
                )
                continue
            resolved = resolve_internal_url(canonical, page_path)
            if resolved is None:
                continue
            if (
                find_public_target(
                    resolved["target_path"], public_paths, redirects
                )
                is None
            ):
                errors.append(
                    f"{page_path}: canonical target does not exist: {canonical}"
                )
    return errors


def redirect_errors(inventory: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    public_paths = set(inventory["public_paths"])
    redirects = redirect_map(inventory["redirects"])
    for redirect in inventory["redirects"]:
        resolved = resolve_internal_url(
            redirect["target"], redirect["source"].lstrip("/")
        )
        if resolved is None:
            continue
        target = find_public_target(
            resolved["target_path"], public_paths, redirects
        )
        if target is None:
            errors.append(
                "Broken nginx redirect target: "
                f"{redirect['source']} -> {redirect['target']}"
            )
            continue
        fragment = resolved["target_fragment"]
        if (
            fragment
            and fragment not in set(inventory["pages"].get(target, {}).get("ids", []))
        ):
            errors.append(
                "Broken nginx redirect fragment: "
                f"{redirect['source']} -> {redirect['target']}"
            )
    return errors


def seo_errors(inventory: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    public_paths = set(inventory["public_paths"])
    redirects = redirect_map(inventory["redirects"])

    for robots_file in inventory["seo"]["robots_files"]:
        for line in robots_file["content"].splitlines():
            directive, separator, value = line.partition(":")
            if (
                separator
                and directive.strip().lower() == "disallow"
                and value.strip()
            ):
                errors.append(
                    f"{robots_file['path']}: crawl-blocking robots directive: "
                    f"{line.strip()}"
                )

    sitemap_urls: list[str] = []
    for sitemap_file in inventory["seo"]["sitemap_files"]:
        urls = sitemap_file.get("urls", [])
        sitemap_urls.extend(urls)
        for url in urls:
            split = urlsplit(url)
            if split.netloc.lower() != "docs.telebugs.com":
                errors.append(
                    f"{sitemap_file['path']}: sitemap URL points outside "
                    f"docs.telebugs.com: {url}"
                )
                continue
            resolved = resolve_internal_url(url, sitemap_file["path"])
            if (
                resolved is None
                or find_public_target(
                    resolved["target_path"], public_paths, redirects
                )
                is None
            ):
                errors.append(
                    f"{sitemap_file['path']}: sitemap URL does not exist: {url}"
                )

    if sitemap_urls:
        expected_paths = sorted(
            path
            for path in inventory["html_paths"]
            if path not in {"404.html", "print.html", "toc.html", "up.html"}
        )
        expected_urls = {f"{ORIGIN}/{path}" for path in expected_paths}
        actual_urls = set(sitemap_urls)
        for url in sorted(expected_urls - actual_urls):
            errors.append(f"Documentation URL missing from sitemap: {url}")
        for path in inventory["seo"]["noindex_pages"]:
            url = f"{ORIGIN}/{path}"
            if url in actual_urls:
                errors.append(f"Noindex URL included in sitemap: {url}")

    return errors


def link_errors(inventory: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    public_paths = set(inventory["public_paths"])
    redirects = redirect_map(inventory["redirects"])
    pages = inventory["pages"]

    references: list[tuple[str, dict[str, str], str]] = []
    for page_path, page in pages.items():
        references.extend(
            (page_path, link, "link") for link in page["internal_links"]
        )
        references.extend(
            (page_path, resource, "resource")
            for resource in page["resources"]
        )
    references.extend(
        (resource["source_path"], resource, "CSS resource")
        for resource in inventory["css_resources"]
    )

    for source_path, reference, kind in references:
        target = find_public_target(
            reference["target_path"], public_paths, redirects
        )
        if target is None:
            errors.append(
                f"{source_path}: broken internal {kind}: {reference['raw']}"
            )
            continue
        fragment = reference.get("target_fragment", "")
        if fragment and target.endswith(".html"):
            target_ids = set(pages.get(target, {}).get("ids", []))
            if fragment not in target_ids:
                errors.append(
                    f"{source_path}: missing fragment #{fragment} in {target} "
                    f"(from {reference['raw']})"
                )
    return errors


def baseline_contract_errors(
    baseline: dict[str, Any], current: dict[str, Any]
) -> list[str]:
    errors: list[str] = []
    current_html = set(current["html_paths"])
    current_public = set(current["public_paths"])

    for path in baseline["html_paths"]:
        if path not in current_html:
            errors.append(f"Missing baseline HTML URL: /{path}")

    for path in baseline["public_paths"]:
        if path not in current_public:
            errors.append(f"Missing baseline public asset: /{path}")

    current_redirects = {
        (
            redirect["source"],
            redirect["status"],
            redirect["target"],
        )
        for redirect in current["redirects"]
    }
    for redirect in baseline["redirects"]:
        signature = (
            redirect["source"],
            redirect["status"],
            redirect["target"],
        )
        if signature not in current_redirects:
            errors.append(
                "Missing or changed nginx redirect: "
                f"{redirect['source']} -> {redirect['target']} "
                f"({redirect['status']})"
            )

    for path, baseline_page in baseline["pages"].items():
        current_page = current["pages"].get(path)
        if current_page is None:
            continue
        current_heading_ids = {
            heading["id"]
            for heading in current_page["headings"]
            if heading["id"]
        }
        for heading in baseline_page["headings"]:
            heading_id = heading["id"]
            if heading_id and heading_id not in current_heading_ids:
                errors.append(
                    f"Missing baseline heading fragment: /{path}#{heading_id}"
                )

    for fragment_link in baseline["fragment_links"]:
        target = find_public_target(
            fragment_link["target_path"],
            current_public,
            redirect_map(current["redirects"]),
        )
        if target is None:
            continue
        fragment = fragment_link["target_fragment"]
        target_ids = set(current["pages"].get(target, {}).get("ids", []))
        if fragment and fragment not in target_ids:
            errors.append(
                "Missing baseline linked fragment: "
                f"/{target}#{fragment} "
                f"(linked from /{fragment_link['source_path']})"
            )

    if baseline["problem_type_urls"] != current["problem_type_urls"]:
        errors.append(
            "REST API problem-type URLs changed: "
            f"expected {baseline['problem_type_urls']}, "
            f"found {current['problem_type_urls']}"
        )

    baseline_noindex = set(baseline["seo"]["noindex_pages"])
    for path in sorted(set(current["seo"]["noindex_pages"]) - baseline_noindex):
        errors.append(f"Unexpected noindex directive: /{path}")

    return errors


def print_summary(
    inventory: dict[str, Any],
    *,
    baseline_html_count: int | None = None,
    errors: list[str] | None = None,
) -> None:
    counts = inventory["counts"]
    if baseline_html_count is not None:
        print(f"HTML URLs before: {baseline_html_count}")
        print(f"HTML URLs after:  {counts['html_paths']}")
    else:
        print(f"HTML URLs: {counts['html_paths']}")
    print(f"Public files: {counts['public_paths']}")
    print(f"Nginx redirects: {counts['redirects']}")
    print(f"Internal links: {counts['internal_links']}")
    print(f"Heading IDs: {counts['heading_ids']}")
    print(f"Fragment links: {counts['fragment_links']}")
    print(f"Absolute docs.telebugs.com links: {counts['absolute_docs_links']}")
    print(f"REST API problem-type URLs: {counts['problem_type_urls']}")
    print(
        "Canonical links: "
        + str(
            sum(
                len(page["metadata"]["canonicals"])
                for page in inventory["pages"].values()
            )
        )
    )
    print(f"Pages with noindex: {len(inventory['seo']['noindex_pages'])}")
    print(f"Robots files: {len(inventory['seo']['robots_files'])}")
    print(f"Sitemap files: {len(inventory['seo']['sitemap_files'])}")
    if errors is not None:
        print(f"Failures: {len(errors)}")


def load_baseline(path: Path) -> dict[str, Any]:
    baseline = json.loads(path.read_text(encoding="utf-8"))
    if baseline.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(
            f"Unsupported baseline schema: {baseline.get('schema_version')}"
        )
    if baseline.get("origin") != ORIGIN:
        raise ValueError(f"Unexpected baseline origin: {baseline.get('origin')}")
    return baseline


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("capture", "check"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument(
            "--root",
            type=Path,
            default=Path(__file__).resolve().parent.parent,
        )
        subparser.add_argument("--public", type=Path)
        subparser.add_argument("--server", type=Path)
        subparser.add_argument("--baseline", type=Path)
    args = parser.parse_args()

    root = args.root.resolve()
    public_dir = (
        args.public.resolve() if args.public else root / "public"
    )
    server_path = (
        args.server.resolve()
        if args.server
        else root / "config" / "server.conf"
    )
    baseline_path = (
        args.baseline.resolve()
        if args.baseline
        else root / DEFAULT_BASELINE
    )

    inventory = capture_inventory(root, public_dir, server_path)
    crawl_failures = (
        link_errors(inventory)
        + redirect_errors(inventory)
        + canonical_errors(inventory)
        + seo_errors(inventory)
    )

    if args.command == "capture":
        baseline_path.write_text(
            json.dumps(inventory, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(f"Captured URL baseline: {baseline_path}")
        print_summary(inventory, errors=crawl_failures)
        if crawl_failures:
            for failure in crawl_failures:
                print(f"ERROR: {failure}", file=sys.stderr)
            return 1
        return 0

    if not baseline_path.is_file():
        print(f"Baseline does not exist: {baseline_path}", file=sys.stderr)
        return 2
    baseline = load_baseline(baseline_path)
    failures = (
        baseline_contract_errors(baseline, inventory) + crawl_failures
    )
    failures = sorted_unique(failures)
    print_summary(
        inventory,
        baseline_html_count=baseline["counts"]["html_paths"],
        errors=failures,
    )
    if failures:
        for failure in failures:
            print(f"ERROR: {failure}", file=sys.stderr)
        return 1
    print("URL stability check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
