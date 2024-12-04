from bs4 import BeautifulSoup
import requests
import json


def load_config(config_file):
    """
    Load API key and CSE ID from a given config file.
    """
    try:
        with open(config_file, "r") as file:
            config = json.load(file)
            api_key = config.get("api_key")
            cse_id = config.get("cse_id")
            if not api_key or not cse_id:
                print("Invalid config file: Missing 'api_key' or 'cse_id'.")
                return None, None
            return api_key, cse_id
    except Exception as e:
        print(f"Error loading config file: {e}")
        return None, None


def google_search(query, api_key, cse_id, **kwargs):
    """
    Perform a Google search using the Custom Search JSON API.
    """
    try:
        from googleapiclient.discovery import build

        service = build("customsearch", "v1", developerKey=api_key)
        results = service.cse().list(q=query, cx=cse_id, **kwargs).execute()
        return results.get("items", [])
    except Exception as e:
        print(f"Error during Google search: {e}")
        return []


def google_scrape(domain):
    """
    Scrape Google search results to find keywords (company name).
    """
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )
        }
        response = requests.get(f"https://www.google.com/search?q={domain}+crunchbase", headers=headers)

        # Parse the HTML content of the search results page
        soup = BeautifulSoup(response.text, "html.parser")
        result = soup.find("h3")  # Find the first title from search results

        if result:
            full_title = result.text
            return extract_keyword(full_title), full_title
        else:
            return None, None
    except Exception as e:
        print(f"Error during Google scraping: {e}")
        return None, None


def extract_keyword(full_title):
    """
    Extract the most relevant keyword (company name) from the title.
    """
    special_characters = "—–!@#$%^&*()_+{}[]:;<>,.?/~\\|-"
    for letter in full_title:
        if letter in special_characters:
            if full_title[full_title.index(letter) - 1] == " ":
                return full_title.split(f" {letter}")[0]
            else:
                return full_title.split(letter)[0]
    return full_title


def find_company_name(domain, config_file=None):
    """
    Find the company name using Google Custom Search API or scraping.
    """
    if config_file:
        api_key, cse_id = load_config(config_file)
        if api_key and cse_id:
            # Use the API method
            print(f"Used API method to find company name for: {domain}")
            search_results = google_search(f"{domain} crunchbase", api_key, cse_id)
            if search_results:
                full_title = search_results[0]["title"]
                return extract_keyword(full_title), full_title
            else:
                print("No results found when used API.")
        else:
            print("Invalid API configuration. Falling back to scraping.")

    # Fallback to scraping
    print(f"Used scraping method to find company name for: {domain}")
    return google_scrape(domain)
