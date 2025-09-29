from langchain_groq import ChatGroq
from langchain.memory import ConversationSummaryBufferMemory
from langchain.schema import HumanMessage, AIMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import LLMChain
import streamlit as st
from config import *
from utility import extract_user_info, get_user_context

class FitnessCoachChatbot:
    def __init__(self):
        if not GROQ_API_KEY:
            st.error("❌ GROQ_API_KEY not found in environment variables. Please add it to your .env file.")
            st.stop()
        
        # Initialize LangChain components
        self.setup_llm()
        self.setup_memory()
        self.setup_conversation_chain()
    
    def setup_llm(self):
        """Initialize the Groq Llama 3 model"""
        self.llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name=MODEL_NAME,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            streaming=False
        )
    
    def setup_memory(self):
        """Setup LangChain memory for conversation context"""
        self.memory = ConversationSummaryBufferMemory(
            llm=self.llm,
            max_token_limit=MEMORY_LIMIT,
            return_messages=True,
            memory_key="chat_history"
        )
    
    def setup_conversation_chain(self):
        """Setup the conversation chain with custom prompt"""
        
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])
    
    def generate_response(self, user_input: str, user_profile: dict) -> str:
        """Generate response using Llama 3 via Groq with LangChain"""
        
        # Check if user profile is complete (at least one goal selected)
        if not user_profile['goals']:
            return "👋 Welcome! I see you haven't set up your fitness profile yet. To provide you with personalized fitness advice, please go to the sidebar and:\n\n1. **Select your fitness goals** (Lose Weight, Build Muscle, or General Fitness)\n2. **Choose your fitness level**\n3. **Update your profile**\n\nOnce you've set up your profile, I'll be able to give you customized workout and nutrition plans!"
        
        # Extract user information (simplified)
        profile_updated = extract_user_info(user_input, user_profile)
        
        # Get user context
        context = get_user_context(user_profile)
        
        try:
            # Create LLM chain for this specific request
            chain = LLMChain(
                llm=self.llm,
                prompt=self.prompt_template,
                verbose=False
            )
            
            # Prepare all input variables
            input_variables = {
                'input': user_input,
                'goals': context['goals'],
                'fitness_level': context['fitness_level'],
                'preferences': context['preferences'],
                'restrictions': context['restrictions']
            }
            
            # Load memory variables
            memory_variables = self.memory.load_memory_variables({})
            input_variables.update(memory_variables)
            
            # Generate response
            response = chain.invoke(input_variables)
            
            # Save messages to memory
            self.memory.chat_memory.add_user_message(user_input)
            self.memory.chat_memory.add_ai_message(response['text'])
            
            return response['text']
            
        except Exception as e:
            error_msg = f"I apologize, but I'm experiencing a technical issue. Please try again. Error: {str(e)}"
            st.error(f"API Error: {str(e)}")
            return error_msg