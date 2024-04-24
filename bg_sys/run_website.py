from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

class Website:
    def __init__(self, selectie):
        self.selectie = selectie
        self.dataset_gefilterd = pd.DataFrame()

# Read datasets
df_1_games = pd.read_csv("bgg_dataset_1/games.csv")
df_1_themes = pd.read_csv("bgg_dataset_1/themes.csv")
df_1_mechanics = pd.read_csv("bgg_dataset_1/mechanics.csv")

# Merge datasets and select columns
merged = pd.merge(df_1_games, df_1_themes)
merged = pd.merge(merged, df_1_mechanics)
selectie = merged[["BGGId", "Name", "AvgRating", "MinPlayers", "MaxPlayers", 'ImagePath', "MfgAgeRec", "MfgPlaytime", "GameWeight", "Science Fiction", "Adventure", "Fantasy", "Movies / TV / Radio theme", "Humor", "Animals", "Economic", "Medieval", "World War II", "Fighting", "Area Majority / Influence", "Dice Rolling", "Hand Management", "Hexagon Grid", "Set Collection", "Modular Board", "Negotiation", "Trading", "Variable Player Powers", "Grid Movement", "Simulation", "Cooperative Game", "Deduction", "Solo / Solitaire Game", "Drafting", "Physical"]]
# Creat score columns and assign value 0
selectie['Score'] = 0
selectie['Score_themes'] = 0
selectie['Score_mechanics'] = 0

# Make class object
website = Website(selectie)

# Function for applying themes scores
def themes_filter(row, themes_lijst):
    score = 0
    score += row["Adventure"] * int(themes_lijst[0])
    score += row["Fantasy"] * int(themes_lijst[1])
    score += row["Science Fiction"] * int(themes_lijst[2])
    score += row["Movies / TV / Radio theme"] * int(themes_lijst[3])
    score += row["Humor"] * int(themes_lijst[4])
    score += row["Animals"] * int(themes_lijst[5])
    score += row["Economic"] * int(themes_lijst[6])
    score += row["Medieval"] * int(themes_lijst[7])
    score += row["World War II"] * int(themes_lijst[8])
    score += row["Fighting"] * int(themes_lijst[9])
    return score

# Function for applying mechanics scores
def mechanics_filter(row, mechanics_list):
    score = 0
    score += row["Dice Rolling"] * int(mechanics_list[0])
    score += 1/2 * row["Hand Management"] * int(mechanics_list[1])
    score += 1/2 * row["Drafting"] * int(mechanics_list[1])
    score += row["Set Collection"] * int(mechanics_list[2])
    score += 1/3 * row["Modular Board"] * int(mechanics_list[3])
    score += 1/3 * row["Hexagon Grid"] * int(mechanics_list[3])
    score += 1/3 * row["Grid Movement"] * int(mechanics_list[3])
    score += row["Area Majority / Influence"] * int(mechanics_list[4])
    score += row["Variable Player Powers"] * int(mechanics_list[5])
    score += row["Physical"] * int(mechanics_list[6])
    score += row["Simulation"] * int(mechanics_list[7])
    score += row["Cooperative Game"] * int(mechanics_list[8])
    score += row["Deduction"] * int(mechanics_list[9])
    score += 1/2 * row["Trading"] * int(mechanics_list[10])
    score += 1/2 * row["Negotiation"] * int(mechanics_list[10])
    return score

# Loads first page
@app.route("/")
def start_site():
    return render_template("index.html") 

if __name__ == 'main':
    app.run(debug=True)
    # "python -m flask --app run_website run" to run in terminal
    # https://flask.palletsprojects.com/en/2.2.x/quickstart/ to properly install flask
    # https://python-adv-web-apps.readthedocs.io/en/latest/flask_forms.html


# Loads basic questions page
@app.route("/to_basic_questions.html")
def index_to_basic_question():
    return render_template("basic_questions.html")



@app.post("/to_themes.html")
def basic_to_themes():

    if request.method == 'POST':
        # Reset scores in case page is reloaded
        website.dataset_gefilterd['Score'] = 0
        website.dataset_gefilterd['Score_themes'] = 0
        website.dataset_gefilterd['Score_mechanics'] = 0

        # Get user input from HTML form
        players = request.form.get('Players')
        age = request.form.get('Age')
        time_min = request.form.get('Time_min')
        time_max = request.form.get('Time_max')
        dif_min = request.form.get('Dif_min')
        dif_max = request.form.get('Dif_max')

        # Make sure min is actually the minimal amount when reading in range sliders
        if float(time_min) > float(time_max): 
            time_min, time_max = time_max, time_min
        if float(dif_min) > float(dif_max):
            dif_min, dif_max = dif_max, dif_min

        # Execute query to match user requirements
        website.dataset_gefilterd = website.selectie.query(
            f'''
                MinPlayers <= {players} and \
                MaxPlayers >= {players} and \
                MfgAgeRec <= {age} and \
                MfgPlaytime <= {time_max} and \
                MfgPlaytime >= {time_min} and \
                GameWeight <= {dif_max} and \
                GameWeight >= {dif_min}
            '''
        )

        # If requirements are too strict and not enough games are left, then fill in questions again
        if (website.dataset_gefilterd.shape[0] < 50):
            return render_template("basic_questions_err.html")


    return render_template("themes.html")


