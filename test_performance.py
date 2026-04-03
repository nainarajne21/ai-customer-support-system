# test_performance.py - Tests how well your AI performs
from tasks import get_task, grade_response
from inference import ask_ai

print("=" * 60)
print("📊 PERFORMANCE TEST - How well does your AI do?")
print("=" * 60)

tasks = ["easy", "medium", "hard"]

for task_name in tasks:
    print(f"\n{'='*60}")
    print(f"Testing: {task_name.upper()} Task")
    print('='*60)
    
    task = get_task(task_name)
    
    print(f"\n📧 CUSTOMER EMAIL:")
    print(f"   {task.customer_email}")
    
    print(f"\n🤖 AI RESPONSE:")
    ai_response = ask_ai(task.customer_email)
    print(f"   {ai_response}")
    
    print(f"\n📊 GRADING DETAILS:")
    
    # Check each criteria
    score = 0
    details = []
    
    # Length check
    length = len(ai_response)
    if task.min_length <= length <= task.max_length:
        score += 0.2
        details.append(f"   ✅ Length: {length} chars (Perfect!)")
    elif length < task.min_length:
        score += 0.1
        details.append(f"   ⚠️ Length: {length} chars (Too short)")
    else:
        score += 0.05
        details.append(f"   ⚠️ Length: {length} chars (Too long)")
    
    # Keywords found
    keywords_found = []
    for kw in task.expected_keywords:
        if kw.lower() in ai_response.lower():
            keywords_found.append(kw)
    keyword_score = (len(keywords_found) / len(task.expected_keywords)) * 0.4
    score += keyword_score
    details.append(f"   ✅ Keywords: {len(keywords_found)}/{len(task.expected_keywords)} found")
    details.append(f"      Found: {', '.join(keywords_found)}")
    
    # Forbidden words
    bad_words_found = []
    for bad in task.forbidden_words:
        if bad.lower() in ai_response.lower():
            bad_words_found.append(bad)
    if bad_words_found:
        score -= 0.2
        details.append(f"   ⚠️ WARNING: Used forbidden words: {', '.join(bad_words_found)}")
    else:
        details.append(f"   ✅ No forbidden words used!")
    
    # Professional tone
    polite_words = ["sorry", "apologize", "thank", "please", "help"]
    polite_found = [w for w in polite_words if w in ai_response.lower()]
    if polite_found:
        score += 0.2
        details.append(f"   ✅ Professional tone: Found '{polite_found[0]}'")
    
    # Final score
    final_score = grade_response(task, ai_response)
    details.append(f"\n   🎯 TOTAL SCORE: {final_score:.2f}/1.0")
    
    for detail in details:
        print(detail)
    
    if final_score >= 0.5:
        print(f"\n   ✅ RESULT: PASSED (Good job!)")
    else:
        print(f"\n   ❌ RESULT: FAILED (Needs improvement)")

print("\n" + "=" * 60)
print("🎯 PERFORMANCE SUMMARY")
print("=" * 60)