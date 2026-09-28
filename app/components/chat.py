import streamlit as st

from ai.core.agent import Agent


def analytics_chat(domain):

    st.divider()

    st.subheader("🤖 Analytics Assistant")

    st.markdown("""
    <style>
    /* Position Clear Chat beside the chat input */
    div[data-testid="stButton"] {
        position: fixed;
        bottom: 15px;
        right: 25px;
        z-index: 9999;
        width: auto !important;
    }

    div[data-testid="stButton"] button {
        width: auto !important;
        padding: 8px 14px;
    }
    </style>
    """, unsafe_allow_html=True)

    if st.button("🔄 Clear Chat"):
        st.session_state.pop(f"{domain}_chat_history", None)
        st.rerun()



    st.caption(
        f"Ask questions about {domain} analytics."
    )
   

    # =================================================
    # CREATE CUSTOMER AGENT
    # =================================================

    agent = Agent(
        openai_api_key=st.secrets["OPENAI_API_KEY"],
        domain=domain
    )
  
    # =================================================
    # SEPARATE HISTORY FOR EACH DOMAIN
    # =================================================

    chat_key = f"{domain}_chat_history"

    if chat_key not in st.session_state:

        st.session_state[chat_key] = []

    # =================================================
    # DISPLAY CHAT HISTORY
    # =================================================

    for message in st.session_state[chat_key]:

        with st.chat_message(
            message["role"]
        ):

            st.write(
                message["content"]
            )

    # =================================================
    # USER INPUT
    # =================================================

    question = st.chat_input(
        f"Ask something about {domain} analytics..."
    )

    # =================================================
    # PROCESS QUESTION
    # =================================================

    if question:

        # =============================================
        # STORE USER QUESTION
        # =============================================

        st.session_state[chat_key].append({

            "role": "user",

            "content": question

        })

        with st.chat_message("user"):

            st.write(question)

        # =============================================
        # ASK OPENAI
        # =============================================

        result = agent.ask(

            question=question,

            chat_history=st.session_state[chat_key],

            provider="openai"

        )

        # =============================================
        # GET RESULT
        # =============================================

        answer = result["answer"]

        insights = result["insights"]

        # =============================================
        # DISPLAY ANSWER
        # =============================================

        with st.chat_message("assistant"):

            st.markdown(answer)

            if insights:

                st.markdown("### Insights")

                st.markdown(insights)

        # =============================================
        # STORE AI ANSWER
        # =============================================

        st.session_state[chat_key].append({

            "role": "assistant",

            "content": answer

        })

        # =============================================
        # STORE AI INSIGHTS
        # =============================================

        if insights:

            st.session_state[chat_key].append({

                "role": "assistant",

                "content": insights

            })