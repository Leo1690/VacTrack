"""
Runs a Flask webserver which allows you to view information about a Github
repository, which is obtained using the gitinfo.Repository class. Depends on
the flask package, and the gitinfo module. Will dynamically add new 
information based on the available functions of said class.
"""

from flask import Flask, render_template, request
import dropbox



APP = Flask(__name__)
ACCESS_TOKEN = "37-7Yx4I5TAAAAAAAAAA1k_GtxWt3E9qZH8rrmN3Q_DDUC9qNtdLmXmo959coMvz"
dbx = dropbox.Dropbox(ACCESS_TOKEN)
metadata, res = dbx.files_download(path="/data.txt")
print(res.content)
FILE_TO = '/data.txt'

signal = int()

@APP.route("/", methods = ['GET'])
def get_data():
    """
    Display information on the main page.
    """
    metadata, res = dbx.files_download(path="/data.txt")
    content = float(res.content)
    if (content < 0):
        data = f'Yikes! Error connecting - the vacuum was probably never here.'
    elif (content < 0.33):
        data = f'The vacuum is here!'
    else:
        data = f'The vacuum was here {content:.3} minutes ago.'

    return render_template("index.html", data = data)

@APP.route("/set-key")
def put_data():
    """
    Set availability of the data
    """
    signal = request.args["avail"]
    signal = (str)(signal)
    dbx.files_upload(bytes(signal, encoding="ascii"), FILE_TO, mode=dropbox.files.WriteMode.overwrite)
    return 'OK'

if __name__ == "__main__":
    APP.run(debug=True)
