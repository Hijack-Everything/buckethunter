import requests
from concurrent.futures import ThreadPoolExecutor

def generate_storage_urls(targets):
    """
    Generate potential storage URLs for AWS, GCP, and Azure based on domain/subdomains.
    """
    urls = []
    for target in targets:
        # AWS Patterns
        urls.append((f"https://{target}.s3.amazonaws.com", "AWS"))
        urls.append((f"https://{target}-s3.amazonaws.com", "AWS"))
        urls.append((f"http://{target}.s3.amazonaws.com", "AWS"))
        urls.append((f"http://{target}-s3.amazonaws.com", "AWS"))

        # GCP Patterns
        urls.append((f"https://{target}.storage.googleapis.com", "GCP"))
        urls.append((f"https://{target}-storage.googleapis.com", "GCP"))
        urls.append((f"http://{target}.storage.googleapis.com", "GCP"))
        urls.append((f"http://{target}-storage.googleapis.com", "GCP"))

        # Azure Patterns
        urls.append((f"https://{target}.blob.core.windows.net", "Azure"))
        urls.append((f"https://{target}-blob.core.windows.net", "Azure"))
        urls.append((f"http://{target}.blob.core.windows.net", "Azure"))
        urls.append((f"http://{target}-blob.core.windows.net", "Azure"))

    return urls


def scan_url(url_data):
    """
    Scan a single storage URL.
    Returns the URL and provider if the URL exists.
    """
    url, provider = url_data
    try:
        response = requests.head(url, timeout=5)
        if response.status_code in [200, 403]:  # Exists or access restricted
            return url, provider
    except requests.RequestException:
        pass
    return None, None


def scan_storage(domain, subdomains, scan_subdomains, threads=50):
    """
    Scan for cloud storage buckets using multithreading.
    """
    if scan_subdomains:
        print(f"Scanning for cloud storage buckets for {domain} and subdomains...")
        targets = [domain] + subdomains
    else:
        print(f"Scanning for cloud storage buckets for {domain} only...")
        targets = [domain]

    # Generate all potential URLs for AWS, GCP, and Azure
    urls = generate_storage_urls(targets)

    # Scan URLs using multithreading
    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = list(executor.map(scan_url, urls))

    # Collect results by provider
    aws_buckets = [url for url, provider in results if provider == "AWS"]
    gcp_buckets = [url for url, provider in results if provider == "GCP"]
    azure_buckets = [url for url, provider in results if provider == "Azure"]

    # Print results
    print("\nAWS Buckets Found:")
    for bucket in aws_buckets:
        print(bucket)
        pass

    print("\nGCP Buckets Found:")
    for bucket in gcp_buckets:
        print(bucket)
        pass

    print("\nAzure Buckets Found:")
    for bucket in azure_buckets:
        print(bucket)
        pass
    print("="*100)


    return aws_buckets, gcp_buckets, azure_buckets
