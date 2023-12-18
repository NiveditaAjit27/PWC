# import necessary libraries 
import openai
import streamlit as st
import random


# OpenAI API key
openai.api_key = "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"

# Function to generate a question and answer options using the OpenAI API
def generate_question_answer(prompt):
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

# Create Streamlit title and subtitle
st.title("MCQ Quiz Application")
st.subheader("Topic to quiz on!")

# Get user inputs
topic = st.text_input("Enter your preferred quiz topic")
num_qns = st.slider("Number of questions", 1, 10, 5)

# Initializing score
score = 0

with st.form("quiz_form"):
    # Generate questions and answers
    for i in range(num_qns):
        prompt_question = f"Generate a completely different multiple choice question on {topic}: {i+1}"
        question = generate_question_answer(prompt_question)
        prompt_answeropt = f"Which option letter is the correct answer for the question: {question}?"
        answeropt = generate_question_answer(prompt_answeropt).strip().upper()
        wrong_answer_1 = generate_question_answer(f"Generate an incorrect answer option for {question} as B, but it should not be {answeropt} and not be related to {topic}").strip().upper()
        wrong_answer_2 = generate_question_answer(f"Generate an incorrect answer option for {question} as C, but it should not be {answeropt} and not be related to {topic}").strip().upper()
        wrong_answer_3 = generate_question_answer(f"Generate an incorrect answer option for {question} as D, but it should not be {answeropt} and not be related to {topic}").strip().upper()
        total_answers = [answeropt, wrong_answer_1, wrong_answer_2, wrong_answer_3]
        random.shuffle(total_answers)

        # Display the question
        st.write(f"{i+1}. {question}")
        for i, answer in enumerate(total_answers):
            st.write(f"{chr(i+65)}. {answer}")


        # Get user's answer
        user_answer_key = f"user_answer_{i}"
        user_answer = st.text_input(f"Your Answer (Enter A, B, C, or D):", key=user_answer_key)

        # Display the correct answer
        st.write(f"Correct Answer: {answeropt}")

        # Check if the user's answer is correct
        if user_answer.upper() == answeropt:
            st.write("Correct Answer")
            score += 1
        elif user_answer:
            st.write("Incorrect Answer")

        # Question Seperator to diffrentiate between questions
        st.markdown("---")

# Adding a submit button 
form_submit_button = st.form_submit_button("Submit Quiz")

# Display final score 
if form_submit_button:
    st.write(f"Your final score: {score}/{num_qns}")
