import urllib.parse
WEBSITES = {
    "facebook": "https://www.facebook.com",
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "twitter": "https://www.twitter.com",
    "instagram": "https://www.instagram.com",
    "linkedin": "https://www.linkedin.com",
    "amazon": "https://www.amazon.in",
    "wikipedia": "https://www.wikipedia.com",
}
def search_website(query, specific_site=None):
    if specific_site:
        base_url = WEBSITES.get(specific_site.lower())
        if base_url:
            search_paths = {
                "youtube": f"/results?search_query={urllib.parse.quote(query)}",
                "amazon": f"/s?k={urllib.parse.quote(query)}",
                "wikipedia": f"/w/index.php?search={urllib.parse.quote(query)}"
            }
            return base_url + search_paths.get(specific_site.lower(), f"/search?q={urllib.parse.quote(query)}")
        return None

    return WEBSITES.get(query.lower()) or f"https://www.google.com/search?q={urllib.parse.quote(query)}"