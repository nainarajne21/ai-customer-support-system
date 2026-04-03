# tasks.py - Three customer support tasks with automatic graders
# Each task has: name, description, customer email, and a scoring function

from pydantic import BaseModel
from typing import Dict, Any

class Task(BaseModel):
    """A single task for the AI to solve"""
    name: str  # Name of the task (easy/medium/hard)
    description: str  # What the AI needs to do
    customer_email: str  # The email from the customer
    expected_keywords: list  # Words the AI should use in response
    forbidden_words: list  # Words the AI should NEVER use
    min_length: int  # Minimum response length
    max_length: int  # Maximum response length

# ============ TASK 1: EASY - Password Reset ============
TASK_EASY = Task(
    name="password_reset",
    description="A customer forgot their password. Help them reset it politely.",
    customer_email="Hello! I forgot my password. Can you help me reset it?",
    expected_keywords=["password", "reset", "help", "click", "link", "email"],
    forbidden_words=["stupid", "dumb", "can't", "impossible"],
    min_length=30,
    max_length=150
)

# ============ TASK 2: MEDIUM - Double Billing ============
TASK_MEDIUM = Task(
    name="double_billing",
    description="A customer was charged twice for their subscription. Process a refund.",
    customer_email="Hi, I've been charged twice for my subscription this month. Please refund one of them.",
    expected_keywords=["refund", "charge", "subscription", "sorry", "process", "credit", "double"],
    forbidden_words=["no", "can't", "ignore", "later"],
    min_length=50,
    max_length=200
)

# ============ TASK 3: HARD - Angry Customer & App Crash ============
TASK_HARD = Task(
    name="app_crash_refund",
    description="A very angry customer's app crashed multiple times. Handle with care and offer refund.",
    customer_email="Your app crashed 5 times today! I've lost all my work. I want a full refund and I'm very angry!",
    expected_keywords=["sorry", "apologize", "refund", "crash", "frustration", "understand", "investigate", "compensation"],
    forbidden_words=["stupid", "no", "can't", "maybe", "ignore", "too bad"],
    min_length=80,
    max_length=300
)

# Dictionary to access tasks easily
ALL_TASKS = {
    "easy": TASK_EASY,
    "medium": TASK_MEDIUM,
    "hard": TASK_HARD
}

def grade_response(task: Task, response: str) -> float:
    """
    This is the AUTOMATIC GRADER!
    It gives a score from 0.0 to 1.0 based on how good the AI's response is.
    
    Think of it like a teacher grading homework:
    - 0.0 = F (terrible)
    - 0.5 = C (okay)
    - 1.0 = A+ (perfect!)
    """
    score = 0.0
    
    # === PART 1: Length Check (20% of score) ===
    # Is the response too short or too long?
    if task.min_length <= len(response) <= task.max_length:
        score += 0.2  # Perfect length!
    elif len(response) < task.min_length:
        score += 0.1  # Too short - half points
    elif len(response) > task.max_length:
        score += 0.05  # Too long - barely any points
    
    # === PART 2: Expected Keywords (40% of score) ===
    # Does the AI use important words?
    keyword_score = 0
    response_lower = response.lower()
    
    for keyword in task.expected_keywords:
        if keyword.lower() in response_lower:
            keyword_score += 1
    
    # Convert to percentage (how many keywords found)
    if task.expected_keywords:
        score += (keyword_score / len(task.expected_keywords)) * 0.4
    
    # === PART 3: Forbidden Words Penalty (20% penalty) ===
    # Bad words reduce score
    for bad_word in task.forbidden_words:
        if bad_word.lower() in response_lower:
            score -= 0.2  # Big penalty!
            break  # Only penalize once per response
    
    # === PART 4: Professional Tone (20% of score) ===
    # Check for polite and professional language
    polite_words = ["thank", "appreciate", "please", "happy to help", "glad"]
    for word in polite_words:
        if word in response_lower:
            score += 0.05
            break  # Just need one polite word
    
    # === BONUS: Special for HARD task (extra points for empathy) ===
    if task.name == "app_crash_refund":
        empathy_words = ["understand", "frustrating", "sorry", "apologize"]
        for word in empathy_words:
            if word in response_lower:
                score += 0.1
                break
    
    # Make sure score stays between 0.0 and 1.0
    return max(0.0, min(1.0, score))

def get_task(task_name: str) -> Task:
    """Get a task by name (easy, medium, or hard)"""
    if task_name not in ALL_TASKS:
        raise ValueError(f"Task '{task_name}' not found! Choose from: {list(ALL_TASKS.keys())}")
    return ALL_TASKS[task_name]

def get_all_tasks() -> Dict[str, Task]:
    """Get all tasks"""
    return ALL_TASKS

# ============ TEST SECTION ============
if __name__ == "__main__":
    print("🎮 Testing the Task System!\n")
    
    # Test the grader with some example responses
    test_response = "I'm sorry you forgot your password! Please click the 'Forgot Password' link to reset it."
    
    print(f"Task: {TASK_EASY.name}")
    print(f"Customer: {TASK_EASY.customer_email}")
    print(f"AI Response: {test_response}")
    print(f"Grade: {grade_response(TASK_EASY, test_response)}/1.0")
    
    print("\n--- Testing Bad Response ---")
    bad_response = "no"
    print(f"AI Response: {bad_response}")
    print(f"Grade: {grade_response(TASK_EASY, bad_response)}/1.0")