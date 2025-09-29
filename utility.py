def get_default_user_profile():
    """Return default user profile"""
    return {
        'goals': [],
        'fitness_level': 'beginner',
        'preferences': [],
        'restrictions': [],
        'personal_info': {}
    }

def extract_user_info(message: str, user_profile: dict):
    """Extract user information and update profile"""
    message_lower = message.lower()
    profile_updated = False
    
    # Clear existing goals if user explicitly states new ones
    if any(phrase in message_lower for phrase in ["i want to", "my goal is", "i need to", "help me"]):
        # Only extract if user explicitly states goals
        if "lose weight" in message_lower or "weight loss" in message_lower:
            if "weight_loss" not in user_profile['goals']:
                user_profile['goals'] = ["weight_loss"]
                profile_updated = True
        elif "gain weight" in message_lower or "build muscle" in message_lower or "muscle gain" in message_lower:
            if "muscle_gain" not in user_profile['goals']:
                user_profile['goals'] = ["muscle_gain"]
                profile_updated = True
        elif "get fit" in message_lower or "general fitness" in message_lower:
            if "general_fitness" not in user_profile['goals']:
                user_profile['goals'] = ["general_fitness"]
                profile_updated = True
    
    # Only update fitness level if explicitly stated
    if "i am a beginner" in message_lower or "just starting" in message_lower:
        if user_profile['fitness_level'] != 'beginner':
            user_profile['fitness_level'] = 'beginner'
            profile_updated = True
    elif "i am intermediate" in message_lower or "have some experience" in message_lower:
        if user_profile['fitness_level'] != 'intermediate':
            user_profile['fitness_level'] = 'intermediate'
            profile_updated = True
    elif "i am advanced" in message_lower or "i am experienced" in message_lower:
        if user_profile['fitness_level'] != 'advanced':
            user_profile['fitness_level'] = 'advanced'
            profile_updated = True
    
    return profile_updated

def get_user_context(user_profile: dict) -> dict:
    """Get user context for prompt formatting"""
    return {
        'goals': ', '.join(user_profile['goals']) if user_profile['goals'] else 'Not specified',
        'fitness_level': user_profile['fitness_level'],
        'preferences': ', '.join(user_profile['preferences']) if user_profile['preferences'] else 'None specified',
        'restrictions': ', '.join(user_profile['restrictions']) if user_profile['restrictions'] else 'None'
    }