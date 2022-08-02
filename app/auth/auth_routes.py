from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.auth.forms import UserCreationForm, UserLoginForm #EditUser
from app.models import User
from app.models import db
from werkzeug.security import check_password_hash


from flask_login import login_user, logout_user,login_required, current_user

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/login', methods = ["GET", "POST"])
def logIn():
    form = UserLoginForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username).first()

            if user:
                if check_password_hash(user.password, password):
                    login_user(user)
                    return render_template('home.html', form=form)
                else:
                    flash('Incorrect username/password combination.', 'danger')
                    return redirect(url_for ('auth.logIn'))
            else:
                flash('User with that username does not exist.', 'danger')
                return redirect(url_for ('auth.signUp'))

    return render_template('login.html', form=form)

@auth.route('/logout')
def logMeOut():
    flash("Successfully logged out.", 'success')
    logout_user()
    return redirect(url_for('auth.logIn'))

@auth.route('/signup', methods = ['GET',"POST"])
def signUp():
    form = UserCreationForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            user = User(username,email,password)

            db.session.add(user)
            db.session.commit()

            return redirect(url_for ('auth.logIn'))
        else:
            flash('Invalid form. Please fill it out correctly.', 'danger')
    return render_template('signup.html', form=form)


@auth.route('/editprofile/<int:id>', methods=["GET", "POST"])
@login_required
def editProfile(id):
    form = UserCreationForm()
    user = User.query.get_or_404(id)
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        #commit updates:
        user.updateUserInfo(username, email, password)
        user.saveUpdates()

        flash("User Updated", 'success')
        return redirect(url_for('index'))
    else:
        return render_template('editprofile.html', form=form, user=user)

@auth.route('/editprofile/delete/<int:id>',methods = ['GET',"POST"])
@login_required
def deleteUser(id):
    user = User.query.get_or_404(id)
    print(user)
    db.session.delete(user)
    db.session.commit()
    flash('Successfully deleted profile.', 'success')
    return redirect(url_for('index'))
    # else:
    #     return render_template('editprofile.html', user=user)
