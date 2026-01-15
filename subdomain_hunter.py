#!/usr/bin/env python3
"""
SubdomainHunter - Advanced Subdomain Enumeration Tool
A fast, multi-threaded subdomain discovery tool
Usage: python subdomain_hunter.py -d example.com
"""

import dns.resolver
import requests
import concurrent.futures
import argparse
import json
import re
import time
import sys
from urllib.parse import urlparse
from typing import Set, List, Dict
from collections import defaultdict
from datetime import datetime

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_banner():
    """Display tool banner"""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
   _____ __  ______  ____  ____  __  _____    _____   __
  / ___// / / / __ )/ __ \/ __ \/  |/  /   |  /  _/ | / /
  \__ \/ / / / __  / / / / / / / /|_/ / /| |  / //  |/ / 
 ___/ / /_/ / /_/ / /_/ / /_/ / /  / / ___ |_/ // /|  /  
/____/\____/_____/_____/\____/_/  /_/_/  |_/___/_/ |_/   
                                                          
    HUNTER v1.0 - Advanced Subdomain Enumeration Tool
{Colors.END}{Colors.YELLOW}    Created for Security Researchers & Bug Bounty Hunters{Colors.END}
{Colors.BLUE}    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}
    """
    print(banner)

class SubdomainHunter:
    def __init__(self, domain: str, threads: int = 50, timeout: int = 5, verbose: bool = False):
        self.domain = domain
        self.threads = threads
        self.timeout = timeout
        self.verbose = verbose
        self.subdomains: Set[str] = set()
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = timeout
        self.resolver.lifetime = timeout
        
        # Use reliable DNS servers
        self.resolver.nameservers = ['8.8.8.8', '1.1.1.1', '8.8.4.4']
        
        self.start_time = time.time()
    
    def log(self, message: str, level: str = "info"):
        """Print colored log messages"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if level == "info":
            print(f"{Colors.BLUE}[{timestamp}] [*]{Colors.END} {message}")
        elif level == "success":
            print(f"{Colors.GREEN}[{timestamp}] [+]{Colors.END} {message}")
        elif level == "error":
            print(f"{Colors.RED}[{timestamp}] [-]{Colors.END} {message}")
        elif level == "warning":
            print(f"{Colors.YELLOW}[{timestamp}] [!]{Colors.END} {message}")
        elif level == "found":
            print(f"{Colors.CYAN}[{timestamp}] [FOUND]{Colors.END} {Colors.GREEN}{message}{Colors.END}")
    
    def run_all(self, wordlist_path: str = None, enable_ct: bool = True, 
                enable_brute: bool = True, enable_web: bool = True,
                enable_zone: bool = True) -> Dict:
        """Run all enumeration techniques"""
        self.log(f"Starting subdomain enumeration for: {Colors.BOLD}{self.domain}{Colors.END}", "info")
        print()
        
        results = {
            'domain': self.domain,
            'subdomains': [],
            'statistics': defaultdict(int),
            'scan_time': 0
        }
        
        # Certificate Transparency Logs
        if enable_ct:
            self.log("Phase 1: Certificate Transparency Logs", "info")
            ct_subs = self.search_ct_logs()
            results['statistics']['ct_logs'] = len(ct_subs)
            self.log(f"Found {Colors.BOLD}{len(ct_subs)}{Colors.END} subdomains from CT logs", "success")
            print()
        
        # Web Sources
        if enable_web:
            self.log("Phase 2: Web Sources & APIs", "info")
            web_subs = self.web_search()
            results['statistics']['web_search'] = len(web_subs)
            self.log(f"Found {Colors.BOLD}{len(web_subs)}{Colors.END} subdomains from web sources", "success")
            print()
        
        # DNS Zone Transfer
        if enable_zone:
            self.log("Phase 3: DNS Zone Transfer", "info")
            zt_subs = self.zone_transfer()
            results['statistics']['zone_transfer'] = len(zt_subs)
            if zt_subs:
                self.log(f"Found {Colors.BOLD}{len(zt_subs)}{Colors.END} subdomains from zone transfer", "success")
            else:
                self.log("Zone transfer not allowed (expected)", "warning")
            print()
        
        # DNS Brute Force (Last because it's time-consuming)
        if enable_brute and wordlist_path:
            self.log("Phase 4: DNS Brute-Force Attack", "info")
            brute_subs = self.dns_bruteforce(wordlist_path)
            results['statistics']['brute_force'] = len(brute_subs)
            self.log(f"Found {Colors.BOLD}{len(brute_subs)}{Colors.END} subdomains from brute-force", "success")
            print()
        
        # Calculate scan time
        results['scan_time'] = round(time.time() - self.start_time, 2)
        
        # Compile unique results
        all_subs = sorted(list(self.subdomains))
        results['subdomains'] = all_subs
        results['statistics']['total_unique'] = len(all_subs)
        
        return results
    
    def search_ct_logs(self) -> Set[str]:
        """Search Certificate Transparency logs"""
        found = set()
        
        # crt.sh - Primary source
        try:
            url = f"https://crt.sh/?q=%.{self.domain}&output=json"
            response = requests.get(url, timeout=self.timeout * 2)
            
            if response.status_code == 200:
                data = response.json()
                for entry in data:
                    name = entry.get('name_value', '')
                    for subdomain in name.split('\n'):
                        subdomain = subdomain.strip().lower()
                        if subdomain.endswith(self.domain) and '*' not in subdomain:
                            if subdomain not in self.subdomains:
                                found.add(subdomain)
                                self.subdomains.add(subdomain)
                                if self.verbose:
                                    self.log(subdomain, "found")
        except Exception as e:
            self.log(f"crt.sh query failed: {str(e)}", "error")
        
        return found
    
    def dns_bruteforce(self, wordlist_path: str) -> Set[str]:
        """Brute-force subdomains using wordlist"""
        found = set()
        
        try:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                words = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        except FileNotFoundError:
            self.log(f"Wordlist not found: {wordlist_path}", "error")
            return found
        
        self.log(f"Loaded {len(words)} entries from wordlist", "info")
        
        def check_subdomain(word):
            subdomain = f"{word}.{self.domain}"
            if self.resolve_dns(subdomain):
                return subdomain
            return None
        
        # Progress tracking
        checked = 0
        total = len(words)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(check_subdomain, word): word for word in words}
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                checked += 1
                
                if result:
                    found.add(result)
                    self.subdomains.add(result)
                    self.log(result, "found")
                
                # Progress bar
                if checked % 50 == 0 or checked == total:
                    progress = (checked / total) * 100
                    bar_length = 40
                    filled = int(bar_length * checked / total)
                    bar = '█' * filled + '░' * (bar_length - filled)
                    print(f"\r{Colors.YELLOW}[*] Progress: [{bar}] {progress:.1f}% ({checked}/{total}){Colors.END}", end='', flush=True)
        
        print()  # New line after progress bar
        return found
    
    def resolve_dns(self, hostname: str) -> bool:
        """Check if hostname resolves"""
        try:
            self.resolver.resolve(hostname, 'A')
            return True
        except:
            return False
    
    def web_search(self) -> Set[str]:
        """Search for subdomains via web sources"""
        found = set()
        
        sources = {
            'HackerTarget': f"https://api.hackertarget.com/hostsearch/?q={self.domain}",
            'BufferOver': f"https://dns.bufferover.run/dns?q=.{self.domain}",
        }
        
        for source_name, url in sources.items():
            try:
                response = requests.get(url, timeout=self.timeout * 2)
                if response.status_code == 200:
                    # Extract subdomains
                    pattern = r'([a-zA-Z0-9][-a-zA-Z0-9]*\.)+' + re.escape(self.domain)
                    matches = re.findall(pattern, response.text)
                    
                    source_count = 0
                    for match in matches:
                        subdomain = match.lower().rstrip('.')
                        if subdomain.endswith(self.domain) and subdomain not in self.subdomains:
                            found.add(subdomain)
                            self.subdomains.add(subdomain)
                            source_count += 1
                            if self.verbose:
                                self.log(subdomain, "found")
                    
                    if source_count > 0:
                        self.log(f"{source_name}: {source_count} subdomains", "info")
                        
            except Exception as e:
                if self.verbose:
                    self.log(f"{source_name} failed: {str(e)}", "error")
        
        return found
    
    def zone_transfer(self) -> Set[str]:
        """Attempt DNS zone transfer (AXFR)"""
        found = set()
        
        try:
            import dns.zone
            import dns.query
            
            ns_records = self.resolver.resolve(self.domain, 'NS')
            
            for ns in ns_records:
                ns_server = str(ns).rstrip('.')
                try:
                    zone = dns.zone.from_xfr(
                        dns.query.xfr(ns_server, self.domain, timeout=self.timeout)
                    )
                    for name in zone.nodes.keys():
                        subdomain = f"{name}.{self.domain}".lower()
                        found.add(subdomain)
                        self.subdomains.add(subdomain)
                        if self.verbose:
                            self.log(subdomain, "found")
                except:
                    continue
        except:
            pass
        
        return found
    
    def export_results(self, results: Dict, output_format: str = 'txt', output_file: str = None):
        """Export results to file"""
        if not output_file:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_file = f"subdomains_{self.domain}_{timestamp}"
        
        if output_format == 'json':
            filename = f"{output_file}.json"
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
        elif output_format == 'txt':
            filename = f"{output_file}.txt"
            with open(filename, 'w') as f:
                for subdomain in results['subdomains']:
                    f.write(f"{subdomain}\n")
        
        self.log(f"Results saved to: {Colors.BOLD}{filename}{Colors.END}", "success")
        return filename


