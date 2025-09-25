import random
import string

def generate_random_password(length=12):
    """
    Generate a random password with at least one uppercase letter, 
    lowercase letter, number, and symbol.
    
    Args:
        length (int): Length of the password (minimum 4, default 12)
    
    Returns:
        str: A randomly generated password
    
    Raises:
        ValueError: If length is less than 4
    """
    if length < 4:
        raise ValueError("Password length must be at least 4 to include all required character types")
    
    # Define character sets
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Ensure at least one character from each required category
    password = [
        random.choice(uppercase),
        random.choice(lowercase),
        random.choice(digits),
        random.choice(symbols)
    ]
    
    # Fill the rest of the password length with random characters from all categories
    all_characters = uppercase + lowercase + digits + symbols
    for _ in range(length - 4):
        password.append(random.choice(all_characters))
    
    # Shuffle the password list to randomize the order
    random.shuffle(password)
    
    return ''.join(password)

# Example usage
if __name__ == "__main__":
    print("Generated passwords:")
    for i in range(5):
        password = generate_random_password(12)
        print(f"Password {i+1}: {password}")
    
    # Test with different lengths
    print("\nDifferent lengths:")
    for length in [8, 16, 20]:
        password = generate_random_password(length)
        print(f"Length {length}: {password}")