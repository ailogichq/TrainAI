import json
import requests
import re
from config import settings


def course_content_prompt(subject):
    prompt = f"""
    You are an Training Course Content Creator. When given a subject/topic,
    generate user friendly and well - formatted, easy to understand course content in 
    at least 2 paragraphs with at least 10 sentences per content.
    Your response should be a list of dictionaries of different sections of the course
    content in a logical sequential order. The content should be just 5.
    Generate the content in JSON RESPONSE FORMAT

    SUBJECT TO GENERATE CONTENT ON: {subject}

    JSON RESPONSE FORMAT:
    [{{"title": "<title_of_content_1>", "content": "content_1"}},
    {{"title": "<title_of_content_2>", "content": "content_2"}},
    {{"title": "<title_of_content_3>", "content": "content_3"}},
    .
    .
    .
    {{"title": "<title_of_content_nth>", "content": "content_nth"}}
    ]

    """
    return prompt

def quiz_generator_prompt(subject):
    prompt = f"""
    You are a Quiz Creator. When given a course content,
    Generate Questions and mubased on the course content you are given.
    Your response should be a list of dictionaries of different questions with 4 multiple choice questions.
    Only Generate 10 Questions.

    Generate the content in JSON RESPONSE FORMAT

    SUBJECT TO GENERATE CONTENT ON: {subject}

    JSON RESPONSE FORMAT:
    [
    {{"question": "<question_1>", "options": [<option1>, <option2>, <option3>, <option4>], "answer": "<correct_option>"}},
    {{"question": "<question_2>", "options": [<option1>, <option2>, <option3>, <option4>], "answer": "<correct_option>"}},
    {{"question": "<question_3>", "options": [<option1>, <option2>, <option3>, <option4>], "answer": "<correct_option>"}},
    .
    .
    .
    {{"question": "<question_nth>", "options": [<option1>, <option2>, <option3>, <option4>], "answer": "<correct_option>"}}
    ]
    """
    return prompt


def extract_dictionary(text):
    pattern = r"[\{[^{}]*\}]"
    # pattern = r'\[\s*\{.*?\}\s*(?:,\s*\{.*?\}\s*)*\]'

    res = re.findall(pattern, text)
    print(res)
    try:
        res = res[-1]
    except Exception as e:
        res = {}
        print(e)

    return res

def openai_response(query):

    messages = [
        {
            "role": "system",
            "content": f"""
                  {query}
                """,
        }
    ]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.openai_sec_key}",
    }

    payload = {
        "model": "gpt-4o",
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 4000,
        # "response_format": {"type": "json_object"},
    }
    response = requests.post(settings.openai_url, headers=headers, data=json.dumps(payload))
    result = response.json()["choices"][0]["message"]["content"]
    return result

def get_course_content(subject):
    result = []
    # try:
    result = json.loads(openai_response(course_content_prompt(subject)).strip('`json\n'))
    print(result)
    # except Exception as e:
    #     result = []
    return result

def get_quiz_generator(subject):
    result = []
    # try:
    result = json.loads(openai_response(quiz_generator_prompt(subject)).strip('`json\n'))
    print(result)
    # except Exception as e:
    #     result = []
    return result

# get_course_content("Cybersecurity measures in an organisation")

# content = """
# [{'title': 'Introduction to Cybersecurity', 'content': "This section provides an overview of cybersecurity, explaining its importance in protecting an organization's digital assets. It covers the basic concepts, including threats, vulnerabilities, and the impact of cyber attacks on businesses."}, 
# {'title': 'Identifying Cyber Threats', 'content': 'In this section, learners will explore various types of cyber threats such as malware, phishing, ransomware, and insider threats. It includes real-world examples and case studies to illustrate how these threats can affect an organization.'}, 
# {'title': 'Implementing Security Measures', 'content': 'This section focuses on the practical steps organizations can take to protect themselves from cyber threats. Topics include network security, data encryption, access control, and the use of firewalls and antivirus software.'}, 
# {'title': 'Developing a Cybersecurity Policy', 'content': 'Learners will understand the importance of having a comprehensive cybersecurity policy in place. This section covers the key components of a cybersecurity policy, how to develop one, and the role of employee training and awareness in maintaining security.'},
# {'title': 'Responding to Cyber Incidents', 'content': 'This section outlines the steps an organization should take in the event of a cyber incident. It includes incident response planning, communication strategies, and recovery processes to minimize damage and restore operations quickly.'}]"""
# get_quiz_generator(content)




