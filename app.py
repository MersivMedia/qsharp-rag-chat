import os
from dotenv import load_dotenv
from pinecone import Pinecone
from openai import OpenAI
from anthropic import Anthropic
from typing import List, Dict, Any
import streamlit as st
from operator import attrgetter
from streamlit.components.v1 import html

# Load environment variables
load_dotenv()

# Custom CSS
st.markdown("""
<style>
    /* Dark theme with quantum blue accents */
    .stApp {
        background-color: #0a0f18 !important;
    }
    
    /* Chat input placeholder color */
    .stChatInput textarea::placeholder {
        color: #00b4ff !important;
        opacity: 0.7;
    }
    
    /* All text elements */
    .stApp, .stMarkdown, div[data-testid="stMarkdownContainer"] p, .stChatMessage {
        color: #ffffff !important;
    }
    
    /* Chat messages and input */
    .stChatMessage, .stChatInput {
        background-color: #141c2b !important;
        border: 1px solid #00b4ff !important;
        box-shadow: 0 0 10px rgba(0, 180, 255, 0.1) !important;
        width: 650px !important;  /* Set fixed width for both */
        margin: 0 auto !important;
        padding-right: 20px !important;  /* Add more padding on right side */
    }
    
    /* Chat input styling */
    section[data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 100px !important;
        left: 0 !important;
        right: 0 !important;
        background-color: #0a0a0a !important;
        padding: 0 !important;
        z-index: 999 !important;
    }
    
    /* Control text input width */
    .stChatInput > div {
        width: 650px !important;  /* Match chat message width */
        margin: 0 auto !important;
        padding: 0 !important;
    }
    
    /* Ensure the text input itself is properly contained */
    .stChatInput textarea {
        width: 100% !important;
        box-sizing: border-box !important;
        color: #ffffff !important;
        background-color: #141c2b !important;
        border: 1px solid #00b4ff !important;
        padding: 8px 12px !important;
    }
    
    /* Container for the input background */
    div[data-testid="stChatInputContainer"] {
        width: 650px !important;  /* Match chat message width */
        margin: 0 auto !important;
        padding: 0 !important;
    }
    
    /* Style placeholder text */
    .stChatInput textarea::placeholder {
        color: #00b4ff !important;
        opacity: 0.7 !important;
    }
    
    /* Remove white background from chat container */
    .stChatContainer, div[data-testid="stChatMessageInput"] {
        background-color: #0a0a0a !important;
    }
    
    /* Buttons and interactive elements */
    .stButton>button {
        background-color: #141c2b !important;
        color: #00b4ff !important;
        border: 1px solid #00b4ff !important;
    }
    
    /* Expandable sections */
    .streamlit-expanderHeader {
        background-color: #1a1a1a !important;
        color: #00ff00 !important;
        border: 1px solid #00ff00 !important;
    }
    
    /* Headers */
    h1, h2, h3, [data-testid="stHeader"] {
        color: #ffffff !important;
        text-shadow: 0 0 10px rgba(0, 180, 255, 0.3) !important;
    }
    
    /* Center main title only */
    .stApp > header + div [data-testid="stMarkdownContainer"] > div:first-child > h1 {
        text-align: center !important;
        width: 100% !important;
        margin: 20px 0 !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #00ff00 !important;
    }
    
   
    /* Disclaimer modal */
    .disclaimer-modal {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0.8);
        z-index: 999;
    }
    
    .disclaimer-content {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: #141c2b;
        padding: 2rem;
        border: 2px solid #00b4ff;
        border-radius: 10px;
        z-index: 1000;
        max-width: 600px;
        text-align: center;
        color: white;
    }
    
    .disclaimer-content button {
        background-color: #00b4ff;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        margin-top: 20px;
    }
    
    .disclaimer-content button:hover {
        background-color: #0077ff;
    }
    
    /* Sticky Footer */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0a0f18;
        color: #ffffff;
        text-align: center;
        padding: 10px 0;
        border-top: 1px solid #00b4ff;
        z-index: 998;
    }
    
    .footer a {
        color: #00b4ff;
        text-decoration: none;
    }
    
    .footer a:hover {
        text-decoration: underline;
    }
    
    .social-icons {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-bottom: 5px;
    }
    
    .social-icons svg {
        width: 24px;
        height: 24px;
        fill: #00b4ff;
        transition: fill 0.3s ease;
    }
    
    .social-icons a:hover svg {
        fill: #66d9ff;
    }
    
    /* Add padding to main content to prevent footer overlap */
    .main-content {
        padding-bottom: 50px !important;
    }
    
    /* Adjust chat input position */
    section[data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 70px !important;
        left: 0 !important;
        right: 0 !important;
        background-color: #0a0a0a !important;
        padding: 20px !important;
        z-index: 999 !important;
    }
    
    /* Force black background on all chat-related elements */
    .st-emotion-cache-128upt6,
    .st-emotion-cache-12cetgn,
    .st-emotion-cache-0,
    .st-emotion-cache-b95f0i,
    .st-emotion-cache-1n76uvr,
    .st-emotion-cache-ke1f9q,
    .st-emotion-cache-1wpj71q,
    .st-emotion-cache-s1k4sy,
    div[data-testid="stBottomBlockContainer"],
    div[data-testid="stVerticalBlockBorderWrapper"],
    .stVerticalBlock,
    .stElementContainer {
        background-color: #0a0f18 !important;
    }

    section[data-testid="stChatInput"] > div {
        background-color: #0a0a0a !important;
    }
    
    div[data-testid="stChatMessageInput"] > div {
        background-color: #0a0a0a !important;
    }
    
    /* Adjust main chat container to not overlap with fixed input */
    .stChatContainer {
        margin-bottom: 100px !important;
        background-color: #0a0a0a !important;
        overflow-y: auto !important;
        height: auto !important;
        min-height: 100vh !important;
        padding: 0 20px !important;
    }
    
    /* Ensure all backgrounds are black */
    .stMarkdown, .stChatMessage, div[class*="stChatInput"] {
        background-color: #0a0a0a !important;
    }

    /* Additional container styling */
    div[data-testid="stBottomBlockContainer"] {
        position: fixed !important;
        bottom: 120px !important;
        z-index: 998 !important;
        width: 100% !important;
    }

    /* Ensure content is scrollable */
    .main .block-container {
        padding-bottom: 300px !important;
        overflow-y: auto !important;
        height: auto !important;
    }

    /* Style scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        background-color: #0a0a0a;
    }

    ::-webkit-scrollbar-thumb {
        background-color: #00b4ff;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-track {
        background-color: #141c2b;
    }

    /* Ensure expandable sections are fully visible */
    .streamlit-expanderContent {
        background-color: #0a0a0a !important;
        margin-bottom: 10px !important;
    }

    /* Main app container */
    .stApp {
        height: 100vh !important;
        overflow-y: auto !important;
        padding: 0 20px !important;
    }

    /* Chat message container */
    .stChatMessage {
        margin-bottom: 20px !important;
    }

    /* Message content */
    .stMarkdown {
        overflow: visible !important;
    }

    /* Ensure input container matches exact width */
    div[data-testid="stBottomBlockContainer"] {
        width: 650px !important;
        margin: 0 auto !important;
    }

    /* Remove any flex spacing */
    .stVerticalBlock {
        gap: 0 !important;
    }

    /* Ensure chat message container aligns with input */
    .stChatMessage {
        margin-left: auto !important;
        margin-right: auto !important;
        box-sizing: border-box !important;
    }

    .stChatMessage {
        padding-bottom: 3.5rem !important;  /* Increased padding below messages */
    }
    
    /* Update placeholder text */
    .stChatInput textarea::placeholder {
        content: "Ask a question about q# coding" !important;
    }

    /* Make header dark */
    header[data-testid="stHeader"] {
        background-color: #0a0f18 !important;
    }

    /* Style header buttons and menu items */
    .stDeployButton, 
    button[kind="header"],
    .stDecoration {
        background-color: #141c2b !important;
        color: #00b4ff !important;
        border-color: #00b4ff !important;
    }

    /* Style dropdown menu */
    div[data-testid="stToolbar"],
    div[class*="stToolbar"] {
        background-color: #0a0f18 !important;
    }

    [data-testid="collapsedControl"] {
        display: none;
    }
    
    section[data-testid="stSidebar"] {
        display: none;
    }
    
    /* Ensure the app takes full width */
    .main > .block-container {
        max-width: 100%;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    /* Adjust chat input position */
    section[data-testid="stChatInput"] {
        padding-bottom: 0.2rem !important;  /* Reduced space between input and footer */
        position: fixed !important;
        bottom: 2.5rem !important;  /* Moved closer to footer */
        background: transparent !important;
    }

    /* Ensure messages don't get hidden behind input */
    [data-testid="stChatMessageContainer"] {
        padding-bottom: 9rem !important;  /* Increased padding to prevent cutoff */
    }

    /* Adjust main chat container height and position */
    [data-testid="stChatMessageContainer"] {
        height: calc(100vh - 180px) !important;  /* Reduced height to leave space for input */
        overflow-y: auto !important;
        margin-bottom: 100px !important;  /* Space for input and footer */
    }

    /* Adjust chat input position */
    section[data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 2.5rem !important;
        background: transparent !important;
        padding: 0.5rem !important;
        width: 100% !important;
    }

    /* Add padding to messages */
    .stChatMessage {
        padding: 1rem !important;
    }

    /* Main container adjustments */
    .main > .block-container {
        padding-bottom: 0px !important;
    }

    /* Chat message container */
    [data-testid="stChatMessageContainer"] {
        height: calc(100vh - 180px) !important;
        max-height: calc(100vh - 180px) !important;
        overflow-y: auto !important;
        margin-bottom: 120px !important;  /* Increased margin to prevent overlap */
    }

    /* Individual message styling */
    .stChatMessage {
        padding: 1rem !important;
        margin-bottom: 1rem !important;
        padding-bottom: 2rem !important;  /* Added extra padding at bottom of messages */
    }

    /* Chat input container */
    section[data-testid="stChatInput"] {
        position: fixed !important;
        bottom: 50px !important;
        left: 0 !important;
        right: 0 !important;
        background: var(--background-color) !important;
        padding: 1rem !important;
        z-index: 1000 !important;
    }

    /* Ensure proper stacking */
    .stChatFloating {
        bottom: 40px !important;
    }


    /* Footer adjustments */
    footer {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 40px !important;
        z-index: 999 !important;
    }

    /* Regular message styling */
    .stChatMessage {
        margin-bottom: 20px !important;
    }

    /* Message content */
    .stMarkdown {
        overflow: visible !important;
    }

    /* Main chat container */
    .stChatContainer {
        margin-bottom: 100px !important;
        overflow-y: auto !important;
        height: auto !important;
        min-height: 100vh !important;
        padding: 0 20px !important;
    }

    /* Regular message styling */
    .stChatMessage {
        margin-bottom: 20px !important;
    }

    /* Message content */
    .stMarkdown {
        overflow: visible !important;
    }

    /* Remove padding from chat input container */
    div[data-testid="stChatInputContainer"] {
        padding: 0 !important;
        margin: 0 !important;
        width: 650px !important;
        margin: 0 auto !important;
    }

    /* Ensure chat input matches width */
    section[data-testid="stChatInput"] {
        width: 650px !important;
        margin: 0 auto !important;
        padding: 0 !important;
    }

    /* Ensure content is scrollable */
    .main .block-container {
        overflow-y: auto !important;
        height: auto !important;
    }

    /* Main chat container */
    .stChatContainer {
        margin-bottom: 100px !important;
        overflow-y: auto !important;
        height: auto !important;
        min-height: 100vh !important;
        padding: 0 20px !important;
    }

    /* Regular message styling */
    .stChatMessage {
        margin-bottom: 20px !important;
        width: 650px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }

    /* Message content */
    .stMarkdown {
        overflow: visible !important;
    }

    /* Extra padding for assistant messages */
    div[data-testid="stChatMessageContent"][aria-label="Chat message from assistant"] {
        padding-bottom: 120px !important;
    }

    /* Remove all padding from bottom block container and its children */
    div[data-testid="stBottomBlockContainer"],
    div[data-testid="stVerticalBlockBorderWrapper"],
    .st-emotion-cache-b95f0i,
    .stVerticalBlock,
    .stElementContainer {
        padding: 0 !important;
        margin: 0 !important;
    }

    /* Ensure input container matches exact width */
    div[data-testid="stBottomBlockContainer"] {
        width: 650px !important;
        margin: 0 auto !important;
    }

    /* Remove any flex spacing */
    .stVerticalBlock {
        gap: 0 !important;
    }

    /* Ensure chat message container aligns with input */
    .stChatMessage {
        margin-left: auto !important;
        margin-right: auto !important;
        box-sizing: border-box !important;
    }

    /* Ensure content is scrollable */
    .main .block-container {
        overflow-y: auto !important;
        height: auto !important;
    }
</style>

<div id="disclaimerModal" class="disclaimer-modal">
    <div class="disclaimer-content">
        <h2 style="color: #00b4ff;">Welcome to QSharp Quantum Computing</h2>
        <p>This is a RAG (Retrieval-Augmented Generation) AI chat application designed to assist with Q# programming questions and explore quantum computing research.</p>
        <p>The AI uses a curated knowledge base of Q# documentation, quantum computing papers, and best practices to provide accurate and helpful responses.</p>
        <div style="margin-top: 2rem;">
            <button 
                style="
                    background-color: #141c2b;
                    color: #00b4ff;
                    border: 1px solid #00b4ff;
                    padding: 0.5rem 1rem;
                    margin-top: 1rem;
                    cursor: pointer;
                    border-radius: 5px;
                    display: inline-block;
                "
                onclick="document.querySelector('[data-testid=\\'stButton\\'] button').click();"
            >
                Got it!
            </button>
        </div>
    </div>
</div>

<script>
    function showDisclaimer() {
        document.getElementById('disclaimerModal').style.display = 'block';
    }
    
    function hideDisclaimer() {
        document.getElementById('disclaimerModal').style.display = 'none';
        localStorage.setItem('disclaimerAccepted', 'true');
    }
    
    // Show disclaimer on first load
    if (!localStorage.getItem('disclaimerAccepted')) {
        showDisclaimer();
    }
    
    // Handle disclaimer acceptance
    document.querySelector('.disclaimer-content button').addEventListener('click', function() {
        localStorage.setItem('disclaimerAccepted', 'true');
        hideDisclaimer();
    });
</script>
""", unsafe_allow_html=True)

