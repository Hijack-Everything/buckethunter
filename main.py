import argparse
import json
from modules.analyzers.domain_analyzer import analyze_domain
from modules.scanners.storage_scanner import scan_storage
from modules.grayhatwarfare.grayhatwarfare_search import perform_grayhatwarfare_search
from modules.company_name.company_name_finder import find_company_name
def display_logo():
    print("="*100)
    logo = r"""
····································································
: ________  ___  ___  ________  ___  __    _______  _________      :
:|\   __  \|\  \|\  \|\   ____\|\  \|\  \ |\  ___ \|\___   ___\    :
:\ \  \|\ /\ \  \\\  \ \  \___|\ \  \/  /|\ \   __/\|___ \  \_|    :
: \ \   __  \ \  \\\  \ \  \    \ \   ___  \ \  \_|/__  \ \  \     :
:  \ \  \|\  \ \  \\\  \ \  \____\ \  \\ \  \ \  \_|\ \  \ \  \    :
:   \ \_______\ \_______\ \_______\ \__\\ \__\ \_______\  \ \__\   :
:    \|_______|\|_______|\|_______|\|__| \|__|\|_______|   \|__|   :
:                                                                  :
:                                                                  :
:                                                                  :
: ___  ___  ___  ___  ________   _________  _______   ________     :
:|\  \|\  \|\  \|\  \|\   ___  \|\___   ___\\  ___ \ |\   __  \    :
:\ \  \\\  \ \  \\\  \ \  \\ \  \|___ \  \_\ \   __/|\ \  \|\  \   :
: \ \   __  \ \  \\\  \ \  \\ \  \   \ \  \ \ \  \_|/_\ \   _  _\  :
:  \ \  \ \  \ \  \\\  \ \  \\ \  \   \ \  \ \ \  \_|\ \ \  \\  \| :
:   \ \__\ \__\ \_______\ \__\\ \__\   \ \__\ \ \_______\ \__\\ _\ :
:    \|__|\|__|\|_______|\|__| \|__|    \|__|  \|_______|\|__|\|__|:
····································································
    """
    defination= r'''Made by Suman Kumar Chakraborty'''
    print(logo)
    print(defination)
    print("="*100)





def main():
    """
    BucketHunter: Discover cloud buckets provided domains and subdomains.
    """
    
    parser = argparse.ArgumentParser(description="BucketHunter: Discover cloud buckets and analyze domains.")
    
    # Arguments
    parser.add_argument("-d", "--domain", help="Analyze a single domain.")
    parser.add_argument("-l", "--list", help="Path to a file containing a list of domains and subdomains.")
    parser.add_argument("-g", "--grayhatwarfare", action="store_true", help="Enable GrayHatWarfare search.(Might give false positives but sometimes can give a gold mine)")
    parser.add_argument("-a", "--all", action="store_true", help="Perform all actions.")
    parser.add_argument("-cf", "--config-file", type=str, help="Path to the config file for API keys.")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of threads to use (default: 100).")
    parser.add_argument("-o", "--output", help="Path to the output JSON file to store results.")

    args = parser.parse_args()

    # Ensure either -d or -l is provided
    if not args.domain and not args.list:
        print("Error: Please provide either a domain (-d) or a list of domains (-l).")
        return

    threads = args.threads
    unique_keywords = set()  # To store unique company names for GrayHatWarfare search
    results = []  # To store results for output

    # Analyze a single domain
    if args.domain:
        print(f"\nAnalyzing single domain: {args.domain}")
        domain_results = {"domain": args.domain}
        domain_results["Reverse_Lookup"], domain_results["Hosting_Provider"] = analyze_domain(args.domain)
        domain_results["aws_storage_scan"], domain_results["gcp_storage_scan"], domain_results["azure_storage_scan"] = scan_storage(args.domain, [], scan_subdomains=False, threads=threads)

        # GrayHatWarfare Search
        if args.grayhatwarfare or args.all:
            print(f"Finding company name for GrayHatWarfare search for domain: {args.domain}")
            company_name, _ = find_company_name(args.domain, args.config_file)
            if company_name:
                unique_keywords.add(company_name)
                domain_results["company_name"] = company_name

        results.append(domain_results)

    # Analyze domains from a list
    if args.list:
        try:
            with open(args.list, "r") as file:
                domains = [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print(f"Error: File {args.list} not found.")
            return

        for domain in domains:
            print(f"\nAnalyzing domain from list: {domain}")
            domain_results = {"domain": domain}
            domain_results["Reverse_Lookup"], domain_results["Hosting_Provider"] = analyze_domain(domain)
            domain_results["aws_storage_scan"], domain_results["gcp_storage_scan"], domain_results["azure_storage_scan"] = scan_storage(domain, [], scan_subdomains=False, threads=threads)

            # GrayHatWarfare Search
            if args.grayhatwarfare or args.all:
                print(f"Finding company name for GrayHatWarfare search for domain: {domain}")
                company_name, _ = find_company_name(domain, args.config_file)
                if company_name:
                    unique_keywords.add(company_name)
                    domain_results["company_name"] = company_name

            results.append(domain_results)

    # Perform GrayHatWarfare search for unique keywords
    if args.grayhatwarfare or args.all:
        print("\nStarting GrayHatWarfare search for extracted keywords...")
        grayhatwarfare_results = []
        for keyword in unique_keywords:
            print(f"Performing GrayHatWarfare search for keyword: {keyword}")
            search_results = perform_grayhatwarfare_search(keyword, args.config_file)
            grayhatwarfare_results.append({"keyword": keyword, "results": search_results})
        
        results.append({"grayhatwarfare_search": grayhatwarfare_results})

    # Output results to JSON file if -o is specified
    if args.output:
        try:
            with open(args.output, "w") as outfile:
                json.dump(results, outfile, indent=4)
            print(f"\nResults saved to {args.output}")
        except IOError as e:
            print(f"Error writing to output file {args.output}: {e}")

    print("\nProcess completed.")

# Call the display_logo function before starting the main script
if __name__ == "__main__":
    display_logo()
    main()
