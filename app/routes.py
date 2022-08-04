from flask_login import login_required, current_user
from app import app
from flask import render_template, request, redirect, url_for
from app.forms import PokemonSearchForm
import requests
import random
from app.models import Pokemon, User
from app.models import db
from psycopg2 import IntegrityError


@app.route('/')
def index():
    users = User.query.all()
    return render_template('home.html', users=users)

@app.route('/pokedex')
def pokeDex():
    count = 0
    my_dict ={}
    poke_list = []
    while count < 12:
        randompoke = random.randint(1,700)
        print(randompoke)
        url = f'https://pokeapi.co/api/v2/pokemon/{randompoke}'
        res = requests.get(url)
        if res.ok:
            data = res.json()
            my_dict = {
                'name': data['name'],
                'ability': data['abilities'][0]['ability']['name'],
                'img_url': data['sprites']['front_shiny'],
                'hp': data['stats'][0]['base_stat'],
                'attack': data['stats'][1]['base_stat'],
                'defense': data['stats'][2]['base_stat'],
            }
        poke_list.append(my_dict)
        count +=1
        print(my_dict)
    return render_template('pokedex.html',pokemon = poke_list)


@app.route('/select', methods = ["GET","POST"])
@login_required
def searchPokemon():
    form = PokemonSearchForm()
    my_dict = {}
    poke1 = set()
    poke1 = current_user.pokeCollection.all()

    try:
        if request.method == "POST":
            poke_name = form.name.data
            if form.validate():
                url = f'https://pokeapi.co/api/v2/pokemon/{poke_name}'
                res = requests.get(url)
                if res.ok:
                    data = res.json()
                    my_dict = {
                        'id':data['id'],
                        'name': data['name'],
                        'ability': data['abilities'][0]['ability']['name'],
                        'img_url': data['sprites']['front_shiny'],
                        'hp': data['stats'][0]['base_stat'],
                        'attack': data['stats'][1]['base_stat'],
                        'defense': data['stats'][2]['base_stat'],
                    }

                    pokemon = Pokemon(poke_name,my_dict['ability'],my_dict['img_url'],my_dict['hp'],my_dict['attack'],my_dict['defense'] )
                    db.session.add(pokemon)
                    db.session.commit()
                        
                poke1 = current_user.pokeCollection.all()
                owned_pokes = {p.pokemon for p in poke1}
                flag = False
                if my_dict['name'] in owned_pokes:
                    flag=True
                return render_template('select.html', form = form, pokemon = my_dict, flag=flag)

    except:
        IntegrityError
        db.session.rollback()
        return render_template('select.html', form = form, pokemon = my_dict)

    return render_template('select.html', form = form, pokemon = my_dict)

