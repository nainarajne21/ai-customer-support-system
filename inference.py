# inference.py - MOCK VERSION (No API Key Needed!)
# This pretends to be an AI - perfect for testing!

from environment import SupportEnvironment, Action
from tasks import get_task, grade_response

# ============ MOCK AI FUNCTION ============
def ask_ai(customer_email: str, current_response: str = "") -> str:
    """
    This is a MOCK AI - it gives pre-written responses!
    """
    
    # Pre-written good responses for each type of problem
    if "password" in customer_email.lower():
        return "I'm sorry you forgot your password! Please click the 'Forgot Password' link on our login page. You'll receive an email with reset instructions within 5 minutes. Let me know if you need any help!"
    
    elif "charged twice" in customer_email.lower() or "double" in customer_email.lower():
        return "I apologize for the double charge! I've processed a refund for the duplicate payment. You should see the credit in your account within 3-5 business days. Thank you for your patience!"
    
    elif "crash" in customer_email.lower() or "angry" in customer_email.lower():
        return "I'm truly sorry to hear about the crashes - that sounds incredibly frustrating! I understand you've lost work and I want to help. I've issued a full refund, and our technical team will investigate what caused the crashes. Please accept my sincere apologies!"
    
    else:
        return "Thank you for reaching out! We're here to help. Could you please provide more details so I can assist you better?"

def run_task(task_name: str):
    """
    Run a single task with the MOCK AI!
    """
    
    task = get_task(task_name)
    env = SupportEnvironment()
    
    env.current_email = task.customer_email
    env.steps = 0
    env.ai_response = ""
    
    print(f"[START] task={task_name} env=support_system model=mock-ai")
    
    rewards = []
    max_steps = 3
    
    for step_num in range(1, max_steps + 1):
        
        ai_response = ask_ai(task.customer_email, env.ai_response)
        action = Action(response_text=ai_response)
        observation, reward, done, info = env.step(action)
        rewards.append(reward)
        
        short_action = ai_response[:50] + "..." if len(ai_response) > 50 else ai_response
        print(f"[STEP] step={step_num} action={short_action} reward={reward:.2f} done={str(done).lower()} error=null")
        
        if done:
            break
    
    final_score = grade_response(task, env.ai_response)
    success = final_score >= 0.5
    rewards_str = ",".join([f"{r:.2f}" for r in rewards])
    
    print(f"[END] success={str(success).lower()} steps={len(rewards)} rewards={rewards_str}")
    
    return success, final_score

def main():
    print("=" * 50)
    print("🤖 AI Customer Support System (MOCK VERSION)")
    print("=" * 50)
    print("Note: This uses pre-written responses for testing!\n")
    
    tasks = ["easy", "medium", "hard"]
    results = {}
    
    for task_name in tasks:
        print(f"\n--- Running {task_name.upper()} task ---")
        success, score = run_task(task_name)
        results[task_name] = {"success": success, "score": score}
        print(f"Score: {score:.2f}/1.0")
    
    print("\n" + "=" * 50)
    print("📊 FINAL RESULTS")
    print("=" * 50)
    for task_name, result in results.items():
        status = "✅ PASSED" if result["success"] else "❌ FAILED"
        print(f"{task_name.upper()}: {status} (Score: {result['score']:.2f})")
    
    passed = sum(1 for r in results.values() if r["success"])
    print(f"\nTotal: {passed}/3 tasks passed")

if __name__ == "__main__":
    main()