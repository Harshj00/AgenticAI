import requests

DUCKDUCKGO_URL = "https://api.duckduckgo.com/"


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
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        abstract = data.get("AbstractText", "").strip()
        related = data.get("RelatedTopics", [])

        if abstract:
            return f"Search result for '{query}': {abstract}"

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

        return f"No direct answer found for '{query}'."
    except Exception as e:
        return {"error": f"Search error: {e}"}


if __name__ == "__main__":
    print(execute({"query": "Python programming"}))
