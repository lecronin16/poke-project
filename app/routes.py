from app import app
from flask import render_template, request, flash
from app.forms import PokemonSearchForm, CatchPokemon
import requests
import random
from app.models import Pokemon, pokeCollection
from app.models import db
from psycopg2 import IntegrityError


# from app.models import PokeCollection


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/pokedex')
#BRANDT IF YOURE READING THIS HOW DO I GET IT TO SHOW A RANGE OF POKEMON!!
def pokeDex():
    count = 0
    # randompoke = random.randint(1,151)
    # url = f'https://pokeapi.co/api/v2/pokemon/{randompoke}'
    my_dict ={}
    # res = requests.get(url)
    while count < 8:
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
        count +=1
        print(my_dict)
    return render_template('pokedex.html',pokemon = my_dict)


@app.route('/select', methods = ["GET","POST"])
def searchPokemon():
    form = PokemonSearchForm()
    my_dict = {}
    poke_name = form.name.data
    try:
        if request.method == "POST":
            poke_name = form.name.data
            if form.validate():
                url = f'https://pokeapi.co/api/v2/pokemon/{poke_name}'
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
                    pokemon = Pokemon(poke_name,my_dict['ability'],my_dict['img_url'],my_dict['hp'],my_dict['attack'],my_dict['defense'] )
                    

                    db.session.add(pokemon)
                    db.session.commit()
                    return render_template('select.html', form = form, pokemon = my_dict)

    except:
        IntegrityError
        db.session.rollback()
        return render_template('select.html', form = form, pokemon = my_dict)
    return render_template('select.html', form = form, pokemon = my_dict)


@app.route('/select/catch<id>', methods = ["GET","POST"])
def catchPokemon():
    form = CatchPokemon()
    if request.method == "POST":
        pokemon = id
        new_pokemon = pokeCollection(pokemon)

        db.session.add(new_pokemon)
        db.session.commit()

    return render_template('catch.html', form=form)

# @app.route('/pokemon')
# def pokemon():
#     users = User.query.all()
#     caught = []
#     caught_set = set()
#     if current_user.is_authenticated:
#         caught = current_user.caughtPoke.all()
#         caught_set = {c.id for c in caught}
#     for u in users:
#         if u.id in caught_set:
#             u.flag=True

    
    
#     return render_template('pokemon.html', names=users)

# @app.route('/select', methods = ["GET","POST"])
# def searchPokemon():
#     form = PokemonSearchForm()
#     my_dict = {}
#     poke_name = form.name.data

#     if request.method == "POST":
#         poke_name = form.name.data
#         if form.validate():
#             url = f'https://pokeapi.co/api/v2/pokemon/{poke_name}'
#             res = requests.get(url)
#             if res.ok:
#                 data = res.json()
#                 my_dict = {
#                     'name': data['name'],
#                     'ability': data['abilities'][0]['ability']['name'],
#                     'img_url': data['sprites']['front_shiny'],
#                     'hp': data['stats'][0]['base_stat'],
#                     'attack': data['stats'][1]['base_stat'],
#                     'defense': data['stats'][2]['base_stat'],
#                 }
#                 pokemon = Pokemon(poke_name,my_dict['ability'],my_dict['img_url'],my_dict['hp'],my_dict['attack'],my_dict['defense'] )
                

#                 db.session.add(pokemon)
#                 db.session.commit()
#                 return render_template('select.html', form = form, pokemon = my_dict)

#         else:
#             flash('Catch Pokemon or Search for Another')
#             url = f'https://pokeapi.co/api/v2/pokemon/{poke_name}'
#             res = requests.get(url)
#             if res.ok:
#                 data = res.json()
#                 my_dict = {
#                     'name': data['name'],
#                     'ability': data['abilities'][0]['ability']['name'],
#                     'img_url': data['sprites']['front_shiny'],
#                     'hp': data['stats'][0]['base_stat'],
#                     'attack': data['stats'][1]['base_stat'],
#                     'defense': data['stats'][2]['base_stat'],
#                 }
#             return render_template('select.html', form = form, pokemon = my_dict)

#     return render_template('select.html', form = form, pokemon = my_dict)