# Initialize clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENVIRONMENT")
)

# Get Pinecone index
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

def create_embedding(text: str) -> List[float]:
    """Create embedding using OpenAI's text-embedding-3-small."""
    response = openai_client.embeddings.create(
        input=text,
        model=os.getenv("OPENAI_EMBEDDING_MODEL")
    )
    return response.data[0].embedding

def get_ai_response(query: str, results: list) -> str:
    """Generate a comprehensive response using Claude."""
    if not results:
        return "I couldn't find any relevant information in the documents."
    
    # Prepare context from results
    context_parts = []
    for i, result in enumerate(results, 1):
        if hasattr(result, 'metadata') and result.metadata:
            source = f"Source {i}: {result.metadata.get('file_name', 'Unknown')}, {result.metadata.get('source', 'Unknown')}"
            text = result.metadata.get('text', '')
            summary = result.metadata.get('summary', '')
            context_parts.append(f"{source}\nText: {text}\nSummary: {summary}\n")
    
    context = "\n\n".join(context_parts)
    
    # Generate response using Claude
    prompt = f"""Based on the following sources, please provide a comprehensive answer to this question: "{query}"

Context:
{context}

Please synthesize the information and provide a clear, well-structured response. Do not include any citations or source references in your response.

Response:"""

    response = anthropic_client.messages.create(
        model=os.getenv("ANTHROPIC_MODEL"),
        max_tokens=1000,
        temperature=0.7,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    
    return response.content[0].text

def search_all_namespaces(query: str, top_k: int = 5):
    """Search for similar vectors across all namespaces"""
    try:
        # Get query embedding
        query_embedding = create_embedding(query)
        
        # Get all namespaces
        stats = index.describe_index_stats()
        namespaces = list(stats.namespaces.keys())
        
        all_results = []
        
        # Search in each namespace
        for namespace in namespaces:
            results = index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                namespace=namespace
            )
            
            # Add namespace information to each result
            for match in results.matches:
                match.namespace = namespace
            
            all_results.extend(results.matches)
        
        # Sort all results by score and take top_k
        all_results.sort(key=attrgetter('score'), reverse=True)
        return all_results[:top_k]
    
    except Exception as e:
        st.error(f"Error searching vectors: {str(e)}")
        return []

