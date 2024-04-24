from run_website import *

class Test:

    def __init__():

        # Inlezen data
        df_1_games = pd.read_csv("bgg_dataset_1/games.csv")
        df_1_themes = pd.read_csv("bgg_dataset_1/themes.csv")
        df_1_mechanics = pd.read_csv("bgg_dataset_1/mechanics.csv")

        # Mergen datasets en kolommen selecteren
        merged = pd.merge(df_1_games, df_1_themes)
        merged = pd.merge(merged, df_1_mechanics)
        selectie = merged[["BGGId", "Name", "AvgRating", "MinPlayers", "MaxPlayers", 'ImagePath', "MfgAgeRec", "MfgPlaytime", "GameWeight", "Science Fiction", "Adventure", "Fantasy", "Movies / TV / Radio theme", "Humor", "Animals", "Economic", "Medieval", "World War II", "Fighting", "Area Majority / Influence", "Dice Rolling", "Hand Management", "Hexagon Grid", "Set Collection", "Modular Board", "Negotiation", "Trading", "Variable Player Powers", "Grid Movement", "Simulation", "Cooperative Game", "Deduction", "Solo / Solitaire Game", "Drafting", "Physical"]]
        selectie['Score'] = 0 # Voegt de kolom 'score' toe met als waarde 0 voor elke rij





    # We weten dat er maar 1 spel is met een minimum tijd van over
    # 10000 minuten, dus als de queries op 1 spel uitkomen klopt het.
    def test_basic_questions():

        players = 1
        age = 20
        time_min = 10000
        time_max = 60000
        dif_min = 1
        dif_max = 5

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

        if (website.dataset_gefilterd.shape[0] == 1):
            return True

        return False





    # Volgens de tabel zijn er 7 spellen met 5 themas, dus als de bovenste 7 spellen 
    # een score van 250 hebben (5 * 50 = 250) klopt het filteren.  
    def test_themes():

        adventure = 50
        fantasy = 50
        sci_fi = 50
        movies = 50   
        humor = 50
        animals = 50
        economics = 50
        medieval = 50
        WW2 = 50
        fighting = 50
        themes_lijst = [adventure,fantasy,sci_fi,movies,humor,animals,economics,medieval,WW2,fighting]
        selectie['Score'] = selectie.apply (lambda row: themes_filter(row, themes_lijst), axis=1)
        website.dataset_gesorteerd = selectie.sort_values('Score', ascending=False) # Sorteert rijen op score van hoog naar laag 

        for i in range(7):
            if not website.dataset_gesorteerd.iloc[i]['Score'] == 250:
                return False

        return True





    # Als we niet kijken naar de mechanics die zijn samen gevoegd in de tabel, 
    # weten we dat er 1 spel is met 6 mechanics en dus een score van 300, als 
    # die bovenaan staat klopt het filteren.
    def test_mechanics():

        dice = 50
        drafting = 0
        set_col = 50
        modular = 0
        area = 50
        variable = 50
        physical = 50
        simulation = 50
        coop = 50
        deduction = 50 
        trading = 0

        mechanics_lijst = [dice,drafting,set_col,modular,area,variable,physical,simulation,coop,deduction,trading]
        selectie['Score'] = selectie.apply (lambda row: mechanics_filter(row, mechanics_lijst), axis=1)
        website.dataset_gesorteerd = selectie.sort_values('Score', ascending=False) # Sorteert rijen op score van hoog naar laag 

        if not website.dataset_gesorteerd.iloc[0]['Score'] == 300:
            return False

        return True





t = Test

basic = t.test_basic_questions()
themes = t.test_themes()
mechanics = t.test_mechanics()

print("\nResults test_basic_questions:", basic)
print("Results test_themes:", themes)
print("Results test_mechanics:", mechanics, "\n")