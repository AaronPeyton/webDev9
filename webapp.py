from flask import Flask, render_template, request, Markup, flash
import os, json

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.  Otherwise, it is the name of the file (ex. webapp)

@app.route("/")
def render_main():
    return render_template('data_information.html')

# @app.route("/p1")
# def render_page1():
#     return render_template('trig.html')
#
# @app.route("/p2")
# def render_page2():
#     return render_template('derivative.html')
#
# @app.route("/p3")
# def render_page3():
#     return render_template('integral.html')
#
# @app.route("/p4")
# def render_page4():
    return render_template('stats.html')


if __name__=="__main__":
    app.run(debug=False, port=54321)