def show_disclaimer():
    if 'disclaimer_accepted' not in st.session_state:
        disclaimer_container = st.empty()
        with disclaimer_container.container():
            # Wider center column
            col1, col2, col3 = st.columns([0.5, 6, 0.5])
            with col2:
                st.markdown("""
                    <div style="
                        background-color: rgba(0, 0, 0, 0.8);
                        position: fixed;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        z-index: 1000001;
                    ">
                        <div style="
                            background-color: #141c2b;
                            padding: 2rem 2rem 4rem 2rem;
                            border: 2px solid #00b4ff;
                            border-radius: 10px;
                            text-align: center;
                            position: fixed;
                            top: 50%;
                            left: 50%;
                            transform: translate(-50%, -50%);
                            z-index: 1000002;
                            width: 100%;
                            max-width: 800px;
                        ">
                            <h2 style="color: #00b4ff;">Welcome to QSharp Quantum Computing</h2>
                            <p style="color: white;">This is a RAG (Retrieval-Augmented Generation) AI chat application designed to assist with Q# programming questions and explore quantum computing research.</p>
                            <p style="color: white;">The AI uses a curated knowledge base of Q# documentation, quantum computing papers, and best practices to provide accurate and helpful responses.</p>
                        </div>
                    </div>

                    <style>
                        /* Force chat input below overlay */
                        section[data-testid="stChatInput"] {
                            z-index: 999 !important;
                        }

                        /* Style the Streamlit button */
                        .element-container:has([data-testid="stButton"]) {
                            position: fixed !important;
                            z-index: 1000003 !important;
                            top: 50%;
                            left: 50%;
                            transform: translate(-50%, 80px);
                            width: auto !important;
                            text-align: center !important;
                            display: flex !important;
                            justify-content: center !important;
                        }
                        
                        [data-testid="stButton"] {
                            display: flex !important;
                            justify-content: center !important;
                            width: 100% !important;
                        }
                        
                        [data-testid="stButton"] button {
                            background-color: #141c2b !important;
                            color: #00b4ff !important;
                            border: 1px solid #00b4ff !important;
                            padding: 0.5rem 1rem !important;
                            border-radius: 5px !important;
                            display: inline-block !important;
                            width: auto !important;
                            margin: 0 auto !important;
                        }
                    </style>
                """, unsafe_allow_html=True)
                
                if st.button("Got it!", key="disclaimer_button"):
                    st.session_state.disclaimer_accepted = True
                    disclaimer_container.empty()


