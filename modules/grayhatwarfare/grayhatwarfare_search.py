from modules.company_name.company_name_finder import find_company_name
import json
import requests

URL_PATTERN = "https://buckets.grayhatwarfare.com/files?keywords='{}'&page={}"


def html_data(url):
    """
    Fetch HTML content from the GrayHatWarfare bucket search URL.
    """
    try:
        response = requests.get(url)
        return response.text
    except Exception as e:
        print(f"Error fetching HTML data: {e}")
        return None


def extract_data_from_html(html_content):
    """
    Extract relevant bucket and file data from the HTML content.
    """
    try:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html_content, "html.parser")
        data = []

        table = soup.find("table", class_="table table-bordered")
        if table:
            headers = [th.get_text().strip() for th in table.find("thead").find_all("th")]
            headers.extend(["Bucket Link", "File Link"])

            for tr in table.find("tbody").find_all("tr"):
                td_data = [td.get_text().strip() for td in tr.find_all("td")]
                bucket_link = tr.find("a", class_="bucket-link")
                file_link = tr.find("a", id=lambda x: x and x.startswith("link_"))
                bucket_link_url = bucket_link["href"] if bucket_link else None
                file_link_url = file_link["href"] if file_link else None
                td_data.extend([bucket_link_url, file_link_url])
                data.append(dict(zip(headers, td_data)))
        else:
            return False

        return data
    except Exception as e:
        print(f"Error extracting data from HTML: {e}")
        return False


def perform_grayhatwarfare_search(domain, config_file=None):
    """
    Perform GrayHatWarfare search using the extracted company name.
    """
    company_name, full_title = find_company_name(domain, config_file)
    if not company_name:
        print("Failed to extract keywords for the domain.")
        return

    # Print the company details
    print(f"\nExtracted Company Details:")
    print(f"Company Name: {company_name}")
    print(f"Full Title: {full_title}\n")

    # Query GrayHatWarfare with the extracted keyword
    all_data = []
    page_number = 1
    while True:
        req_url = URL_PATTERN.format(company_name, page_number)
        html_content = html_data(req_url)
        if not html_content:
            break

        result = extract_data_from_html(html_content)
        if result is False:
            break

        all_data.extend(result)
        page_number += 1

    # Convert combined data to JSON and print it
    json_output = json.dumps(all_data, indent=4)
    print("\nGrayHatWarfare Results:")
    print(json_output)
    print("="*100)
    return all_data
