# environment.py - This is the playground where your AI learns!
# Think of it like a video game level for your AI robot

from pydantic import BaseModel  # This helps us organize data neatly
import random  # This helps us create different customer emails

# This defines what your AI "sees" (like the screen in a game)
class Observation(BaseModel):
    email: str  # The customer's email message
    current_response: str  # What your AI has written so far
    steps_taken: int  # How many attempts so far

# This defines what your AI can DO (like pressing buttons)
class Action(BaseModel):
    response_text: str  # What your AI wants to reply to the customer

# This is the MAIN PLAYGROUND where your AI practices
class SupportEnvironment:
    def __init__(self):
        """This sets up the playground when we start"""
        self.max_steps = 5  # AI gets 5 tries maximum
        self.steps = 0
        self.current_email = ""
        self.ai_response = ""
        
        # Our collection of customer emails (Easy, Medium, Hard)
        self.customer_emails = {
            "easy": "Hello! I forgot my password. Can you help me reset it?",
            "medium": "Hi, I've been charged twice for my subscription this month. Please refund one of them.",
            "hard": "Your app crashed 5 times today! I've lost all my work. I want a full refund and I'm very angry!"
        }
    
    def reset(self):
        """This starts a NEW GAME for your AI"""
        # Pick a random difficulty for practice
        difficulty = random.choice(["easy", "medium", "hard"])
        self.current_email = self.customer_emails[difficulty]
        self.ai_response = ""
        self.steps = 0
        
        # Return what the AI sees at the start
        return Observation(
            email=self.current_email,
            current_response="",
            steps_taken=0
        )
    
    def step(self, action):
        """
        This is where the AI TAKES AN ACTION
        action = what your AI wants to say
        """
        self.steps += 1
        
        # Save what the AI wrote
        self.ai_response = action.response_text
        
        # Check if AI's response is good
        reward = self._calculate_reward()
        
        # Is the game finished?
        done = self._is_done()
        
        # Extra info (like score details)
        info = {"feedback": "Your response was..."}
        
        # Create what the AI sees now
        observation = Observation(
            email=self.current_email,
            current_response=self.ai_response,
            steps_taken=self.steps
        )
        
        return observation, reward, done, info
    
    def _calculate_reward(self):
        """
        This is the SCORING SYSTEM (like getting candy!)
        Returns a score from 0.0 to 1.0
        """
        reward = 0.0
        
        # Rule 1: Longer responses are better (up to 0.3 points)
        if len(self.ai_response) > 50:
            reward += 0.3
        elif len(self.ai_response) > 20:
            reward += 0.15
        
        # Rule 2: Apologizing is good! (0.2 points)
        if "sorry" in self.ai_response.lower() or "apologize" in self.ai_response.lower():
            reward += 0.2
        
        # Rule 3: Offering help is good! (0.2 points)
        if "help" in self.ai_response.lower() or "assist" in self.ai_response.lower():
            reward += 0.2
        
        # Rule 4: Being mean is BAD! (penalty)
        if "stupid" in self.ai_response.lower() or "angry" in self.ai_response.lower():
            reward -= 0.5
        
        # Make sure reward stays between 0 and 1
        return max(0.0, min(1.0, reward))
    
    def _is_done(self):
        """Check if the game is over"""
        # Game ends if AI took too many steps
        if self.steps >= self.max_steps:
            return True
        
        # Game ends if AI gave a perfect response
        if self._calculate_reward() >= 0.8:
            return True
        
        return False
    
    def state(self):
        """Return the current state (for judges)"""
        return {
            "email": self.current_email,
            "response": self.ai_response,
            "steps": self.steps
        }
