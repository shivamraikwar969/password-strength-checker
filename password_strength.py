import math
import re

COMMON_PASSWORDS = {
    "password", "123456", "12345678", "123456789", "qwerty", "abc123",
    "letmein", "welcome", "admin", "iloveyou", "monkey", "dragon",
    "password1", "qwerty123", "111111", "passw0rd", "admin123",
}


def estimate_entropy(password):
    pool = 0
    if re.search(r"[a-z]", password):
        pool += 26
    if re.search(r"[A-Z]", password):
        pool += 26
    if re.search(r"\d", password):
        pool += 10
    if re.search(r"[^A-Za-z0-9]", password):
        pool += 32
    return len(password) * math.log2(pool) if pool else 0.0


def check_password(password):
    score = 0
    tips = []

    if len(password) >= 8:
        score += 1
    else:
        tips.append("Use at least 8 characters (12+ is better).")
    if len(password) >= 12:
        score += 1

    if re.search(r"[a-z]", password):
        score += 1
    else:
        tips.append("Add lowercase letters.")
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        tips.append("Add uppercase letters.")
    if re.search(r"\d", password):
        score += 1
    else:
        tips.append("Add numbers.")
    if re.search(r"[^A-Za-z0-9]", password):
        score += 1
    else:
        tips.append("Add special characters (!@#$%^&*).")

    if password.lower() in COMMON_PASSWORDS:
        score = 0
        tips.insert(0, "This is a very common password. Avoid it!")
    if re.search(r"(.)\1{2,}", password):
        score = max(score - 1, 0)
        tips.append("Avoid repeating the same character 3+ times (e.g. 'aaa').")
    if re.search(r"(0123|1234|2345|3456|4567|5678|6789|abcd|qwer)", password.lower()):
        score = max(score - 1, 0)
        tips.append("Avoid simple sequences like '1234' or 'abcd'.")

    if score <= 2:
        label = "Weak"
    elif score <= 4:
        label = "Medium"
    else:
        label = "Strong"

    return score, label, tips


def main():
    print("=== Password Strength Checker ===")
    while True:
        password = input("\nEnter a password (blank to quit): ")
        if not password:
            print("Bye!")
            break

        score, label, tips = check_password(password)
        entropy = estimate_entropy(password)

        print(f"\nStrength : {label} ({score}/6)")
        print(f"Entropy  : ~{entropy:.1f} bits")
        if tips:
            print("Suggestions:")
            for tip in tips:
                print(f"  - {tip}")
        else:
            print("Great password!")


if __name__ == "__main__":
    main()