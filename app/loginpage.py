#Team Bord: Austin Ngan (Gerald), Thomas Yu (Perry), Mark Zhu (Bob the Third Jr), Roshani Shrestha (Pete)
#SoftDev
#P00

#from flask import Flask             #facilitate flask webserving
#from flask import render_template   #facilitate jinja templating
#from flask import request           #facilitate form submission
#from flask import session           #facilitate session

from flask import Flask, render_template, request, session
import os

app = Flask(__name__)    #create Flask object
app.secret_key=os.urandom(32) #secret key for flask to work

teamBord = "Team Bord: Austin Ngan, Roshani Shrestha, Thomas Yu, Mark Zhu" #TNPG + roster for both landing and response pages
username = "Username" # will change later

password = "Password123" # will change later

@app.route("/", methods=['GET', 'POST'])
def disp_loginpage():
    '''The response page that will display a greeting, the username, and the request method used'''
    if "user" in session: # checks if the user is logged in
        #print("***DIAG: session['user'] ***")
        #print(session['user'])
        return render_template('userblog.html', heading = teamBord, username = session['user'])
    else:
        return render_template( 'login.html', message = request.args.get('message'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route("/register_auth", methods=['GET', 'POST'])
def register_auth():
    if (request.method == 'POST'): # checks if the request method is POST
        tempUser = request.form['username']
        tempPass = request.form['password']
        # print("***DIAG: request.form ***")
        # print(request.form)
        # print("***DIAG: tempUser ***")
        # print(tempUser)
        # print("***DIAG: tempPass ***")
        # print(tempPass)
        if (tempUser == username): # checks if the username already exists
            error = "Error: Username already exists."
            return render_template('register.html', message = error)
        else:
            return render_template('login.html', message = "You have successfully registered an account.")

@app.route("/auth", methods=['GET', 'POST'])
def authenticate():
    error = ""
    if (request.method == 'POST'): # checks if the request method is POST
        tempUser = request.form['username']
        tempPass = request.form['password']
        if (tempUser == username and tempPass == password): # checks if the username and password are both correct
            session['user'] = tempUser # adds session data
            return render_template('userblog.html', heading = teamBord, username = session['user'])
        else:  # the case that the username and password are not both correct
            # print("***DIAG: request.form ***")
            # print(request.form)
            # print("***DIAG: tempUser ***")
            # print(tempUser)
            # print("***DIAG: tempPass ***")
            # print(tempPass)
            if (tempUser != username and tempPass != password): # checks if both are incorrect
                error = "Error: Username and password are incorrect."
            elif (tempUser != username): # checks if only username is incorrect
                error = "Error: Username is incorrect."
            else: # the last case is that only the password is incorrect
                error = "Error: Password is incorrect."
    return render_template( 'login.html', message = error)

@app.route("/logout", methods=['GET', 'POST'])
def logOut():
    '''For when the user logs out of the session'''
    session.pop('user',None)
    return render_template('login.html', message = 'You have successfully logged out.')

# temporary
@app.route("/blog1", methods=['GET', 'POST'])
def blogPage():
    return render_template('indivBlog.html')

@app.route("/createPost", methods=['GET', 'POST'])
def createPost():
    '''For when the user wants to make a new post'''
    return render_template('editBlog.html')

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
