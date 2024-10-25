import streamlit as st

# Initialize session state variables
if "screen" not in st.session_state:
    st.session_state.screen = "intro"
    st.session_state.score = 0
    st.session_state.answers = {}

# CSS styling for larger font and button adjustments
st.markdown(
    """
    <style>
    .big-font {
        font-size:20px !important;
    }
    .header-font {
        font-size:26px !important;
        font-weight: bold;
    }
    .subheader-font {
        font-size:22px !important;
        font-weight: bold;
    }
    .button-style {
        font-size:18px !important;
        margin-top: 20px;
        padding: 10px 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Training content sections
training_content = [
    {
        "title": "1. Password Management",
        "content": """
            Strong passwords are essential to secure your online accounts.
            Use unique, complex passwords for each account and consider using a password manager.
            Avoid common words and use a mix of uppercase, lowercase, numbers, and symbols.
        """
    },
    {
        "title": "2. Phishing Scams",
        "content": """
            Phishing is a common cyberattack where attackers trick you into providing sensitive information.
            Be wary of suspicious emails, texts, or phone calls requesting personal information.
            Always verify the sender's identity and avoid clicking on unknown links.
        """
    },
    {
        "title": "3. Secure Wi-Fi Practices",
        "content": """
            Using secure Wi-Fi is essential to protect your data. Avoid public Wi-Fi for sensitive activities.
            Consider using a VPN when connecting to unsecured networks. Always secure your home network with a strong password.
        """
    },
    {
        "title": "4. Software Updates",
        "content": """
            Keeping your software up to date helps protect you from vulnerabilities.
            Regular updates often include security patches that help prevent exploitation by cybercriminals.
            Enable automatic updates wherever possible.
        """
    }
]

# Quiz questions
quiz_questions = [
    {
        "question": "What is a strong password practice?",
        "options": [
            "Use the same password for all accounts.",
            "Use unique and complex passwords for each account.",
            "Use a simple password for easier memory.",
            "Include only lowercase letters in the password."
        ],
        "answer": "Use unique and complex passwords for each account."
    },
    {
        "question": "What should you be cautious of in phishing scams?",
        "options": [
            "Emails from known sources.",
            "Unfamiliar emails asking for personal information.",
            "Text messages from friends.",
            "Social media notifications."
        ],
        "answer": "Unfamiliar emails asking for personal information."
    },
    {
        "question": "What should you avoid when using Wi-Fi for sensitive activities?",
        "options": [
            "Using your home Wi-Fi network.",
            "Using public Wi-Fi without a VPN.",
            "Securing your Wi-Fi with a password.",
            "Using a strong password."
        ],
        "answer": "Using public Wi-Fi without a VPN."
    },
    {
        "question": "Why are software updates important?",
        "options": [
            "They improve the appearance of the software.",
            "They provide security patches and prevent exploitation.",
            "They allow access to new apps.",
            "They are optional and unimportant."
        ],
        "answer": "They provide security patches and prevent exploitation."
    }
]

# Intro Screen
def intro_screen():
    st.markdown("<div class='header-font'>Welcome to the CyberSecurity Awareness Course</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='big-font'>In this course, you'll go through a training section to learn about cybersecurity "
        "essentials. Afterward, you'll be given a quiz to assess your understanding of these concepts.</div>",
        unsafe_allow_html=True
    )
    st.markdown("<div class='big-font'>If you're ready to begin, click the 'Proceed' button below.</div>", unsafe_allow_html=True)
    
    if st.button("Proceed", key="intro_proceed"):
        st.session_state.screen = "training1"

# Training Screen
def training_screen():
    # Find the current training screen index
    index = int(st.session_state.screen.replace("training", "")) - 1
    section = training_content[index]

    st.markdown(f"<div class='subheader-font'>{section['title']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='big-font'>{section['content']}</div>", unsafe_allow_html=True)

    # Navigation buttons with spacing
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("Previous", key=f"previous{index}"):
            st.session_state.screen = f"training{index}" if index > 0 else "intro"
    with col3:
        if st.button("Next", key=f"next{index}"):
            st.session_state.screen = f"training{index + 2}" if index < len(training_content) - 1 else "prepare_quiz"

# Preparation Screen
def prepare_quiz_screen():
    st.markdown("<div class='subheader-font'>Get Ready for the Quiz!</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='big-font'>You've completed the training. Now it's time to test your knowledge with a quick quiz. Good luck!</div>",
        unsafe_allow_html=True
    )
    if st.button("Start Quiz", key="start_quiz"):
        st.session_state.screen = "quiz1"

# Quiz Screen
def quiz_screen():
    # Get the current quiz question index
    index = int(st.session_state.screen.replace("quiz", "")) - 1
    question_data = quiz_questions[index]

    st.markdown(f"<div class='subheader-font'>Question {index + 1}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='big-font'>{question_data['question']}</div>", unsafe_allow_html=True)

    # Display options and collect answer with unique keys for each question
    answer = st.radio("Choose your answer:", question_data["options"], key=f"quiz{index + 1}")
    st.session_state.answers[f"quiz{index + 1}"] = answer

    # Navigation buttons with spacing
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("Previous", key=f"quiz_prev{index}"):
            st.session_state.screen = f"quiz{index}" if index > 0 else "prepare_quiz"
    with col3:
        if st.button("Next", key=f"quiz_next{index}"):
            st.session_state.screen = f"quiz{index + 2}" if index < len(quiz_questions) - 1 else "result"

# Result Screen
def result_screen():
    # Calculate score
    score = sum(
        1 for i, question_data in enumerate(quiz_questions, 1)
        if st.session_state.answers.get(f"quiz{i}") == question_data["answer"]
    )

    st.markdown("<div class='subheader-font'>Quiz Results</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='big-font'>You scored {score} out of {len(quiz_questions)}.</div>", unsafe_allow_html=True)

    # Feedback based on score
    if score == len(quiz_questions):
        st.markdown("<div class='big-font'>Excellent! You have strong cybersecurity awareness.</div>", unsafe_allow_html=True)
    elif score >= len(quiz_questions) / 2:
        st.markdown("<div class='big-font'>Good job! You have a solid understanding but could benefit from a little more practice.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='big-font'>Keep learning! Cybersecurity is a critical skill in today’s digital world.</div>", unsafe_allow_html=True)

    # Options to retake training or quiz with button adjustments
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Retake Training", key="retake_training"):
            st.session_state.screen = "training1"
            st.session_state.answers.clear()
    with col2:
        if st.button("Retake Quiz", key="retake_quiz"):
            st.session_state.screen = "quiz1"
            st.session_state.answers.clear()

# Screen router
if st.session_state.screen == "intro":
    intro_screen()
elif st.session_state.screen.startswith("training"):
    training_screen()
elif st.session_state.screen == "prepare_quiz":
    prepare_quiz_screen()
elif st.session_state.screen.startswith("quiz"):
    quiz_screen()
elif st.session_state.screen == "result":
    result_screen()
