# app.py
# rebuild trigger
import os
import pymssql
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    response = ""
    if request.method == 'POST':
        input_query = request.form['input']
        response = connect_to_mssql(input_query)
    return render_template('index.html', input=request.form.get('input', ''), response=response)

def connect_to_mssql(input_query):
    # Connect to the database
    conn = pymssql.connect(
        server=os.environ["DB_SERVER"],
        database=os.environ["DB_NAME"],
        user=os.environ["DB_READONLY_USER"],
        password=os.environ["DB_READONLY_PW"]
    )
    cursor = conn.cursor(as_dict=True)

    # Execute the query
    cursor.execute(input_query)
    output = cursor.fetchall()

    # Close the connection
    conn.close()
    
    return output

if __name__ == '__main__':
    app.run()