from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from app.models import Pokemon
from app.poketeam.forms import BattleSearchForm
from app.models import User
from app.models import db

poketeam = Blueprint('poketeam', __name__, template_folder='poketemplates')

@poketeam.route('/viewteam')
def viewTeam():
    return render_template('poketeam.html')

@poketeam.route('/battle', methods=['GET','POST'])
@login_required
def battle():
    form = BattleSearchForm()
    if form.validate():
        enemy_team = User.query.all()
        return redirect(url_for('poketeam.battleUser', username=enemy_team))
    return render_template('battle.html', form=form)

@poketeam.route('/battleuser<username>')
def battleUser(username):
    user = User.query.filter_by(username=username).first()
    # enemy_poke = username.pokeCollection.all()
    return render_template('battleuser.html', user=user, username=username)


@poketeam.route('/select/<pokemon>')
@login_required
def catchPoke(pokemon):
    caught = Pokemon.query.filter_by(pokemon=pokemon).first()
    current_user.catchPokemon(caught)
    return redirect(url_for('poketeam.getPoke'))

@poketeam.route('/select/<pokemon>')
@login_required
def releasePokemon(pokemon):
    let_go = Pokemon.query.get(pokemon=pokemon).first()
    current_user.releasePokemon(let_go)
    return redirect(url_for('poketeam.getPoke'))


@poketeam.route('/poketeam')
@login_required
def getPoke():
    current_team = current_user.pokeCollection.all()
    return render_template('poketeam.html',current_team = current_team)


