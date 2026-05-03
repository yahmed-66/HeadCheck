from curl_cffi import requests
from colorama import Fore, Style
import sys
from pathlib import Path

# Pull security headers from OWASP
OWASP_SECURITY_HEADERS_ADD = "https://raw.githubusercontent.com/OWASP/www-project-secure-headers/refs/heads/master/ci/headers_add.json"
OWASP_SECURITY_HEADERS_REMOVE = "https://raw.githubusercontent.com/OWASP/www-project-secure-headers/refs/heads/master/ci/headers_remove.json"
def get_owasp_security_headers(owasp_url):
    try:    
        response = requests.get(owasp_url)
        if response.status_code != 200:
            print(f"{Fore.RED}[ ! ] Failed to fetch OWASP security headers:{Style.RESET_ALL}")
            print(f"{Fore.RED}[ ! ] Status code: {response.status_code}{Style.RESET_ALL}")
            sys.exit(1)
        return response.json()['headers']
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[ ! ] An error occurred while fetching OWASP security headers:{Style.RESET_ALL}")
        print(f"{Fore.RED}[ ! ] Error: {e}{Style.RESET_ALL}")
        sys.exit(1)

# Abstracts the GET request process
def make_request(url, allow_redirects=True):
    try:
        response = requests.get(
            url,
            allow_redirects=allow_redirects,
            impersonate="chrome",
        )
        return response
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[ ! ] An error occurred while making the request:{Style.RESET_ALL}")
        print(f"{Fore.RED}[ ! ] Error: {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    # Input URL from user
    if len(sys.argv) != 2:
        print(f"{Fore.RED}[ ! ] Usage: python3 {Path(sys.argv[0]).name} <url>{Style.RESET_ALL}")
        sys.exit(1)

    url = sys.argv[1]
    if not url.startswith(("http://", "https://")):
        print(f"{Fore.RED}[ ! ] URL must start with http:// or https://{Style.RESET_ALL}")
        sys.exit(1)
    # Check only response headers
    response = make_request(url)
    # headers = dict(response.headers)
    # Fetch OWASP security headers list
    print(f"{Fore.GREEN}[ * ] Fetching OWASP security headers list...{Style.RESET_ALL}")
    # Match formats for all data pulled
    add_headers = {h["name"].lower(): h["value"] for h in get_owasp_security_headers(OWASP_SECURITY_HEADERS_ADD)}
    remove_headers = {h.lower() for h in get_owasp_security_headers(OWASP_SECURITY_HEADERS_REMOVE)}
    headers = {k.lower(): v for k, v in response.headers.items()}
    
    # Check if headers in url are missing from OWASP headers list
    missing_headers = []
    misconfigured_headers = []
    unrecommended_headers = []
    # If headers are there, check if they are configured properly, otherwise suggest they be added
    for name, recommended_value in add_headers.items():
        actual_value = headers.get(name)
        if actual_value is None:
            missing_headers.append(name)
        elif actual_value.lower() != recommended_value.lower():
            misconfigured_headers.append((name, actual_value, recommended_value))
    # Check if any response headers are on the remove list
    for name in headers:
        if name in remove_headers:
            unrecommended_headers.append(name)

    # Print results
    print(f"{Fore.GREEN}{10 * '='} Results {10 * '='}{Style.RESET_ALL}")
    if unrecommended_headers:
        print(f"{Fore.RED}[ - ] Unrecommended headers:{Style.RESET_ALL}")
        for header in unrecommended_headers:
            print(f"{Fore.RED}\t - {header}{Style.RESET_ALL}")
    if misconfigured_headers:
        print(f"{Fore.YELLOW}[ * ] Misconfigured headers:{Style.RESET_ALL}")
        for name, actual, recommended in misconfigured_headers:
            print(f"{Fore.YELLOW}\t * {name}:\n\t\tFound: '{actual}'\n\t\tRecommended: '{recommended}'{Style.RESET_ALL}")
    if missing_headers:
        print(f"{Fore.CYAN}[ + ] Missing headers:{Style.RESET_ALL}")
        for header in missing_headers:
            print(f"{Fore.CYAN}\t + {header}{Style.RESET_ALL}")
    # Check if headers best practice is maintained
    if len(unrecommended_headers) + len(misconfigured_headers) + len(missing_headers) == 0:
        print(f"{Fore.GREEN}[ :) ] No issues found! Well done!{Style.RESET_ALL}")
    
    print(f"{Fore.GREEN}Summary: {Fore.RED}{len(unrecommended_headers)} Unrecommended headers, {Fore.YELLOW} {len(misconfigured_headers)} Misconfigured headers, {Fore.CYAN} {len(missing_headers)} Missing headers.")
    sys.exit(0)