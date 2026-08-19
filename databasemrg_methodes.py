#%%
import pprint
from databasemrg import StorageManager

pp = pprint.PrettyPrinter(indent=4, width=50)
stormrg = StorageManager("T03")

#%%
stormrg.maakRol(
    {
        "rol_naam": ""
    }
)

#%%
stormrg.maakStatus(
    {
        "status": 1
    }
)

#%%
stormrg.maakBegrip_code(
    {
        "code": "Toad-0A1",
        "begrip_code_betekenis": "Er zijn veel toad die Toad zijn enzo"
    }
)

#%%
stormrg.maakFunctie(
    {
        "status": "Toad",
        "functie_naam": "functie_nieuw",
        "omschrijving_functie": "Is een mario"
    }
)

#%%
stormrg.maakGebruiker(
    {
        "rol_naam": "Toadette",
        "functie_naam": "functie_nieuw",
        "status": "Geen Toad",
        "voornaam": "Lief",
        "achternaam": "Toadje",
        "gehele_naam": "Gebruiker1",
        "email": "Toad.Man111s@hottoad.nl"
    }
)

#%%
stormrg.maakBegrippenkader(
    {
        "invoer": {
            "gehele_naam": "Toad Mans"
        },
        "functie_naam": "Toad",
        "status": "Geen Toad",
        "naam_begrippenkader": "<b>Toad</b>",
        "omschrijving": "SSFTR",
        "gewijzigd_op": "Datum2",
        "vervalt_op": "Datum3",
    }
)

#%%
stormrg.maakBegrip(
    {
        "invoer": {
            "gehele_naam": "Gebruiker1"
        },
        "status": "Geen Toad",
        "naam_begrippenkader": "Yoshi",
        "code": "Toad-001",
        "voorkeursterm": "Gemaakt_door_gebruiker_90",
        "definitie_begrip":"Nieuwe_definitie",
        "toelichting_begrip": "Bowser Bowser Bowser Bowser ",
        "voorbeeld_begrip": "Buzzhe",
        "gewijzigd_op": "datum 2",
        "vervalt_op": "datum 3",
        "bron": "https://toad.com"
    }
)

#%%
stormrg.maakAlternatieve_term(
    {
        "invoer": {
            "gehele_naam": "Gebruiker1"
        },
        "alternatieve_term": "5",
        "voorkeursterm": "1E voorkeursterm",
        "naam_begrippenkader": "Yoshi",
        "status": "Geen Toad",
        "vervalt_op": "CCE",
        "gewijzigd_op": "CFR"
    }
)

#%%
###
###
#%%
query_resultaat = stormrg.zoekGebruiker_algemeen(
    {
        "zoek_opdracht": ""
    }
)

pp.pprint(query_resultaat)

#%%
query_resultaat = stormrg.zoekGebruiker_op_status(
    {
        "status": "Toad"
    }
)

pp.pprint(query_resultaat)

#%%
query_resultaat = stormrg.zoekGebruiker_op_rol(
    {
        "rol_naam": "Toadette"
    }
)

pp.pprint(query_resultaat)

#%%
query_resultaat = stormrg.zoekGebruiker_op_functie(
    {
        "functie_naam": "mario is coolL"
    }
)

pp.pprint(query_resultaat)

#%%
query_resultaat = stormrg.zoekGebruiker_op_id(
    {
        "gebruiker_id": 5
    }
)

pp.pprint(query_resultaat)

#%%
query_resultaat = stormrg.geefAlle_gebruikers()

pp.pprint(query_resultaat)

#%%
query_resultaat = stormrg.zoekBegrippen_algemeen(
    {
        "zoek_opdracht": "BV99"
    }
)

pp.pprint(query_resultaat)

#%%
query_resultaat = stormrg.geefAlle_begrippen(
)

pp.pprint(query_resultaat)

#%%
query_resultaat = stormrg.geefAlle_Begrippenkaders(
)

pp.pprint(query_resultaat)

#%%
query_resultaat = stormrg.geefAlle_Begrippen_bijhorend_tot_begrippenkader(
    {
        "naam_begrippenkader":"Mario"
    }
)

pp.pprint(query_resultaat)

#%%
query_resultaat = stormrg.geefBegrip_bijhorend_tot_begrippenkader(
    {
        "naam_begrippenkader":"Yoshi",
        "voorkeursterm":"BowserisToad",
    }
)

pp.pprint(query_resultaat)

#%%
query_resultaat = stormrg.geefAlle_Alternatieve_termen_bijhorend_tot_begrip(
    {
        "naam_begrippenkader":"Yoshi",
        "voorkeursterm":"BowserisToad",
    }
)

pp.pprint(query_resultaat)

#%%
query_resultaat = stormrg.zoekBegrip(
    {
        "naam_begrippenkader":"Yoshi",
        "voorkeursterm":"BowserisToad",
    }
)

pp.pprint(query_resultaat)

#%%
query_resultaat = stormrg.geefAlle_statussen(
)

pp.pprint(query_resultaat)

#%%
query_resultaat = stormrg.geefAlle_begripcodes(
)

pp.pprint(query_resultaat)

#%%
query_resultaat = stormrg.geefAlle_functies(
)

pp.pprint(query_resultaat)

#%%
query_resultaat = stormrg.ID_geefAlle_Alternatieve_termen_bijhorend_tot_begrip(
    {
        "begrip_id": 4
    }
)

pp.pprint(query_resultaat)

#%%
query_resultaat = stormrg.ID_geefAlle_Begrippen_bijhorend_tot_begrippenkader(
    {
        "begrippenkader_id": 2
    }
)

pp.pprint(query_resultaat)

#%%
query_resultaat = stormrg.ID_zoekBegrip(
    {
        "begrip_id": 1
    }
)

pp.pprint(query_resultaat)

#%%
query_resultaat = stormrg.ID_geef_Begrippenkader(
    {
        "begrippenkader_id": 1
    }
)

pp.pprint(query_resultaat)

#%%
query_resultaat = stormrg.geef_Begrippenkader_op_naam(
    {
        "naam_begrippenkader": "Yoshi"
    }
)

pp.pprint(query_resultaat)

#%%
controle_resultaat = stormrg.controleer_of_begrip_al_bestaat(
    {
        "voorkeursterm": "1e voorkeursterm 2",
        "naam_begrippenkader": "Yoshi"
    }
)
pprint.pprint(controle_resultaat)

#%%
controle_resultaat = stormrg.controleer_of_begrippenkader_al_bestaat(
    {
        "naam_begrippenkader": "Yoshop"
    }
)
pprint.pprint(controle_resultaat)

#%%
controle_resultaat = stormrg.controleer_of_alternatieve_term_bestaat(
    {
        "naam_begrippenkader": "Yoshi",
        "voorkeursterm": "1e voorkeursterm",
        "alternatieve_term": "5"
    }
)
pprint.pprint(controle_resultaat)

#%%
# print(dir(bool))
# print(dir(list))
print(str(  hasattr([0,0,0], "__invert__")  ) + " lijst")
print(str(  hasattr(True, "__invert__")     ) + " bool")