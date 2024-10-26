import streamlit as st
from content_generator import get_course_content, get_quiz_generator

# Initialize session state variables
if "screen" not in st.session_state:
    st.session_state.screen = "welcome"
    st.session_state.score = 0
    st.session_state.answers = {}
    st.session_state.course_subject = None
    st.session_state.loading = False  # Loading state

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

# Welcome Screen - Get Subject
def welcome_screen():
    st.markdown("<div class='header-font'>Welcome to the [AI] Learning System</div>", unsafe_allow_html=True)
    st.markdown("<div class='big-font'>Enter the course subject you want to learn about:</div>", unsafe_allow_html=True)
    
    # Subject input field
    st.session_state.course_subject = st.text_input("Course Subject", placeholder="e.g., Cybersecurity measures in an organisation")
    
    # Proceed button
    proceed_button = st.button("Proceed", key="welcome_proceed", disabled=st.session_state.loading)

    if proceed_button and st.session_state.course_subject:
        # Set loading state and fetch content
        st.session_state.loading = True
        with st.spinner("Generating course content and quiz... Please wait."):
            st.session_state.training_content = get_course_content(st.session_state.course_subject)
            st.session_state.quiz_questions = get_quiz_generator(st.session_state.training_content)
            st.session_state.loading = False
            st.session_state.screen = "intro"  # Move to next screen automatically

# Intro Screen
def intro_screen():
    st.markdown("<div class='header-font'>Get Ready to Start Your Course!</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='big-font'>In this course, you'll go through a training section to learn about the selected "
        "topic. Afterward, you'll be given a quiz to assess your understanding of these concepts.</div>",
        unsafe_allow_html=True
    )
    st.markdown("<div class='big-font'>If you're ready to begin, click the 'Proceed' button below.</div>", unsafe_allow_html=True)
    
    if st.button("Proceed", key="intro_proceed"):
        st.session_state.screen = "training1"

# Training Screen
def training_screen():
    index = int(st.session_state.screen.replace("training", "")) - 1
    section = st.session_state.training_content[index]

    st.markdown(f"<div class='subheader-font'>{section['title']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='big-font'>{section['content']}</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("Previous", key=f"previous{index}"):
            st.session_state.screen = f"training{index}" if index > 0 else "intro"
    with col3:
        if st.button("Next", key=f"next{index}"):
            st.session_state.screen = f"training{index + 2}" if index < len(st.session_state.training_content) - 1 else "prepare_quiz"

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
    index = int(st.session_state.screen.replace("quiz", "")) - 1
    question_data = st.session_state.quiz_questions[index]

    st.markdown(f"<div class='subheader-font'>Question {index + 1}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='big-font'>{question_data['question']}</div>", unsafe_allow_html=True)

    answer = st.radio("Choose your answer:", question_data["options"], key=f"quiz{index + 1}")
    st.session_state.answers[f"quiz{index + 1}"] = answer

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("Previous", key=f"quiz_prev{index}"):
            st.session_state.screen = f"quiz{index}" if index > 0 else "prepare_quiz"
    with col3:
        if st.button("Next", key=f"quiz_next{index}"):
            st.session_state.screen = f"quiz{index + 2}" if index < len(st.session_state.quiz_questions) - 1 else "result"

# Result Screen
def result_screen():
    score = sum(
        1 for i, question_data in enumerate(st.session_state.quiz_questions, 1)
        if st.session_state.answers.get(f"quiz{i}") == question_data["answer"]
    )

    st.markdown("<div class='subheader-font'>Quiz Results</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='big-font'>You scored {score} out of {len(st.session_state.quiz_questions)}.</div>", unsafe_allow_html=True)

    if score == len(st.session_state.quiz_questions):
        st.markdown("<div class='big-font'>Excellent! You have strong cybersecurity awareness.</div>", unsafe_allow_html=True)
    elif score >= len(st.session_state.quiz_questions) / 2:
        st.markdown("<div class='big-font'>Good job! You have a solid understanding but could benefit from a little more practice.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='big-font'>Keep learning! Cybersecurity is a critical skill in today’s digital world.</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Retake Training", key="retake_training"):
            st.session_state.screen = "training1"
            st.session_state.answers.clear()
    with col2:
        if st.button("Retake Quiz", key="retake_quiz"):
            st.session_state.screen = "quiz1"
            st.session_state.answers.clear()

# Screen Router
if st.session_state.screen == "welcome":
    welcome_screen()
elif st.session_state.screen == "intro":
    intro_screen()
elif st.session_state.screen.startswith("training"):
    training_screen()
elif st.session_state.screen == "prepare_quiz":
    prepare_quiz_screen()
elif st.session_state.screen.startswith("quiz"):
    quiz_screen()
elif st.session_state.screen == "result":
    result_screen()
