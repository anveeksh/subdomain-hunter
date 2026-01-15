# 🎯 SubdomainHunter

<p align="center">
  <img src="https://img.shields.io/badge/python-3.7+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/version-1.0-orange.svg" alt="Version">
</p>

<p align="center">
  <strong>A powerful, fast, and comprehensive subdomain enumeration tool</strong><br>
  Designed for security researchers, penetration testers, and bug bounty hunters
</p>

<p align="center">
  Developer: <strong>Anveeksh</strong><br>
  Website: <a href="https://www.anveekshmrao.com">https://www.anveekshmrao.com</a>
</p>

---

## ✨ Features

### 🔍 Multiple Discovery Methods
- **Certificate Transparency Logs** - Query CT logs for historical SSL certificates
- **DNS Brute-Force** - Multi-threaded subdomain discovery with wordlists
- **Web Source Aggregation** - Collect data from public APIs and sources
- **DNS Zone Transfer** - Attempt AXFR zone transfers

### ⚡ High Performance
- Multi-threaded concurrent scanning
- Optimized DNS resolution
- Progress bars and real-time feedback
- Configurable thread count and timeouts

### 🎨 Beautiful Interface
- **Interactive Menu Mode** - User-friendly menu system
- **Command-Line Mode** - Full CLI support for automation
- Colored terminal output
- Real-time progress indicators
- Detailed statistics and reporting

### 💾 Flexible Export
- Export results as JSON or TXT
- Timestamped output files
- View previous scan results
- Organized data structure

---

## 📋 Requirements

- **Python 3.7+**
- **Internet connection**
- **pip** (Python package manager)

---

## 🚀 Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/subdomain-hunter.git
cd subdomain-hunter
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

That's it! You're ready to go.

---

## 📖 Usage

### Interactive Mode (Recommended for Beginners)

Simply run the tool without any arguments:
```bash
python subdomain_hunter.py
```

You'll see a beautiful menu:
```
╔════════════════════════════════════════════════════════╗
║              SUBDOMAIN HUNTER - MAIN MENU              ║
╚════════════════════════════════════════════════════════╝

[1] Quick Scan (Passive Only - Fast)
[2] Standard Scan (Passive + Basic Brute-Force)
[3] Aggressive Scan (All Methods + Custom Wordlist)
[4] Custom Scan (Choose Your Options)
[5] View Previous Results
[6] Help & Documentation
[7] About & Credits
[0] Exit
```

### Command-Line Mode (For Automation)

#### Basic Scan
```bash
python subdomain_hunter.py -d example.com
```

#### Scan with Custom Wordlist
```bash
python subdomain_hunter.py -d example.com -w wordlists/big.txt
```

#### Fast Scan (More Threads)
```bash
python subdomain_hunter.py -d example.com -t 100
```

#### Passive Enumeration Only
```bash
python subdomain_hunter.py -d example.com --no-brute
```

#### Verbose Mode
```bash
python subdomain_hunter.py -d example.com -v
```

#### Export as JSON
```bash
python subdomain_hunter.py -d example.com -o json
```

#### Custom Output Filename
```bash
python subdomain_hunter.py -d example.com -f my_scan -o json
```

---

## 🎯 Command-Line Options
```
Required Arguments:
  -d, --domain          Target domain to enumerate

Optional Arguments:
  -w, --wordlist        Path to wordlist file for brute-force
  -t, --threads         Number of threads (default: 50)
  --timeout             DNS timeout in seconds (default: 5)
  -v, --verbose         Enable verbose output
  
Scan Control:
  --no-ct               Disable Certificate Transparency search
  --no-brute            Disable DNS brute-force
  --no-web              Disable web source search
  --no-zone             Disable zone transfer attempt
  
Output Options:
  -o, --output          Output format: txt or json (default: txt)
  -f, --file            Output filename (without extension)
```

---

## 📊 Example Output
```
   _____ _   _ ____  ____   ___  __  __    _    ___ _   _ 
  / ____| | | | __ )|  _ \ / _ \|  \/  |  / \  |_ _| \ | |
  \___ \| | | |  _ \| | | | | | | |\/| | / _ \  | ||  \| |
   ___) | |_| | |_) | |_| | |_| | |  | |/ ___ \ | || |\  |
  |____/ \___/|____/|____/ \___/|_|  |_/_/   \_\___|_| \_|
                                                            
    HUNTER v1.0 - Advanced Subdomain Enumeration Tool
    Developer: Anveeksh | https://www.anveekshmrao.com
    For Security Researchers & Bug Bounty Hunters
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[14:23:45] [*] Starting subdomain enumeration for: example.com

[14:23:45] [*] Phase 1: Certificate Transparency Logs
[14:23:47] [+] Found 42 subdomains from CT logs

[14:23:47] [*] Phase 2: Web Sources & APIs
[14:23:49] [+] Found 18 subdomains from web sources

[14:23:49] [*] Phase 3: DNS Zone Transfer
[14:23:49] [!] Zone transfer not allowed (expected)

[14:23:49] [*] Phase 4: DNS Brute-Force Attack
[14:23:49] [*] Loaded 60 entries from wordlist
[14:23:49] [FOUND] www.example.com
[*] Progress: [████████████████████████████████████████] 100.0% (60/60)
[14:23:50] [+] Found 1 subdomains from brute-force

======================================================================
                       SCAN SUMMARY
======================================================================

Target Domain: example.com
Scan Duration: 5.2 seconds
Total Subdomains: 56

Discovery Breakdown:
  • Certificate Transparency...... 42
  • Web Sources.................... 18
  • DNS Brute-Force................ 1

======================================================================

Discovered Subdomains:
──────────────────────────────────────────────────────────────────────
  • admin.example.com
  • api.example.com
  • blog.example.com
  • dev.example.com
  • mail.example.com
  • www.example.com
  ...

[14:23:50] [+] Results saved to: subdomains_example.com_20250115_142350.txt

[✓] Scan completed successfully!
```

