from flask import Flask, render_template
import pandas as pd
from g3 import getTopGainersAndLosers, isMarketTime,getfnoData
from jinja2 import FileSystemLoader, Environment


app = Flask(__name__)

template_loader = FileSystemLoader(searchpath="./templates")
template_env = Environment(loader=template_loader)


@app.route('/')
# def index():
#     return render_template('index.html')
def index():
    # Call the function to get the data
    data = getTopGainersAndLosers()
    # Convert the data to a Pandas dataframe

    df = pd.DataFrame(data)
    
    # Render the dataframe as an HTML table using Flask's built-in Jinja template engine
    return render_template('index.html', data=df.to_dict('records'))

@app.route('/fno')
def fno():
    # Call the function to get the FNO data
    fno_data = getfnoData()  # Replace with your function to retrieve FNO data
    # Convert the data to a Pandas dataframe
    df1 = pd.DataFrame(fno_data)
    # Render the dataframe as an HTML table using Flask's built-in Jinja template engine
    return render_template('fno.html', data=df1.to_dict('records'))


if __name__ == '__main__':
    #app.run()
    app.run(debug=True, host='0.0.0.0')
