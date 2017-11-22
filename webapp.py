from flask import Flask, render_template, request, Markup, flash
import os, json

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)
with open('static/graduates.json') as graduate_data:
    data = json.load(graduate_data)

@app.route("/")
def render_main():
    return render_template('data_information.html')

@app.route("/major")
def render_major():
    return render_template('majorInfo.html')

@app.route("/division")
def render_division():
    return render_template('divisionInfo.html')


# @app.route("/p2")
# def render_page2():
#     return render_template('derivative.html')

if __name__=="__main__":
    # set debug to false when publishing
    app.run(debug = True, port = 54321)
