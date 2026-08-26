import pprint
import sqlalchemy

from databasemrg import StorageManager
from database_maken import maak_database
from pathlib import Path

# TODO: Alle codes en statussen en enkel alle begrippenkaders
# TODO: Strip gebruiken voor spaties aan de zijkanten

pp = pprint.PrettyPrinter(indent=2, width=50, compact=True)

def dprint(w):
    print(" == \033[1mDEBUG\033[0m ==\n\033[35m"+str(w)+"\033[0m\n ====\n")


class TussenLaag:
    def __init__(self, database) -> None:
        self.stormrg = StorageManager(database)
        self.database_naam = database

    @staticmethod
    def fout_afhandeling(functie):
        def wrapper(self, *args, **kwargs):

            informatie_uit_functie = []

            try:
                informatie_uit_functie = functie(self, *args, **kwargs)

            except sqlalchemy.exc.OperationalError as e:
                print("\033[31m[!] Operatie fout --------\033[0m")
                print(e,"\n \033[31m-------- \033[0m")
                informatie_uit_functie = {"fout":str(e)}

            except sqlalchemy.exc.IntegrityError as f:
                print("\033[31m[!] Integriteits fout --------\033[0m")
                print(f, "\n \033[31m-------- \033[0m")
                informatie_uit_functie = {"fout":"Integriteits fout"}
            except Exception as e:
                print("\033[31m[!] Fout in functie --------\033[0m")
                print(e, "\n \033[31m-------- \033[0m")
                informatie_uit_functie = {"fout":str(e)}
            finally:


                if hasattr(informatie_uit_functie, "__len__") and len(informatie_uit_functie) == 0:
                        print("\033[31m[!] Geen resultaten gevonden --------\033[0m")
                        return {"fout":"Geen resultaten gevonden"}

                return informatie_uit_functie

        return wrapper


    def controleer_of_database_bestaat(self):
        db_path = Path(f"databases/{self.database_naam}.db")
        if db_path.exists():
            print("\033[32mDatabase: \'" + self.database_naam+"\' bestaat al\033[m")
        else:
            print("Database", self.database_naam, "bestaat niet")
            print("Database", self.database_naam, "aanmaken")
            maak_database(self.database_naam)
            print("Database", self.database_naam, "aangemaakt")

    @fout_afhandeling
    def aanmaken_begrippenkader(self, informatie:dict):
        self.stormrg.maakBegrippenkader(informatie)
        print("\033[34m[+] Begrippenkader --\033[0m")
        pp.pprint(informatie)

    @fout_afhandeling
    def aanmaken_begrip(self, informatie:dict):
        self.stormrg.maakBegrip(informatie)
        print("\033[34m[+] Begrip --\033[0m")
        pp.pprint(informatie)

    @fout_afhandeling
    def aanmaken_alternatieve_term(self, informatie:dict):
        print("\033[34m[+] Alternatieve term --\033[0m")
        print("\033[34m[+] Alternatieve term lijst --------\033[0m")

        for term in informatie["alternatieve_termen"]:
            #zorgt ervoordat de termen van een alternatie term lijst naar de alternatieve waarde gaan:
            """
            {
                "invoer": {
                    "gehele_naam": "Gebruiker1"
                },
                "alternatieve_termen": [ ->> "Wagen" <<-, "Voertuig", "Personenauto"],
                "voorkeursterm": "Auto",
                "naam_begrippenkader": "Verkeer",
                "status": "Actief",
                "vervalt_op": "",
                "gewijzigd_op": "2026-08-13"
            }
            Wordt
            {
                "invoer": {
                    "gehele_naam": "Gebruiker1"
                },
                "alternatieve_termen": [ ->> "Wagen" <<-, "Voertuig", "Personenauto"],
          --->> "alternatieve_term": "Wagen", <<----
                "voorkeursterm": "Auto",
                "naam_begrippenkader": "Verkeer",
                "status": "Actief",
                "vervalt_op": "",
                "gewijzigd_op": "2026-08-13"
            }
            """



            informatie["alternatieve_term"] = term
            bestaat = self.stormrg.controleer_of_alternatieve_term_bestaat(informatie)
            if not bestaat:
                self.stormrg.maakAlternatieve_term(informatie)
                print("\033[34m    [+] Alternative term --\033[0m")
                pp.pprint(informatie)
            else:
                print("\033[37m    [X] Alternative term: \'" + term + "\' bestaat al--\033[0m")

        print("\033[34m --------\033[0m")

    @fout_afhandeling
    def aanmaken_alternatieve_term_eenkeer(self, informatie: dict):
        print("\033[34m[+] Alternatieve term --------\033[0m")



        self.stormrg.maakAlternatieve_term(informatie)
        pp.pprint(informatie)

        print("\033[34m --------\033[0m")

    @fout_afhandeling
    def zoek_begrip_algemeen(self, informatie:dict):
       begrippen = self.stormrg.zoekBegrippen_algemeen(informatie)
       print("\033[34m[i] Zoeken op begrip algemeen met: \'" +informatie["zoek_opdracht"]+ "\' --------\033[0m")
       if len(begrippen) != 0:
           for begrip in begrippen:
               alternative_termen = self.stormrg.ID_geefAlle_Alternatieve_termen_bijhorend_tot_begrip(
                   {"begrip_id": begrip["begrip_id"]}
               )
               begrip["alternatieve_termen"] = alternative_termen

       pp.pprint(begrippen)
       print("\033[34m --------\033[0m")
       return begrippen

    @fout_afhandeling
    def geef_alle_begrippenkaders(self):
        begrippenkaders = self.stormrg.geefAlle_Begrippenkaders()
        print("\033[34m[i] Alle begrippenkaders --------\033[0m")
        pp.pprint(begrippenkaders)
        print("\033[34m --------\033[0m")
        return begrippenkaders

    @fout_afhandeling
    def geef_alle_begrippen_tot_begrippenkader(self, informatie:dict):

        print("\033[34m[i] Alle begrippen van begrippenkader: \'"+ informatie["naam_begrippenkader"]+"\' --------\033[0m")
        begrippen = self.stormrg.geefBegrip_bijhorend_tot_begrippenkader(
            informatie
        )
        pp.pprint(begrippen)
        print("\033[34m --------\033[0m")
        return begrippen

    @fout_afhandeling
    def geef_alle_alternative_termen_tot_begrip(self, informatie:dict):
        alternative_termen = self.stormrg.geefAlle_Alternatieve_termen_bijhorend_tot_begrip(
            informatie
        )
        print("\033[34m[i] Alle alternative termen van begrip: \'" + informatie["voorkeursterm"] + "\' in begrippenkader: \'"+informatie["naam_begrippenkader"]+"\' --------\033[0m")
        pp.pprint(alternative_termen)
        print("\033[34m --------\033[0m")
        return alternative_termen

    @fout_afhandeling
    def zoek_begrip(self, informatie:dict):


        begrip = self.stormrg.zoekBegrip(informatie)
        print("\033[34m[i] Zoek op begrip: \'" + informatie["voorkeursterm"] + "\' in begrippenkader: \'"+informatie["naam_begrippenkader"]+"\' --\033[0m")
        pp.pprint(begrip)
        print(type(begrip))
        return begrip

    @fout_afhandeling
    def zoek_detail_begrip(self, informatie:dict):
        begrip = self.stormrg.zoekBegrip(informatie)
        print("\033[34m[i] Zoek op begrip in detail: \'" + informatie["voorkeursterm"] + "\' in begrippenkader: \'" +
              informatie[
                  "naam_begrippenkader"] + "\' --\033[0m")

        if len(begrip) != 0:

            alternative_termen = self.stormrg.geefAlle_Alternatieve_termen_bijhorend_tot_begrip(
                informatie
            )

            begrip[0]["alternatieve_termen"] = alternative_termen




        pp.pprint(begrip)
        print("\033[34m --------\033[0m")
        return begrip

    @fout_afhandeling
    def geef_alle_begrippen_met_begrippenkaders(self):
        begrippenkaders = self.stormrg.geefAlle_Begrippenkaders()

        print("\033[34m[i] Geef alle begrippenkaders met bijhorende begrippen: --------\033[0m")

        for kader in begrippenkaders:
            begrippen_tot_begrippenkader = self.stormrg.geefAlle_Begrippen_bijhorend_tot_begrippenkader(
                {"naam_begrippenkader": kader["naam_begrippenkader"]}
            )
            kader["begrippen_tot_begrippenkader"] = begrippen_tot_begrippenkader
            print("\033[34m    [i] Begrippenkader: \'" + kader["naam_begrippenkader"] + "\' met bijhorende begrippen --------\033[0m")
            pp.pprint(kader)

        print("\033[34m --------\033[0m")

        pp.pprint(begrippenkaders)

        return begrippenkaders


    @fout_afhandeling
    def geef_alle_begrip_codes(self):
        begrip_codes = self.stormrg.geefAlle_begripcodes()
        print("\033[34m[i] Alle beschrikbare begrip codes --------\033[0m")
        pp.pprint(begrip_codes)
        print("\033[34m --------\033[0m")
        return begrip_codes


    @fout_afhandeling
    def geef_alle_statussen(self):
        statussen = self.stormrg.geefAlle_statussen()
        print("\033[34m[i] Alle beschrikbare statussen --------\033[0m")
        pp.pprint(statussen)
        print("\033[34m --------\033[0m")
        return statussen

    @fout_afhandeling
    def geef_alle_functies(self):
        statussen = self.stormrg.geefAlle_functies()
        print("\033[34m[i] Alle beschrikbare Functies --------\033[0m")
        pp.pprint(statussen)
        print("\033[34m --------\033[0m")
        return statussen


    @fout_afhandeling

    @fout_afhandeling
    def ID_geef_alle_alternatieve_termen_tot_begrip (self, informatie:dict):
        alternative_termen = self.stormrg.ID_geefAlle_Alternatieve_termen_bijhorend_tot_begrip(
            informatie
        )
        print("\033[34m[i] Alle alternative termen van begrip met begrip_id: \'" + str(informatie["begrip_id"]) + "\' --------\033[0m")
        pp.pprint(alternative_termen)
        print("\033[34m --------\033[0m")
        return alternative_termen

    @fout_afhandeling
    def ID_zoek_begrip(self, informatie:dict):
        begrip = self.stormrg.ID_zoekBegrip(informatie)
        print("\033[34m[i] Zoek op begrip met begrip_id: \'" + str(informatie["begrip_id"]) + "\' --\033[0m")
        pp.pprint(begrip)
        return begrip

    @fout_afhandeling
    def ID_zoek_detail_begrip(self, informatie:dict):
        begrip = self.stormrg.ID_zoekBegrip(informatie)
        print("\033[34m[i] Zoek op begrip in detail op begrip_id: \'" + str(informatie["begrip_id"]) + "\' --\033[0m")

        if len(begrip) != 0:

            alternative_termen = self.stormrg.ID_geefAlle_Alternatieve_termen_bijhorend_tot_begrip(
                informatie
            )

            begrip[0]["alternatieve_termen"] = alternative_termen



        # else:
        #     print("\033[34m[i] Zoek op begrip in detail op begrip_id: \'" + informatie["begrip_id"] + "\' --\033[0m")
        #     print("[Geen resultaten gevonden]")

        pp.pprint(begrip)
        print("\033[34m --------\033[0m")
        return begrip

    @fout_afhandeling
    def ID_geef_alle_begrippen_tot_begrippenkader(self, informatie: dict):
        begrippen = self.stormrg.ID_geefAlle_Begrippen_bijhorend_tot_begrippenkader(
            informatie
        )
        print("\033[34m[i] Alle begrippen van begrippenkader met begrippenkader_id: \'" + str(informatie[
            "begrippenkader_id"]) + "\' --------\033[0m")

        pp.pprint(begrippen)
        print("\033[34m --------\033[0m")
        return begrippen

    @fout_afhandeling
    def ID_geef_begrippenkader_informatie(self, informatie:dict):
        begrippenkader = self.stormrg.ID_geef_Begrippenkader(
            informatie
        )

        print("\033[34m[i] Zoek op begrippenkader met begrippenkader_id: \'" + str(informatie["begrippenkader_id"]) + "\' --\033[0m")
        pp.pprint(begrippenkader)
        print("\033[34m --------\033[0m")



    @fout_afhandeling
    def geef_Begrippenkader_op_naam(self, informatie:dict):
        begrippenkader = self.stormrg.geef_Begrippenkader_op_naam(
            informatie
        )

        print("\033[34m[i] Zoek op begrippenkader met naam_begrippenkader: \'" +
            informatie["naam_begrippenkader"] + "\' --\033[0m")
        pp.pprint(begrippenkader)
        print("\033[34m --------\033[0m")



    @fout_afhandeling
    def geef_begrippenkader_detail(self, informatie:dict):
        begrippenkader = self.stormrg.geef_Begrippenkader_op_naam(
            informatie
        )
        print(
            "\033[34m[i] Zoek op begrippenkader in detail op naam_begripppenkader: \'" + str(
                informatie["naam_begrippenkader"]) + "\' --\033[0m")

        if len(begrippenkader) != 0:
            begrippen = self.stormrg.geefAlle_Begrippen_bijhorend_tot_begrippenkader(
                informatie
            )
            begrippenkader[0]["begrippen"] = begrippen




            # else:
            #     print("\033[34m[i] Zoek op begrip in detail op begrip_id: \'" + informatie["begrip_id"] + "\' --\033[0m")
            #     print("[Geen resultaten gevonden]")

        pp.pprint(begrippenkader)
        print("\033[34m --------\033[0m")
        return begrippenkader


    @fout_afhandeling
    def ID_geef_begrippenkader_detail(self, informatie: dict):
        begrippenkader = self.stormrg.ID_geef_Begrippenkader(
            informatie
        )
        print(
            "\033[34m[i] Zoek op begrippenkader in detail op begrippenkader_id: \'" + str(
                informatie["begrippenkader_id"]) + "\' --\033[0m")
        if len(begrippenkader) != 0:
            begrippen = self.stormrg.ID_geefAlle_Begrippen_bijhorend_tot_begrippenkader(
                informatie
            )
            begrippenkader[0]["begrippen"] = begrippen



            # else:
            #     print("\033[34m[i] Zoek op begrip in detail op begrip_id: \'" + informatie["begrip_id"] + "\' --\033[0m")
            #     print("[Geen resultaten gevonden]")
        pp.pprint(begrippenkader)
        print("\033[34m --------\033[0m")
        return begrippenkader

    @fout_afhandeling
    def geef_alle_begrippen(self):
        begrippen = self.stormrg.geefAlle_begrippen()
        print("\033[34m[i] Alle beschrikbare begrippen --------\033[0m")
        pp.pprint(begrippen)
        print("\033[34m --------\033[0m")
        return begrippen



    @fout_afhandeling
    def geef_invoerscherm_data(self):
        functies_l = []
        statussen_l = []
        begripcodes_l = []
        begrippenkaders_l = []

        functies = self.stormrg.geefAlle_functies()
        statussen = self.stormrg.geefAlle_statussen()
        begripcodes = self.stormrg.geefAlle_begripcodes()
        begrippenkaders = self.stormrg.geefAlle_Begrippenkaders()

        for functie in functies:
            functies_l.append(functie["functie_naam"])
        for status in statussen:
            statussen_l.append(status["status_naam"])
        for begripcode in begripcodes:
            begripcodes_l.append(begripcode["code_naam"])
        for begrippenkader in begrippenkaders:
            begrippenkaders_l.append(begrippenkader["naam_begrippenkader"])

        return {
            "functies": functies_l,
            "statussen": statussen_l,
            "begripcodes": begripcodes_l,
            "begrippenkaders": begrippenkaders_l,
        }

    @fout_afhandeling
    def controleer_of_voorkeurs_term_bestaat(self, informatie:dict):
        print("\033[34m[v] Controleren of voorkeursterm: \'" + str(
                informatie["voorkeursterm"]) + "\' in begrippenkader: \'"+str(informatie["naam_begrippenkader"])+"\' bestaat --\033[0m")
        bestaat = self.stormrg.controleer_of_begrip_al_bestaat(informatie)
        print("Term bestaat: ", bestaat)
        print("\033[34m --------\033[0m")

        return bestaat

    @fout_afhandeling
    def controleer_of_begrippenkader_bestaat(self, informatie:dict):
        print("\033[34m[v] Controleren of begrippenkader: \'"+str(informatie["naam_begrippenkader"])+"\' bestaat --\033[0m")
        bestaat = self.stormrg.controleer_of_begrippenkader_al_bestaat(informatie)
        print("Term bestaat: ", bestaat)
        print("\033[34m --------\033[0m")

        return bestaat




