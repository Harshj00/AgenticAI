import requests
import re
import html

DUCKDUCKGO_URL = "https://api.duckduckgo.com/"


def _strip_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text)


def execute(arguments: dict):
    query = arguments.get("query") or arguments.get("q") or arguments.get("search")
    if not query:
        return {"error": "Web search requires a query parameter."}

    if not isinstance(query, str):
        query = str(query)

    try:
        response = requests.get(
            DUCKDUCKGO_URL,
            params={
                "q": query,
                "format": "json",
                "no_html": "1",
                "skip_disambig": "1",
            },
            headers={"User-Agent": "AgenticAI/1.0 (+https://github.com/Harshj00/AgenticAI)"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        abstract = data.get("AbstractText", "").strip()
        answer = data.get("Answer", "").strip()
        definition = data.get("Definition", "").strip()
        definition_source = data.get("DefinitionSource", "").strip()
        related = data.get("RelatedTopics", [])

        if answer:
            return f"Search answer for '{query}': {answer}"

        if abstract:
            return f"Search result for '{query}': {abstract}"

        if definition:
            label = f" ({definition_source})" if definition_source else ""
            return f"Search definition for '{query}': {definition}{label}"

        snippets = []
        for item in related:
            if isinstance(item, dict):
                text = item.get("Text")
                if text:
                    snippets.append(text)
            elif isinstance(item, list):
                for nested in item:
                    if isinstance(nested, dict):
                        nested_text = nested.get("Text")
                        if nested_text:
                            snippets.append(nested_text)
            if len(snippets) >= 3:
                break

        if snippets:
            return f"Search results for '{query}': " + " | ".join(snippets[:3])

        # Fallback: fetch DuckDuckGo HTML search and extract snippets
        try:
            html_resp = requests.get(
                "https://html.duckduckgo.com/html",
                params={"q": query},
                headers={"User-Agent": "AgenticAI/1.0 (+https://github.com/Harshj00/AgenticAI)"},
                timeout=10,
            )
            html_resp.raise_for_status()
            page = html_resp.text

            # try to extract snippet blocks
            snippet_matches = re.findall(r'<div[^>]+class="result__snippet"[^>]*>(.*?)</div>', page, flags=re.S)
            results = []
            if snippet_matches:
                for s in snippet_matches:
                    clean = html.unescape(_strip_tags(s)).strip()
                    if clean:
                        results.append(clean)
                    if len(results) >= 3:
                        break

            # fallback to titles if snippets not found
            if not results:
                title_matches = re.findall(r'<a[^>]+class="result__a"[^>]*>(.*?)</a>', page, flags=re.S)
                for t in title_matches:
                    clean = html.unescape(_strip_tags(t)).strip()
                    if clean:
                        results.append(clean)
                    if len(results) >= 3:
                        break

            if results:
                return f"Search results for '{query}': " + " | ".join(results[:3])
        except Exception:
            pass

        # Fallback: try Wikipedia search API for a likely answer/snippet
        try:
            wiki_resp = requests.get(
                "https://en.wikipedia.org/w/api.php",
                params={
                    "action": "query",
                    "list": "search",
                    "srsearch": query,
                    "utf8": 1,
                    "format": "json",
                    "srlimit": 3,
                },
                headers={"User-Agent": "AgenticAI/1.0 (+https://github.com/Harshj00/AgenticAI)"},
                timeout=10,
            )
            wiki_resp.raise_for_status()
            wiki_data = wiki_resp.json()
            search = wiki_data.get("query", {}).get("search", [])
            wiki_results = []
            for item in search:
                title = item.get("title")
                snippet = item.get("snippet")
                if snippet:
                    clean = html.unescape(_strip_tags(snippet)).strip()
                    if title:
                        wiki_results.append(f"{title}: {clean}")
                    else:
                        wiki_results.append(clean)
                if len(wiki_results) >= 3:
                    break

            if wiki_results:
                return f"Search results for '{query}': " + " | ".join(wiki_results[:3])
        except Exception:
            pass

        return f"No direct answer found for '{query}'."
    except Exception as e:
        return {"error": f"Search error: {e}"}


if __name__ == "__main__":
    print(execute({"query": "Python programming"}))
