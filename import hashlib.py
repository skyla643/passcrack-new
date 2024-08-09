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

# Function to check multiple passwords
def check_multiple_passwords(passwords):
    results = {}
    for password in passwords:
        leaked, count = check_password_leak(password)
        results[password] = (leaked, count)
    return results

# Example usage
if __name__ == "__main__":
    # You can hardcode passwords here or get them from user input
    passwords = ["#", "#", "#"] # type all the passwords you need checked (allows more than one to be inserted)
    
    results = check_multiple_passwords(passwords)
    
    for password, (leaked, count) in results.items():
        if leaked:
            print(f"Password '{password}' has been leaked {count} times.")
        else:
            print(f"Password '{password}' is safe (not found in known breaches).")
