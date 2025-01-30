from flask import Flask, render_template, request, jsonify
import pandas as pd
from io import BytesIO
import gdown
import requests

app = Flask(__name__)


df = pd.read_excel('sampleData.xlsx')


# for displaying all records
@app.route('/api/data', methods=['GET'])
def get_data():
    result = df.to_dict(orient="records") 
    return jsonify(result)


# API to get specific data by Code
@app.route('/api/data/<string:Code>', methods=['GET'])
def get_data_by_id(Code):
    row = df[df['Code'] == Code]
    if not row.empty:
        result = row.to_dict(orient="records")[0]  
        return jsonify(result['Slab'])
    else:
        return jsonify({"error": "Data not found"}), 404


# displaying and submitting the form
@app.route('/', methods=['GET', 'POST'])
def form():
    results = None
    if request.method == 'POST':
        Code = request.form.get('Code')  

        if isinstance(Code, str):
            df['Code'] = df['Code'].fillna('')  
            results = df[df['Code'].str.contains(Code, case=False, na=False)] 

            if results.empty:
                results = "No matching records found."
            else:
                results = results.to_dict(orient='records')
        else:
            results = "Invalid"

    return render_template('form.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)



