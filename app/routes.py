from app import app
from flask import render_template, request
from app.forms import PokemonSearchForm
import requests
import random

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
    while count < 6:
        randompoke = random.randint(1,151)
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

    if request.method == "POST":
        poke_name = form.name.data

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
    return render_template('select.html', form = form, pokemon = my_dict)
