from interface_db.retrieval.crossref_search import build_url, normalize_item


def test_build_url_encodes_query_and_filter() -> None:
    url = build_url("dynamic surface tension", 5, 2020)
    assert "dynamic+surface+tension" in url
    assert "from-pub-date%3A2020-01-01" in url


def test_normalize_item_keeps_retrieval_fields() -> None:
    item = {
        "DOI": "10.1000/example",
        "title": ["Example"],
        "author": [{"given": "Ada", "family": "Lovelace"}],
        "published": {"date-parts": [[2026, 1, 2]]},
        "container-title": ["Journal"],
        "URL": "https://doi.org/10.1000/example",
        "type": "journal-article",
    }
    assert normalize_item(item)["authors"] == ["Ada Lovelace"]
    assert normalize_item(item)["year"] == 2026