def main():
    st.title("QSharp AI Researcher Chat V1")
    
    # Show disclaimer
    show_disclaimer()
    
    # Set fixed number of results
    top_k = 10
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "results" in message:
                st.write("---")
                st.write("Sources:")
                for i, result in enumerate(message["results"], 1):
                    with st.expander(f"Source {i}"):
                        if hasattr(result, 'metadata') and result.metadata:
                            st.write(f"**File:** {result.metadata.get('file_name', 'Unknown')}")
                            st.write(f"**Location:** {result.metadata.get('source', 'Unknown')}")
                            st.write("**Summary:**")
                            st.write(result.metadata.get('summary', 'No summary available'))
                            st.write("**Full Text:**")
                            st.write(result.metadata.get('text', 'No text available'))
    
    # Chat input
    if prompt := st.chat_input(placeholder="Ask a question about q# coding"):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get response
        with st.chat_message("assistant"):
            with st.spinner("Searching documents..."):
                results = search_all_namespaces(prompt, top_k)
            
            if results:
                with st.spinner("Generating response..."):
                    response = get_ai_response(prompt, results)
                st.write(response)
            else:
                response = "I couldn't find any relevant information in the documents."
                st.write(response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "results": results
            })

    # Add footer
    st.markdown("""
    <div class="footer">
        <div class="social-icons">
            <a href="https://x.com/greptheloot" target="_blank">
                <svg viewBox="0 0 24 24">
                    <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                </svg>
            </a>
            <a href="https://github.com/mersivmedia" target="_blank">
                <svg viewBox="0 0 24 24">
                    <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
                </svg>
            </a>
            <a href="https://app.virtuals.io/prototypes/0xb4a798A8CcE289De0A0E1c881DfbC515858930D2" target="_blank">
                <svg width="28" height="28" viewBox="0 0 56 56" xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd" d="M33.98 19.75a7.14 7.14 0 0 0-2.47-2.78 6.53 6.53 0 0 0-6.55-.2 7.42 7.42 0 0 0-3.11 3.03 6.1 6.1 0 0 0-.64 4.61c.25 1 .73 1.93 1.44 2.81a8.42 8.42 0 0 0 6.78 3.17.1.1 0 0 1 .09.06.1.1 0 0 1 0 .1 25.73 25.73 0 0 1-2.37 4.1c-.04.05-.08.05-.12-.01a98.5 98.5 0 0 0-.76-1.16l-.04-.06-.1-.15a27.28 27.28 0 0 0-4.22-4.9 25.12 25.12 0 0 0-10.29-5.81c-.32-.1-.96-.22-1.94-.39-.18-.03-.31-.02-.4.02-.2.09-.3.23-.28.44.02.2.12.35.31.45A31.14 31.14 0 0 1 23.6 37.93l.12.26a110.53 110.53 0 0 1 .32.74c.2.45.36.77.5.95.38.5.88.83 1.52 1 1.13.3 2.1.04 2.89-.79a26.67 26.67 0 0 0 3.16-4.14 22.8 22.8 0 0 0 2.79-6.42.2.2 0 0 1 .12-.14 24.52 24.52 0 0 0 7.74-4.7c.17-.15.27-.27.29-.36a.53.53 0 0 0-.07-.42c-.08-.15-.2-.22-.36-.2a.73.73 0 0 0-.32.1 25.44 25.44 0 0 1-6.85 2.93c-.05.01-.07 0-.07-.06.1-2.08-.2-4.08-.94-6a7.72 7.72 0 0 0-.45-.93Zm-4.66 7.49 1.24.16h.04c.02-.02.03-.03.03-.05.32-1.27.4-2.54.24-3.81a5.93 5.93 0 0 0-1.1-2.8 2.26 2.26 0 0 0-2.1-.85c-.81.08-1.5.43-2.05 1.06-.75.85-.93 1.81-.54 2.9.33.95.88 1.72 1.64 2.3.72.57 1.59.93 2.6 1.09Z" fill="#00b4ff"/>
                    <path d="M44.64 21.74c.17-.16.39-.28.64-.36.27-.09.52-.11.77-.08.6.07.92.41.95 1.03.02.38-.09.73-.32 1.05-.22.3-.51.5-.87.61a.96.96 0 0 1-.82-.1c-.23-.14-.4-.37-.49-.67-.1-.33-.15-.6-.15-.8 0-.28.1-.5.29-.68Z" fill="#00b4ff"/>
                </svg>
            </a>
        </div>
        <a href="https://mersivmedia.com" target="_blank">Made by Mersiv Media</a>
    </div>
    """, unsafe_allow_html=True)

    # Add a help button in the sidebar
    if st.sidebar.button("❔ Help"):
        show_disclaimer()

if __name__ == "__main__":
    main() 