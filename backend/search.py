try:
    from ddgs import DDGS
except Exception:
    # Fall back to older package name if `ddgs` isn't installed
    from duckduckgo_search import DDGS


def search_web(query):
    with DDGS() as ddgs:
        results = list(
            ddgs.text(
                query,
                max_results=5
            )
        )

    return results