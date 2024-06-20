import openai
import pandas as pd
from flask import Flask, jsonify

app = Flask(__name__)
df = pd.read_excel('Sampleforapi.xlsx')

def process_data_with_openai(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text}
        ],
        max_tokens=50,
        n=1,    
        temperature=1.0
    )
    return response.choices[0].message['content'].strip()

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/process-data', methods=['GET'])
def process_data():
    results = []
    for index, row in df.iterrows():
        text = row['Rep']
        openai_response = process_data_with_openai(text)
        results.append({
            "input": text,
            "openai_response": openai_response
        })
    return jsonify(results)

openai.api_key = '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'

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
    
    
    