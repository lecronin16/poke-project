from flask import Blueprint, render_template

poketeam = Blueprint('poketeam', __name__, template_folder='poketemplates')

@poketeam.route('/viewteam')
def viewTeam():
    return render_template('poketeam.html')

