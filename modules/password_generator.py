
import secrets
import string

class PasswordGenerator:
    def generate(self, length=16, letters=True, numbers=True, symbols=True):
        pool = ""
        if letters:
            pool += string.ascii_letters
        if numbers:
            pool += string.digits
        if symbols:
            pool += "!@#$%^&*()-_=+[]{};:,.?/|"
        if not pool:
            pool = string.ascii_letters + string.digits
        return "".join(secrets.choice(pool) for _ in range(max(4, int(length))))

    def strength(self, password):
        score = 0
        if len(password) >= 12: score += 1
        if len(password) >= 18: score += 1
        if any(c.islower() for c in password): score += 1
        if any(c.isupper() for c in password): score += 1
        if any(c.isdigit() for c in password): score += 1
        if any(not c.isalnum() for c in password): score += 1
        if score <= 2: return "Weak"
        if score <= 4: return "Good"
        return "Very Strong"