# t = TussenLaag("T03")
# t.controleer_of_database_bestaat()
# t.controleer_of_voorkeurs_term_bestaat(
#     {
#         "naam_begrippenkader": "Yoshi",
#         "voorkeursterm": "BowserisToad"
#     }
# )
# t.controleer_of_begrippenkader_bestaat(
#     {
#         "naam_begrippenkader": "Yoshi3"
#     }
# )
# cv = t.zoek_begrip_algemeen(
#     {
#         "zoek_opdracht": "ser"
#     }
# )
# dprint(cv)
#
# XX =t.geef_alle_begrippenkaders()
# dprint(XX)
#
# b = t.geef_alle_begrippen_tot_begrippenkader(
#     {
#         "naam_begrippenkader": "Yoshi"
#     }
# )
#
# dprint(b)
#
# t.geef_alle_alternative_termen_tot_begrip(
#     {
#                 "naam_begrippenkader": "Yoshi",
#                 "voorkeursterm": "BowserisToad"
#     }
# )
#
# v = t.zoek_begrip(
# {
#                 "naam_begrippenkader": "Yoshi",
#                 "voorkeursterm": "BowserisToad",
#             }
# )
#
# dprint(v)
#
#
# xx = t.zoek_detail_begrip(
# {
#                 "naam_begrippenkader":"Yoshi",
#                 "voorkeursterm": "BowserisToad",
#             }
# )
#
# t.geef_alle_begrip_codes()
# t.geef_alle_statussen()
# #
# k = t.aanmaken_begrip(
#     {
#         "invoer": {
#             "gehele_naam": "Toad Mans"
#         },
#         "status": "Geen Toadddd",
#         "naam_begrippenkader": "Yoshi",
#         "code": "Toad-001",
#         "voorkeursterm": "0359j463",
#         "definitie_begrip": "bowser",
#         "toelichting_begrip": "Bowser Bowser Bowser Bowser ",
#         "voorbeeld_begrip": "Buzzhe",
#         "aangemaakt_op": "datum 1",
#         "gewijzigd_op": "FGG",
#         "vervalt_op": "FG",
#         "bron": "https://toad.com"
#     }
# )
#
# print(k)
# v = t.zoek_detail_begrip(
#     {
#         "voorkeursterm": "acx",
#         "naam_begrippenkader": 4
#     }
# )
# #
# # dprint(v)
# # v = t.ID_geef_alle_begrippen_tot_begrippenkader(
# #     {
# #         "begrippenkader_id": 20000
# #     }
# # )
# # dprint(v)
# v = t.ID_geef_begrippenkader_informatie(
#  {
#      "begrippenkader_id": 2
#  }
# )
# print(v)
# #
# v1 = t.ID_zoek_begrip(
#      {
#          "begrip_id": 2
#      }
# )
# # v2 = t.geef_begrippenkader_detail(
# #     {
# #         "naam_begrippenkader": "Yoshi"
# #     }
# # )
# #
# # v3 = t.ID_geef_begrippenkader_detail(
# #     {
# #         "begrippenkader_id": 2
# #     }
# # )
# c = t.geef_alle_begrippen_met_begrippenkaders()
# dprint(c)
# # print("--- EINDE ---")
#
# v4 = t.geef_begrippenkader_detail(
#     {
#         "naam_begrippenkader": "Yoshi90"
#     }
# )
#
# print(v4)

# gv = t.geef_alle_functies(
# )
# print(gv)
#
# g = t.geef_invoerscherm_data()
# print(g)

