import socket

def resolve_dns_and_reverse_lookup(domains):
    """
    Resolves DNS and performs reverse lookup for a list of domains.
    """
    results = []

    for domain in domains:
        try:
            ip = socket.gethostbyname(domain)  # DNS resolution
            try:
                reverse_lookup = socket.gethostbyaddr(ip)[0]  # Reverse lookup
            except socket.herror:
                reverse_lookup = None

            provider = identify_provider(reverse_lookup)
            results.append({
                "domain": domain,
                "ip": ip,
                "reverse_lookup": reverse_lookup,
                "provider": provider
            })
        except Exception as e:
            results.append({
                "domain": domain,
                "ip": None,
                "reverse_lookup": None,
                "provider": None,
                "error": str(e)
            })

    return results


def identify_provider(reverse_lookup):
    """
    Identifies the hosting provider based on reverse lookup results.
    """
    if reverse_lookup:
        reverse_lookup = reverse_lookup.lower()
        if "amazonaws" in reverse_lookup:
            return "AWS"
        elif "googleusercontent" in reverse_lookup or "storage.googleapis" in reverse_lookup:
            return "GCP"
        elif "blob.core.windows.net" in reverse_lookup or "azure" in reverse_lookup:
            return "Azure"
    return "Unknown"