---

## 🗂️ Recommended Wordlists

For better results, use comprehensive wordlists:

### SecLists
```bash
git clone https://github.com/danielmiessler/SecLists.git
python subdomain_hunter.py -d example.com -w SecLists/Discovery/DNS/subdomains-top1million-5000.txt
```

### Popular Wordlists
- **SecLists** - https://github.com/danielmiessler/SecLists
  - `Discovery/DNS/subdomains-top1million-5000.txt` (5K subdomains)
  - `Discovery/DNS/subdomains-top1million-20000.txt` (20K subdomains)
  - `Discovery/DNS/subdomains-top1million-110000.txt` (110K subdomains)

- **Assetnote** - https://wordlists.assetnote.io/

- **jhaddix/all.txt** - https://gist.github.com/jhaddix/86a06c5dc309d08580a018c66354a056

---

## 🛡️ Ethical Usage

This tool is designed for:
- ✅ **Security research**
- ✅ **Bug bounty hunting**
- ✅ **Penetration testing** (with explicit permission)
- ✅ **Educational purposes**

### ⚠️ Important Legal Notice

**Only scan domains you own or have explicit written permission to test.**

Unauthorized scanning of domains you don't own is:
- Illegal in most jurisdictions
- Violates terms of service
- Can result in legal action

Always obtain proper authorization before scanning any target.

---

## 🏗️ Project Structure
```
subdomain-hunter/
├── subdomain_hunter.py      # Main tool file
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── LICENSE                   # MIT License
├── .gitignore               # Git ignore file
└── wordlists/               # Wordlist directory
    └── common.txt           # Default wordlist (60 entries)
```

---

## 🔧 Advanced Configuration

### Custom DNS Servers

Edit `subdomain_hunter.py` and modify the DNS servers:
```python
self.resolver.nameservers = ['8.8.8.8', '1.1.1.1', '8.8.4.4']
```

### Thread Optimization

- **Fast networks**: Use 100-200 threads
- **Standard networks**: Use 50-100 threads (default: 50)
- **Slow networks**: Use 20-50 threads
```bash
python subdomain_hunter.py -d example.com -t 150
```

### Timeout Configuration

Adjust DNS timeout for slower connections:
```bash
python subdomain_hunter.py -d example.com --timeout 10
```

---

## 🐛 Troubleshooting

### Issue: "Module not found: dns"
**Solution:**
```bash
pip install dnspython requests
```

### Issue: "Wordlist not found"
**Solution:**
Make sure the `wordlists/common.txt` file exists, or specify a custom wordlist:
```bash
python subdomain_hunter.py -d example.com -w /path/to/your/wordlist.txt
```

### Issue: Slow scanning
**Solution:**
- Increase thread count: `-t 100`
- Use smaller wordlists
- Check your internet connection

### Issue: No results found
**Solution:**
- Try increasing timeout: `--timeout 10`
- Use verbose mode: `-v`
- Check if the domain is valid and resolves

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
```bash
   git checkout -b feature/AmazingFeature
```
3. **Commit your changes**
```bash
   git commit -m 'Add some AmazingFeature'
```
4. **Push to the branch**
```bash
   git push origin feature/AmazingFeature
```
5. **Open a Pull Request**

### Ideas for Contributions
- Add more data sources
- HTTP probing functionality
- Screenshot capture
- Vulnerability scanning
- HTML report generation
- Database integration
- API endpoint

---

## 📝 Changelog

### Version 1.0 (January 2025)
- Initial release
- Certificate Transparency log search
- DNS brute-force with multi-threading
- Web source aggregation
- Interactive menu interface
- Command-line mode
- JSON and TXT export
- Progress bars and colored output

---

## 📜 License

This project is licensed under the **MIT License**.
```
MIT License

Copyright (c) 2025 Anveeksh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 🙏 Acknowledgments

- **crt.sh** - Certificate Transparency log database
- **HackerTarget** - Free API for reconnaissance
- **BufferOver** - DNS data aggregation
- **dnspython** - Python DNS toolkit
- All contributors and testers

---

## 📧 Contact & Support

- **Developer:** Anveeksh
- **Website:** [https://www.anveekshmrao.com](https://www.anveekshmrao.com)
- **GitHub:** [https://github.com/yourusername/subdomain-hunter](https://github.com/yourusername/subdomain-hunter)

### Found a bug or have a suggestion?
- Open an issue on GitHub
- Contact via website
- Submit a pull request

---

## 🌟 Show Your Support

If you find this tool helpful, please:
- ⭐ Star the repository
- 🐛 Report bugs
- 💡 Suggest features
- 🤝 Contribute code
- 📢 Share with others

---

<p align="center">
  <strong>Made with ❤️ for the cybersecurity community</strong><br>
  Happy hunting! 🎯
</p>
```

---

## 📁 FILE 5: `.gitignore`
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Output files
*.txt
*.json
!requirements.txt
!wordlists/*.txt

# OS
.DS_Store
Thumbs.db
```

---

## 📁 FILE 6: `LICENSE`
```
MIT License

Copyright (c) 2025 Anveeksh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.