import argparse
import json
import subprocess
import requests
import re

def scan_ports(target):
    result = subprocess.run(["nmap", "-Pn", "-p-", target], stdout=subprocess.PIPE)
    return result.stdout.decode()

def check_sql_injection(url):
    test_url = url + "'"
    response = requests.get(test_url)
    if "sql" in response.text.lower() or "syntax" in response.text.lower():
        return True
    return False

def check_xss(url):
    xss_payload = "<script>alert(1)</script>"
    response = requests.get(url + "?test=" + xss_payload)
    return xss_payload in response.text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, help="Target domain or IP")
    args = parser.parse_args()

    results = {}
    results["target"] = args.target
    results["open_ports"] = scan_ports(args.target)
    results["sql_injection_vulnerable"] = check_sql_injection(args.target)
    results["xss_vulnerable"] = check_xss(args.target)

    with open("reports/report.json", "w") as f:
        json.dump(results, f, indent=4)

    print("Scan complete. Results saved to reports/report.json")

if __name__ == "__main__":
    main()
