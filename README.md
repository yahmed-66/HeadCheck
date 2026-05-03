# HeadCheck - Quick header security auditing tool
---

A quick auditing tool that checks if headers present on a website align with OWASP best practices.

## Quick start:

```
git clone https://github.com/yahmed-66/HeadCheck
cd HeadCheck
pip3 install -r requirements.txt
python3 main.py <URL>
```

## Features

Headcheck polls the following URLs provided by OWASP to check if the site's header security matches those recommended by OWASP:
- Headers that should be added: [https://github.com/OWASP/www-project-secure-headers/blob/master/ci/headers_add.json]
- Headers that should be removed: [https://github.com/OWASP/www-project-secure-headers/blob/master/ci/headers_remove.json]

Please make a pull request if you would like to add more features

### Disclaimers

This tool is designed for authorized security testing only. Unauthorized access to computer systems is illegal and punishable by law.

HeadCheck is released under the [MIT License](https://opensource.org/license/mit).