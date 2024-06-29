from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
from groq import Groq

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Set up your Groq API key
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

if not GROQ_API_KEY:
    raise ValueError("No GROQ_API_KEY found in environment variables")

client = Groq(api_key=GROQ_API_KEY)

def generate_answer(question):
    # Generate an answer using the Groq API
    messages = [
        {
            "role": "user",
            "content": "\"You are a study note generator, I will ask a question to you. Please provide detailed answers to all of the questions following these specific requirements:\n\n1. Each answer must be a minimum of 120 words and maximum of 250 words in length.\n\n2. The answers should be simplified and concise, using plain and straightforward language that avoids complex vocabulary or overly advanced terms.\n\n3. The answers should follow the order in which the questions appear in the image, with each answer beginning with a simple, easy-to-understand definition or explanation of the key concept or topic.\n\n4. After the initial definition, the answer should continue by providing key points, facts, or details related to the question, presented in a numbered or bulleted list format.\n\n5. The tone and language used in the answers should be accessible and understandable to a general audience without specialized knowledge of the topic.\n\n6. If any part of the requirements is unclear or if you need any clarification.\n\n7. Strictly Don't use this (*) sysmbol to represnt bullet points instead use Numbers or alphabet to represent the bullets points,please let me know before proceeding."
        },
        {
            "role": "assistant",
            "content": "I'm ready to help! I understand the requirements and will provide detailed answers to your questions. \n\nPlease go ahead and ask your question, and I'll provide a response that meets the requirements."
        },
        {
            "role": "user",
            "content": question
        }
    ]
    
    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="gemma-7b-it",
        )
        answer = chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"
    
    return format_response(answer)

def format_response(response):
    # Formatting response into bullet points
    points = response.split('. ')
    formatted = '\n'.join(f'- {point.strip()}' for point in points if point)
    return formatted

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_answer', methods=['POST'])
def get_answer():
    data = request.json
    question = data.get('question')
    if not question:
        return jsonify({'error': 'Question is required'}), 400
    answer = generate_answer(question)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
