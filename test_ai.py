from inference import ask_ai

# Test with different customer emails
test_emails = [
    "I forgot my password!",
    "You charged me twice!",
    "Your app crashed, I want a refund!"
]

for email in test_emails:
    response = ask_ai(email)
    print(f"Customer: {email}")
    print(f"AI: {response}\n")