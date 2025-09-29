import streamlit as st
from chatbot import FitnessCoachChatbot
from config import *
from utility import get_default_user_profile

def setup_sidebar():
    with st.sidebar:
        st.title("GetFitBot 💪")
        st.subheader("Your Profile")
        selected_goals = st.multiselect(
            "Your Fitness Goals:",
            options=list(GOALS_OPTIONS.keys()),
            format_func=lambda x: GOALS_OPTIONS[x],
            default=st.session_state.user_profile['goals'])
        # Fitness level
        fitness_level = st.selectbox(
            "Your Fitness Level:",
            options=FITNESS_LEVELS,
            index=FITNESS_LEVELS.index(st.session_state.user_profile['fitness_level']))
        
        # Preferences
        preferences = st.multiselect("Activities You Enjoy:",PREFERENCES_OPTIONS, default=st.session_state.user_profile['preferences'])
        # Restrictions
        restrictions = st.multiselect("Activities to Avoid:", RESTRICTIONS_OPTIONS, default=st.session_state.user_profile['restrictions'])
        # Update profile button
        if st.button("Update Profile", type="primary", use_container_width=True):
            st.session_state.user_profile['goals'] = selected_goals
            st.session_state.user_profile['fitness_level'] = fitness_level
            st.session_state.user_profile['preferences'] = preferences
            st.session_state.user_profile['restrictions'] = restrictions
            st.success("Profile updated!")
        
        # Display current profile
        st.subheader("Current Profile")
        profile = st.session_state.user_profile
        if profile['goals']:
            st.write("**Goals:**")
            for goal in profile['goals']:
                st.write(f"• {GOALS_OPTIONS.get(goal, goal.replace('_', ' ').title())}")
        else:
            st.write("❌ **Goals:** Not set - Please select at least one goal")
        st.write(f"**Fitness Level:** {profile['fitness_level'].title()}")
        
        if profile['preferences']:
            st.write("**Likes:**")
            for pref in profile['preferences']:
                st.write(f"• {pref.title()}")
        
        if profile['restrictions']:
            st.write("**Avoids:**")
            for restriction in profile['restrictions']:
                st.write(f"• {restriction.replace('no ', '').title()}")
        
        # Profile completion status
        if not profile['goals']:
            st.error("⚠️ Profile incomplete! Please select your fitness goals.")
        else:
            st.success("✅ Profile complete!")
        
        # Memory stats
        memory_count = len(st.session_state.chatbot.memory.chat_memory.messages) // 2
        st.write(f"**Conversations:** {memory_count}")

def setup_quick_actions():
    st.markdown("---")
    st.subheader("Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏃‍♂️ Workout Plan", use_container_width=True):
            if not st.session_state.user_profile['goals']:
                st.error("Please complete your profile first!")
                st.rerun()
            prompt = "Create a workout plan for me according to my profile"
            st.session_state.messages.append({"role": "user", "content": prompt})
            response = st.session_state.chatbot.generate_response(prompt, st.session_state.user_profile)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col2:
        if st.button("🥗 Diet Plan", use_container_width=True):
            if not st.session_state.user_profile['goals']:
                st.error("Please complete your profile first!")
                st.rerun()
            prompt = "Create a diet plan for me according to my profile"
            st.session_state.messages.append({"role": "user", "content": prompt})
            response = st.session_state.chatbot.generate_response(prompt, st.session_state.user_profile)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col3:
        if st.button("🎯 Set Goals", use_container_width=True):
            if not st.session_state.user_profile['goals']:
                st.error("Please complete your profile first!")
                st.rerun()
            prompt = "Help me set fitness goals according to my profile"
            st.session_state.messages.append({"role": "user", "content": prompt})
            response = st.session_state.chatbot.generate_response(prompt, st.session_state.user_profile)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

def main():
    st.set_page_config(page_title="FitBot - AI Fitness Coach",page_icon="💪",layout="wide")
    
    # Initialize the chatbot
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = FitnessCoachChatbot()
    # Initialize session state variables
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = get_default_user_profile()
    setup_sidebar()
    
    # Main chat interface
    st.title("💪 FitBot - Your AI Fitness Coach")
    # Show warning if profile is not set
    if not st.session_state.user_profile['goals']:
        st.warning("🚨 **Please complete your profile in the sidebar before chatting!** I need to know your fitness goals to provide personalized advice.")
    else:
        st.markdown("Welcome! I'm your personal AI fitness coach. I'll help you with workouts, nutrition, and achieving your fitness goals!")
    st.info("💡 **Note:** Your conversation and profile will reset when you refresh the page.")
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    # Chat input
    if prompt := st.chat_input("Ask me about fitness, workouts, nutrition, or your goals..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate and display bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.chatbot.generate_response(prompt, st.session_state.user_profile)
            st.write(response)
        # Add bot response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    # Setup quick actions
    setup_quick_actions()

if __name__ == "__main__":
    main()
