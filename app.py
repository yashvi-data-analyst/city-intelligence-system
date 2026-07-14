import streamlit as st
import time

from Agents import agent

# ==================================================
# Page Config
# ==================================================

st.set_page_config(
    page_title="City Intelligence System",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# Session State
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==================================================
# CSS
# ==================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html,body,[class*="css"]{

font-family:'Poppins',sans-serif;

}

.stApp{

background:linear-gradient(
135deg,
#020617,
#0f172a,
#111827
);

}

section[data-testid="stSidebar"]{

background:#020617;

border-right:1px solid #1E293B;

}

.title{

text-align:center;

font-size:44px;

font-weight:700;

color:#38BDF8;

margin-top:15px;

}

.subtitle{

text-align:center;

font-size:18px;

color:#CBD5E1;

margin-bottom:35px;

}

.chat-card{

background:rgba(255,255,255,.05);

padding:18px;

border-radius:18px;

border:1px solid rgba(255,255,255,.08);

backdrop-filter:blur(15px);

margin-bottom:15px;

}

.footer{

text-align:center;

color:gray;

padding:20px;

}

</style>
""",unsafe_allow_html=True)

# ==================================================
# Header
# ==================================================

st.markdown("""

<div class='title'>

🌍 CITY INTELLIGENCE SYSTEM

</div>

<div class='subtitle'>

AI Powered Weather & News Assistant

</div>

""",unsafe_allow_html=True)

# ==================================================
# Sidebar
# ==================================================

with st.sidebar:

    st.image(
        "https://img.icons8.com/fluency/96/artificial-intelligence.png",
        width=90
    )

    st.title("AI Agent")

    st.success("🟢 Online")

    st.write("")

    st.info("Powered by LangChain + Mistral")

    st.divider()

    if st.button(
        "🗑 Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages=[]

        st.rerun()

st.divider()

# ==================================================
# Show Previous Messages
# ==================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ==================================================
# Chat Input
# ==================================================

prompt = st.chat_input(
    "Ask about weather or latest news..."
)


# ==================================================
# User Prompt
# ==================================================

if prompt:

    # Store User Message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user", avatar="👤"):

        st.markdown(prompt)

       # Assistant Response

    with st.chat_message("assistant", avatar="🤖"):

        thinking = st.empty()

        thinking.info("🤖 Thinking...")

        try:

            response = agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                }
            )

            thinking.empty()

            answer = ""

            for message in response["messages"]:

                if hasattr(message, "type"):

                    if message.type == "ai" and message.content:

                        answer = message.content

            placeholder = st.empty()

            final_text = ""

            for word in answer.split():

                final_text += word + " "

                placeholder.markdown(
                    f"""
<div class='chat-card'>

{final_text}▌

</div>
""",
                    unsafe_allow_html=True
                )

                time.sleep(0.02)

            placeholder.markdown(
                f"""
<div class='chat-card'>

{final_text}

</div>
""",
                unsafe_allow_html=True
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": final_text
                }
            )

        except Exception as e:

            thinking.empty()

            st.error(e)

# ==================================================
# Download Chat
# ==================================================

st.sidebar.divider()

chat_history = ""

for msg in st.session_state.messages:

    chat_history += (
        f"{msg['role'].upper()}\n"
        f"{msg['content']}\n\n"
    )

st.sidebar.download_button(
    "📥 Download Chat",
    data=chat_history,
    file_name="city_chat_history.txt",
    mime="text/plain",
    use_container_width=True
)

# ==================================================
# Conversation Statistics
# ==================================================

st.sidebar.divider()

st.sidebar.subheader("📊 Statistics")

user_count = len(
    [m for m in st.session_state.messages if m["role"] == "user"]
)

assistant_count = len(
    [m for m in st.session_state.messages if m["role"] == "assistant"]
)

st.sidebar.metric(
    "👤 User Messages",
    user_count
)

st.sidebar.metric(
    "🤖 AI Responses",
    assistant_count
)

# ==================================================
# Quick Prompts
# ==================================================

st.markdown("## 🚀 Quick Questions")

c1, c2 = st.columns(2)

with c1:

    if st.button(
        "🌤 Weather of Delhi",
        use_container_width=True
    ):

        st.session_state.messages.append(
            {
                "role":"user",
                "content":"What is the weather in Delhi?"
            }
        )

        st.rerun()

    if st.button(
        "🌤 Weather of Mumbai",
        use_container_width=True
    ):

        st.session_state.messages.append(
            {
                "role":"user",
                "content":"What is the weather in Mumbai?"
            }
        )

        st.rerun()

with c2:

    if st.button(
        "📰 Latest News of Bengaluru",
        use_container_width=True
    ):

        st.session_state.messages.append(
            {
                "role":"user",
                "content":"Latest news of Bengaluru"
            }
        )

        st.rerun()

    if st.button(
        "📰 Latest News of Jaipur",
        use_container_width=True
    ):

        st.session_state.messages.append(
            {
                "role":"user",
                "content":"Latest news of Jaipur"
            }
        )

        st.rerun()

# ==================================================
# About Project
# ==================================================

st.markdown("---")

with st.expander("ℹ About City Intelligence System"):

    st.markdown("""
### 🚀 Features

- 🌤 Real-Time Weather
- 📰 Latest News
- 🤖 AI Agent (Mistral)
- 🔎 Tavily Search
- 🛡 Human Approval Middleware
- 💬 Chat Interface
- 📥 Download Chat
- 🌙 Modern Dark UI
""")
    
# ==================================================
# Footer
# ==================================================

st.markdown("---")

st.markdown(
    """
    <div class="footer">
        ❤️ Made with Streamlit • LangChain • Mistral AI • Tavily
    </div>
    """,
    unsafe_allow_html=True
)