@app.post("/to_mechanics.html")
def themes_to_mechanics():

    if request.method == 'POST':
        # Reset scores in case page is reloaded:
        website.dataset_gefilterd['Score'] = 0
        website.dataset_gefilterd['Score_themes'] = 0

        # Get user input from HTML form
        adventure = request.form.get('Adventure')
        fantasy = request.form.get('Fantasy')
        sci_fi = request.form.get('Sci-fi')
        movies = request.form.get('Movies')      
        humor = request.form.get('Humor')
        animals = request.form.get('Animals')
        economics = request.form.get('Economics')
        medieval = request.form.get('Medieval')
        WW2 = request.form.get('WW2')
        fighting = request.form.get('Fighting') 
        themes_lijst = [adventure,fantasy,sci_fi,movies,humor,animals,economics,medieval,WW2,fighting]

        # Apply themes score:
        website.dataset_gefilterd['Score_themes'] += website.dataset_gefilterd.apply (lambda row: themes_filter(row, themes_lijst), axis=1)     
    return render_template("mechanics.html")


@app.post("/to_priorities.html")
def mechanics_to_priorities():

    if request.method == 'POST':
        # Reset scores in case page is reloaded
        website.dataset_gefilterd['Score'] = 0
        website.dataset_gefilterd['Score_mechanics'] = 0

        # Get user input from HTML form
        dice = request.form.get('Dice')
        drafting = request.form.get('Drafting')
        set_col = request.form.get('Set')
        modular = request.form.get('Modular')      
        area = request.form.get('Area')
        variable = request.form.get('Variable')
        physical = request.form.get('Physical')
        simulation = request.form.get('Simulation')
        coop = request.form.get('Coop')
        deduction = request.form.get('Deduction') 
        trading = request.form.get('Trading')
        mechanics_lijst = [dice,drafting,set_col,modular,area,variable,physical,simulation,coop,deduction,trading]

        # Apply mechanics score:
        website.dataset_gefilterd['Score_mechanics'] += website.dataset_gefilterd.apply (lambda row: mechanics_filter(row, mechanics_lijst), axis=1)
    return render_template("priority.html")




@app.post("/to_results.html")
def priorities_to_results():
    if request.method == 'POST':
        # Reset scores in case page is reloaded
        website.dataset_gefilterd['Score'] = 0

        # Get user input from HTML form:
        radio = int(request.form.get('Radio'))

        # Apply scalar to themes/mechanics score according to priority:
        if radio == 0:
            website.dataset_gefilterd['Score'] = website.dataset_gefilterd.apply (lambda row: row['Score_themes'] + row['Score_mechanics'], axis=1)
        elif radio == 1:
            website.dataset_gefilterd['Score'] = website.dataset_gefilterd.apply (lambda row: 1.5 * row['Score_themes'] + row['Score_mechanics'], axis=1)
        elif radio == 2:
            website.dataset_gefilterd['Score'] = website.dataset_gefilterd.apply (lambda row: row['Score_themes'] + 1.5 * row['Score_mechanics'], axis=1)
        else:
            website.dataset_gefilterd['Score'] = website.dataset_gefilterd.apply (lambda row: row['Score_themes'] + row['Score_mechanics'], axis=1)

        # Take into acount rating:
        website.dataset_gefilterd['Score'] = website.dataset_gefilterd.apply (lambda row: row['Score'] * 1/2 * row['AvgRating'] if row['Score'] > 0 else row['Score'], axis=1)
        
        # Order games and select columns to display:
        website.dataset_gefilterd = website.dataset_gefilterd.sort_values('Score', ascending=False) 
        website.dataset_gefilterd = website.dataset_gefilterd.head(n=30)
        website.dataset_gefilterd = website.dataset_gefilterd[[ "ImagePath", "Name", "AvgRating", "BGGId"]]
        website.dataset_gefilterd["ImagePath"] = website.dataset_gefilterd["ImagePath"] + "," + website.dataset_gefilterd["BGGId"].astype(str) # BBGId is extracted in js to create link to game
        
        # Fix indexing/ranking:
        website.dataset_gefilterd = website.dataset_gefilterd.reset_index(drop = True)
        website.dataset_gefilterd.index += 1
        website.dataset_gefilterd = pd.DataFrame(website.dataset_gefilterd,index=website.dataset_gefilterd.index)
        website.dataset_gefilterd = website.dataset_gefilterd.rename_axis('Ranking').reset_index(level = 0)
        # Select and rename columns
        website.dataset_gefilterd.rename(columns={'ImagePath': 'Photo', 'AvgRating': 'Rating'}, inplace=True)
        website.dataset_gefilterd.drop('BGGId', axis=1, inplace=True)

    # Return to result page with table:
    return render_template('results.html', tables=[website.dataset_gefilterd.to_html(index = False, justify = 'center').replace('border="1"','border="0"'), 1])
