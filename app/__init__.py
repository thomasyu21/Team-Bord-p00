#Team Bord: Austin Ngan (Gerald), Thomas Yu (Perry), Mark Zhu (Bob the Third Jr), Roshani Shrestha (Pete)
#SoftDev
#P00

#from flask import Flask             #facilitate flask webserving
#from flask import render_template   #facilitate jinja templating
#from flask import request           #facilitate form submission
#from flask import session           #facilitate session

from flask import Flask, render_template, request, session
import userdb   #enable control of an sqlite database
import os

app = Flask(__name__)    # create Flask object
app.secret_key=os.urandom(32) # generates a secret key

# ================================================================ #

@app.route("/", methods=['GET', 'POST'])
def disp_loginpage():
    '''
    Displays the login page or the user's personal blog page if they are logged in.
    '''
    if "user" in session: # checks if the user is logged in
        return render_template('userblog.html', sessionU = True, username = session['user'], listBlog = userdb.findBlogs(session['user']))
    else:
        return render_template( 'login.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    '''
    Takes the user to the register page after pressing the button on the login page.
    '''
    return render_template('register.html')

@app.route("/register_auth", methods=['GET', 'POST'])
def register_auth():
    '''
    Checks if the new username and password provided by the user on the register page are valid.
    Uses the database users.db to check if the username exists already.
    Also checks if the user didn't input any username and/or password.
    '''
    if (request.method == 'POST'): # checks if the request method is POST
        tempUser = request.form['username']
        tempPass = request.form['password']
        if (userdb.checkUser(tempUser)): # checks if the username already exists
            error = "Error: Username already exists."
            return render_template('register.html', message = error)
        elif (tempUser == "" and tempPass == ""): # checks if the both the username and password are empty
            error = "Error: No username or password entered."
            return render_template('register.html', message = error)
        elif (tempUser == ""): # checks if only the username is empty
            error = "Error: No username entered."
            return render_template('register.html', message = error)
        elif (tempPass == ""): # checks if only the password is empty
            error = "Error: No password entered."
            return render_template('register.html', message = error)
        else: # last case is that both the username and password are good
            userdb.addUser(tempUser,tempPass)
            return render_template('login.html', message = "You have successfully registered an account.")

@app.route("/auth", methods=['GET', 'POST'])
def authenticate():
    '''
    Checks if the username and password provided by the user in the login page are correct.
    Uses the database users.db.
    '''
    error = ""
    if (request.method == 'POST'): # checks if the request method is POST
        tempUser = request.form['username']
        tempPass = request.form['password']
        if (userdb.checkUserPass(tempUser, tempPass)): # checks if the username and password are both correct
            session['user'] = tempUser # adds session data
            return render_template('userblog.html', sessionU = True, username = session['user'], listBlog = userdb.findBlogs(request.form['username']))
        else:
            if (not userdb.checkUser(tempUser)): # checks if the username is incorrect
                error = "Error: Username or Password is incorrect."
            else: # the last case is that only the password is incorrect
                error = "Error: Username or Password is incorrect."
    return render_template( 'login.html', message = error)

@app.route("/back_login", methods=['GET', 'POST'])
def backtologin():
    '''
    Takes the user back to the login page after they press the button on the register page.
    '''
    return render_template('login.html')

@app.route("/personal", methods=['GET', 'POST'])
def personal():
    '''
    Sends the user to the home page.
    Used in the navbar.
    '''
    UName=session['user']
    return render_template('userblog.html', sessionU = True, username = UName, listBlog = userdb.findBlogs(UName))

@app.route("/logout", methods=['GET', 'POST'])
def logOut():
    '''
    Logs the user out of the session.
    '''
    session.pop('user', None) # removes the session
    return render_template('login.html', message = 'You have successfully logged out.') # takes the user back to the login page

@app.route("/blogpage", methods=['GET', 'POST'])
def blogPage():
    '''
    Displays the user's blogs.
    '''
    user = request.form['username']
    blogs = userdb.findBlogs(user)
    title = request.form['blogsub']
    entries = userdb.findEntries(user, title)
    if (user == session['user']):
        return render_template('indivBlog.html', blogTitle = title, sessionU = True, username = user, blogDescription = blogs[title], entriesList = entries)
    else:
        return render_template('indivBlog.html', blogTitle = title, sessionU = False, username = user, blogDescription = blogs[title], entriesList = entries)

@app.route("/createBlog", methods=['GET', 'POST'])
def createPost():
    '''For when the user wants to make a new post'''
    return render_template('createBlog.html', username = session['user'])

@app.route("/finishBlog", methods=['GET', 'POST'])
def finishPost():
    '''
    For when the user wants to finish their post
    '''
    blogs = userdb.findBlogs(session['user'])
    title = request.form['title']
    text = request.form['paragraph_text']
    userU=session['user']
    if title in blogs:
        return render_template('createBlog.html', error = "Title Already Exists", blogTitle = title, blogDescription = text, username = session['user'])
    else:
        userdb.addBlog(userU, title, text)
        return render_template('userblog.html', sessionU = True, username = userU, listBlog = userdb.findBlogs(session['user']))

@app.route("/displayAll", methods=['GET', 'POST'])
def displayAll():
    '''
    Displays all the users.
    The user can click on the buttons to see their blogs.
    '''
    return render_template('allBlogs.html', users = userdb.findAllUsers())

@app.route("/userblogs", methods=['GET', 'POST'])
def otherUserPage():
    '''
    Displays a user's page from the list of all users.
    If it is the same user as the one logged in, then certain buttons will be displayed.
    If it is not the same user, then those buttons will not be displayed.
    '''
    user = request.form['usersub']
    blogs = userdb.findBlogs(user)
    if (user == session['user']):
        return render_template('userblog.html', sessionU = True, username = user, listBlog = blogs)
    else:
        return render_template('userblog.html', sessionU = False, username = user, listBlog = blogs)

@app.route("/editBlog", methods=['GET', 'POST'])
def editBlog():
    '''
    Takes the user to a page to edit their blog.
    '''
    blogTitle = request.form['blogTitle']
    blogs = userdb.findBlogs(session['user'])
    return render_template('editBlog.html', newBlogTitle = blogTitle, blogTitle = blogTitle, blogDescription = blogs[blogTitle], username = session['user'])

@app.route("/finishEditBlog", methods=['GET', 'POST'])
def finishEditBlog():
    '''
    For when the user wants to edit Blog Title/Description
    '''
    userU=session['user']
    title = request.form['title']
    oldTitle = request.form['blogTitle']
    text = request.form['paragraph_text']
    entries = userdb.findEntries(session['user'], oldTitle)
    blogs = userdb.findBlogs(session['user'])
    if title in blogs and title != oldTitle:
        return render_template('editBlog.html', error = "Title Already Exists", newBlogTitle = title, blogTitle = oldTitle, blogDescription = text, username = session['user'])
    else:
        userdb.editBlog(userU, oldTitle, title, text)
        return render_template('indivBlog.html', blogTitle = title, sessionU = True, username = session['user'], blogDescription = userdb.findBlogs(session['user'])[title], entriesList = entries)


@app.route("/editEntry", methods=['GET', 'POST'])
def editPost():
    '''
    Takes the user to a page to edit an entry.
    '''
    blogTitle = request.form['blogTitle']
    title = request.form['entrysub']
    entry = userdb.findEntries(session['user'], blogTitle)[title]
    return render_template('editEntry.html', newEntryTitle = title, entryTitle = title, entryText = entry, blogTitle = blogTitle, username = session['user'])

@app.route("/finishEditEntry", methods=['GET', 'POST'])
def finishEditEntry():
    '''
    For when the user wants to edit a previous Post
    '''
    userU=session['user']
    title = request.form['title']
    oldTitle = request.form['entryTitle']
    text = request.form['paragraph_text']
    blogTitle = request.form['blogTitle']
    blogs = userdb.findBlogs(userU)
    entries = userdb.findEntries(userU, blogTitle)
    if title in entries and title != oldTitle:
        return render_template('editEntry.html', error = "Title Already Exists", newEntryTitle = title, entryTitle = oldTitle, entryText = text, blogTitle = blogTitle, username = session['user'])
    else:
        userdb.editEntry(userU, blogTitle, oldTitle, title, text)
        entries = userdb.findEntries(userU, blogTitle)
        return render_template('indivBlog.html', blogTitle = blogTitle, sessionU = True, username = session['user'], blogDescription = blogs[blogTitle], entriesList = entries)

@app.route("/createEntry", methods=['GET', 'POST'])
def createEntry():
    '''
    Takes the user to a page to create an entry.
    '''
    title = request.form['blogTitle']
    return render_template('createEntry.html', username = session['user'], blogTitle = title)

@app.route("/finishEntry", methods=['GET', 'POST'])
def finishEntry():
    '''
    Takes the user to the page with their blogs once they are done making an entry.
    '''
    blogTitle = request.form['blogTitle']
    title = request.form['title']
    text = request.form['paragraph_text']
    userU=session['user']
    blogs = userdb.findBlogs(userU)
    entries = userdb.findEntries(userU, blogTitle)
    if title in entries:
        return render_template("createEntry.html", error = "Title Already Exists", entryTitle = title, entryText = text, blogTitle = blogTitle, username = session['user'])
    else:
        userdb.addEntry(userU, blogTitle, title, text)
        return render_template('indivBlog.html', blogTitle = blogTitle, sessionU = True, username = session['user'], blogDescription = blogs[blogTitle], entriesList = userdb.findEntries(userU, blogTitle))

@app.route("/deleteEntry", methods=['GET', 'POST'])
def deleteEntry():
    userU=session['user']
    blogTitle=request.form['ogBlogTitle']
    entryTitle=request.form['ogTitle']
    userdb.removeEntry(userU, blogTitle, entryTitle)
    blogs = userdb.findBlogs(userU)
    entries = userdb.findEntries(userU, blogTitle)
    return render_template('indivBlog.html', blogTitle = blogTitle, sessionU = True, username = session['user'], blogDescription = blogs[blogTitle], entriesList = entries)

@app.route("/deleteBlog", methods=['GET', 'POST'])
def deleteBlog():
    userU=session['user']
    blogTitle=request.form['ogBlogTitle']
    userdb.removeBlog(userU, blogTitle,)
    blogs = userdb.findBlogs(userU)
    entries = userdb.findEntries(userU, blogTitle)
    return render_template('userblog.html', sessionU = True, username = userU, listBlog = userdb.findBlogs(session['user']))

# ================================================================================ #

if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()
