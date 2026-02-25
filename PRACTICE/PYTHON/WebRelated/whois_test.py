"""whois_test.py: A simple script to perform a WHOIS lookup on a domain name."""

try:
    import whois
except ImportError:
    import sys
    print("Missing dependency: 'whois'. Install it in your environment:\n    python -m pip install python-whois")
    sys.exit(1)

def main():
    domain = "google.com"  # input("Enter a domain name: ")
    try:
        w = whois.whois(domain)
        print(f"Domain Name: {w.domain_name}")
        print(f"Registrar: {w.registrar}")
        print(f"Creation Date: {w.creation_date}")
        print(f"Expiration Date: {w.expiration_date}")
        print(f"Name Servers: {w.name_servers}")
    except Exception as e:
        print(f"Error fetching WHOIS data for {domain}: {e}")

if __name__ == "__main__":
    main()