def print_summary(results: Dict):
    """Print scan summary"""
    print()
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}                       SCAN SUMMARY{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print()
    print(f"{Colors.BOLD}Target Domain:{Colors.END} {results['domain']}")
    print(f"{Colors.BOLD}Scan Duration:{Colors.END} {results['scan_time']} seconds")
    print(f"{Colors.BOLD}Total Subdomains:{Colors.END} {Colors.GREEN}{Colors.BOLD}{results['statistics']['total_unique']}{Colors.END}")
    print()
    print(f"{Colors.BOLD}Discovery Breakdown:{Colors.END}")
    
    methods = {
        'ct_logs': 'Certificate Transparency',
        'web_search': 'Web Sources',
        'zone_transfer': 'Zone Transfer',
        'brute_force': 'DNS Brute-Force'
    }
    
    for key, name in methods.items():
        count = results['statistics'].get(key, 0)
        if count > 0:
            print(f"  • {name:.<30} {Colors.GREEN}{count}{Colors.END}")
    
    print()
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")


def main():
    parser = argparse.ArgumentParser(
        description='SubdomainHunter - Advanced Subdomain Enumeration Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{Colors.BOLD}Examples:{Colors.END}
  Basic scan:
    python subdomain_hunter.py -d example.com
  
  Scan with custom wordlist:
    python subdomain_hunter.py -d example.com -w wordlists/big.txt
  
  Fast scan (more threads):
    python subdomain_hunter.py -d example.com -t 100
  
  Only passive enumeration (no brute-force):
    python subdomain_hunter.py -d example.com --no-brute
  
  Verbose output with JSON export:
    python subdomain_hunter.py -d example.com -v -o json

{Colors.BOLD}Note:{Colors.END} For best results, use with a comprehensive wordlist
        """
    )
    
    parser.add_argument('-d', '--domain', required=True, 
                       help='Target domain to enumerate')
    parser.add_argument('-w', '--wordlist', 
                       help='Path to wordlist file for brute-force')
    parser.add_argument('-t', '--threads', type=int, default=50, 
                       help='Number of threads (default: 50)')
    parser.add_argument('--timeout', type=int, default=5, 
                       help='DNS timeout in seconds (default: 5)')
    parser.add_argument('-v', '--verbose', action='store_true', 
                       help='Enable verbose output')
    parser.add_argument('--no-ct', action='store_true', 
                       help='Disable Certificate Transparency search')
    parser.add_argument('--no-brute', action='store_true', 
                       help='Disable DNS brute-force')
    parser.add_argument('--no-web', action='store_true', 
                       help='Disable web source search')
    parser.add_argument('--no-zone', action='store_true', 
                       help='Disable zone transfer attempt')
    parser.add_argument('-o', '--output', choices=['txt', 'json'], default='txt', 
                       help='Output format (default: txt)')
    parser.add_argument('-f', '--file', 
                       help='Output filename (without extension)')
    
    # Parse arguments
    if len(sys.argv) == 1:
        print_banner()
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()
    
    # Display banner
    print_banner()
    
    # Clean domain
    domain = urlparse(f"http://{args.domain}").netloc or args.domain
    domain = domain.lower().strip()
    
    # Validate domain
    if not re.match(r'^[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,}$', domain):
        print(f"{Colors.RED}[!] Invalid domain format: {domain}{Colors.END}")
        sys.exit(1)
    
    # Create default wordlist if brute-force enabled but no wordlist provided
    wordlist = args.wordlist
    if not args.no_brute and not wordlist:
        wordlist = 'wordlists/common.txt'
        if not os.path.exists(wordlist):
            print(f"{Colors.YELLOW}[!] No wordlist specified. Using passive enumeration only.{Colors.END}")
            print(f"{Colors.YELLOW}[!] Use -w flag to specify a wordlist for brute-force.{Colors.END}")
            args.no_brute = True
    
    # Initialize hunter
    hunter = SubdomainHunter(
        domain=domain,
        threads=args.threads,
        timeout=args.timeout,
        verbose=args.verbose
    )
    
    try:
        # Run scan
        results = hunter.run_all(
            wordlist_path=wordlist,
            enable_ct=not args.no_ct,
            enable_brute=not args.no_brute,
            enable_web=not args.no_web,
            enable_zone=not args.no_zone
        )
        
        # Print summary
        print_summary(results)
        
        # Print all discovered subdomains
        if results['subdomains']:
            print()
            print(f"{Colors.BOLD}Discovered Subdomains:{Colors.END}")
            print(f"{Colors.CYAN}{'─'*70}{Colors.END}")
            for subdomain in results['subdomains']:
                print(f"  {Colors.GREEN}•{Colors.END} {subdomain}")
            print()
        
        # Export results
        hunter.export_results(results, output_format=args.output, output_file=args.file)
        
        print()
        print(f"{Colors.GREEN}{Colors.BOLD}[✓] Scan completed successfully!{Colors.END}")
        
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] Scan interrupted by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}[!] Error: {str(e)}{Colors.END}")
        sys.exit(1)


if __name__ == "__main__":
    import os
    main()