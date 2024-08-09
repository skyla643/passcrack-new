# Password Leak Checker

A Python script to check if your passwords have been compromised in any known data breaches using the **Have I Been Pwned** API.

## Overview

This script hashes your password using the SHA-1 algorithm and checks if it has been leaked in any known data breaches. It leverages the Have I Been Pwned (HIBP) API to compare the hashed password against a database of compromised passwords.

## How It Works

1. **Password Hashing**: The script hashes the password using the SHA-1 algorithm.
2. **K-Anonymity**: The first 5 characters of the hash are sent to the HIBP API, which returns a list of hashes that match this prefix.
3. **Suffix Comparison**: The script compares the remaining characters of the hash (suffix) to the returned list to determine if the password has been leaked.
4. **Result**: The script will indicate whether your password has been compromised and how many times it has been found in breaches.

## Requirements

- Python 3
- `requests` library

Install the `requests` library using pip:

```bash
pip install requests
```

## Usage

### 1. Single Password Check

To check if a single password has been leaked:

```python
import hashlib
import requests

# Function to check if a password has been leaked
def check_password_leak(password):
    # Hash the password using SHA-1
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    
    # The first 5 characters of the hash (for k-anonymity)
    prefix = sha1_password[:5]
    
    # The rest of the hash
    suffix = sha1_password[5:]
    
    # Query the Have I Been Pwned API with the first 5 characters
    url = f'https://api.pwnedpasswords.com/range/{prefix}'
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Check if the suffix is in the response
        hashes = (line.split(':') for line in response.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                return True, count
        return False, 0
    else:
        raise Exception(f"Failed to connect to API: {response.status_code}")

# Example usage
if __name__ == "__main__":
    password = "your_password_here"  # Replace with your password
    leaked, count = check_password_leak(password)
    
    if leaked:
        print(f"Password '{password}' has been leaked {count} times.")
    else:
        print(f"Password '{password}' is safe (not found in known breaches).")
```

### 2. Multiple Passwords Check

To check multiple passwords at once:

```python
# Function to check multiple passwords
def check_multiple_passwords(passwords):
    results = {}
    for password in passwords:
        leaked, count = check_password_leak(password)
        results[password] = (leaked, count)
    return results

# Example usage
if __name__ == "__main__":
    passwords = ["password1", "password2", "password3"]  # Replace with your passwords
    
    results = check_multiple_passwords(passwords)
    
    for password, (leaked, count) in results.items():
        if leaked:
            print(f"Password '{password}' has been leaked {count} times.")
        else:
            print(f"Password '{password}' is safe (not found in known breaches).")
```

### 3. How to Run

1. Clone the repository or download the script.
2. Install the `requests` library if you haven't already: `pip install requests`.
3. Replace the example passwords in the `passwords` list with the ones you want to check.
4. Run the script using Python: `python script_name.py`.

### 4. Sample Output

```plaintext
Password 'password1' has been leaked 500 times.
Password 'password2' is safe (not found in known breaches).
Password 'password3' has been leaked 1500 times.
```

## Contributing

Feel free to fork this repository, make your changes, and submit a pull request. If you find a bug or have a suggestion for improvement, please open an issue.

## License

This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This script is provided for educational and informational purposes only. Use it at your own risk. The author is not responsible for any misuse of the code.

```

### Explanation:

- **Overview**: Describes what the script does and how it works.
- **Requirements**: Lists the prerequisites for running the script, such as Python 3 and the `requests` library.
- **Usage**: Provides detailed instructions on how to use the script, including examples for checking both single and multiple passwords.
- **Contributing**: Encourages others to contribute to the project.
- **License**: Mentions the licensing terms.
- **Disclaimer**: Clarifies the intent of the script and disclaims liability for misuse.

This README file should give users clear guidance on how to use your script and understand its purpose.
