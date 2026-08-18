#%%
import requests

#%%
url = "http://127.0.0.1:5000/aanmaken_begrip/"

data = {
    "informatie":{
        "invoer": {
            "gehele_naam": "Gebruiker1"
        },
        "status": "Geen Toad",
        "naam_begrippenkader": "Yoshi",
        "code": "Toad-001",
        "voorkeursterm": "TOAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD",
        "definitie_begrip":"Nieuwe_definitie",
        "toelichting_begrip": "Bowser Bowser Bowser Bowser ",
        "voorbeeld_begrip": "Buzzhe",
        "aangemaakt_op": "datum 1",
        "gewijzigd_op": "datum 2",
        "vervalt_op": "datum 3",
        "bron": "https://toad.com"
    }
}

response = requests.post(url, json=data)
print(response.text)

#%%
url = "http://127.0.0.1:5000/aanmaken_begrippenkader/"

data = {
    "informatie":
        {
            "invoer": {
                "gehele_naam": "Toad Mans"
            },
            "functie_naam": "Toad",
            "status": "Geen Toad",
            "naam_begrippenkader": "Aangemaakt vanuit request",
            "omschrijving": "SSFTR",
            "aangemaakt_op": "DATum1",
            "gewijzigd_op": "Datum2",
            "vervalt_op": "Datum3",
        }
}

response = requests.post(url, json=data)
print(response.text)
