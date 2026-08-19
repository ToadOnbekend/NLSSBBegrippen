from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

class StorageManager:
    def __init__(self, database:str) -> None:
        self.database = database
        self.database_naam = database
        self.engine = create_engine(f'sqlite:///databases/{database}.db')
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def geef_database_naam(self) -> str:
        return self.database_naam

    ###
    ## MAKEN
    #
    def maakRol(self, informatie:dict):

        self.session.execute(text("""
            INSERT INTO Rol (rol_naam)
            VALUES (:rol_naam);
        """),
                             {
            "rol_naam": informatie["rol_naam"]
        }
        )

        self.session.commit()


    def maakBegrip_code(self, informatie:dict):
        self.session.execute(text("""
            INSERT INTO Begrip_code (begrip_code_betekenis, code)
            VALUES (:begrip_code_betekenis, :code)
        """),
                             {
                                 "begrip_code_betekenis": informatie["begrip_code_betekenis"],
                                 "code": informatie["code"]
                             }
        )
        self.session.commit()


    def maakStatus(self, informatie:dict):
        self.session.execute(text("""
            INSERT INTO Status (status)
            VALUES (:status)
        """),
                             {
                                 "status": informatie["status"]
                             }
        )
        self.session.commit()


    def maakFunctie(self, informatie:dict):
        # resultaten_fetch_query = self.session.execute(text("""
        #     SELECT status_id FROM Status
        #     WHERE status = :status
        #     LIMIT 1;
        # """),
        #                      {
        #                          "status": informatie["status"]
        #                      }
        # ).fetchall()
        #
        # status = resultaten_fetch_query[0][0]
        # print(status)


        self.session.execute(text("""
            INSERT INTO Functie (FK_status_id, omschrijving_functie, functie_naam)
                VALUES (
                    (SELECT status_id 
                    FROM Status 
                    WHERE UPPER(status) = UPPER(:status) 
                    LIMIT 1),
                    :omschrijving_functie, :functie_naam)
            
        """),
                        {
                            "status": informatie["status"],
                            "omschrijving_functie": informatie["omschrijving_functie"],
                            "functie_naam": informatie["functie_naam"]
                             }
        )
        self.session.commit()


    def maakGebruiker(self, informatie:dict):
        self.session.execute(text("""
            INSERT INTO Gebruiker(FK_rol_id, FK_functie_id, FK_status_id, voornaam, achternaam, gehele_naam, e_mail)
            VALUES ((SELECT rol_id FROM Rol where UPPER(rol_naam) = UPPER(:rol_naam)),
                    (SELECT functie_id FROM Functie where UPPER(functie_naam) = UPPER(:functie_naam)),
                    (SELECT status_id FROM Status where UPPER(status) = UPPER(:status)),
                    :voornaam, :achternaam, :gehele_naam, :email)
        """),
                             {
                                 "rol_naam": informatie["rol_naam"],
                                 "functie_naam": informatie["functie_naam"],
                                 "status": informatie["status"],
                                 "voornaam": informatie["voornaam"],
                                 "achternaam": informatie["achternaam"],
                                 "gehele_naam": informatie["gehele_naam"],
                                 "email": informatie["email"]
                             }
        )
        self.session.commit()

# TODO: Geen limit 1, in fout afhandeling
    def maakBegrippenkader(self, informatie:dict):
        self.session.execute(text("""
            INSERT INTO Begrippenkader (FK_functie_id, FK_status_id, naam_begrippenkader, omschrijving, aangemaakt_op, 
                                        gewijzigd_op, vervalt_op)
            VALUES ((SELECT Functie.functie_id
                     FROM Functie
                     JOIN Gebruiker ON Gebruiker.FK_functie_id =  Functie.functie_id
                     WHERE UPPER(Gebruiker.gehele_naam) = UPPER(:gehele_naam)
                     LIMIT 1),
                    (SELECT status_id FROM Status where UPPER(status) = UPPER(:status)),
                    :naam_begrippenkader, :omschrijving, (SELECT strftime('%Y-%m-%dT%H:%M:%SZ', 'now')), :gewijzigd_op, :vervalt_op)
        """),
                             {
                                 "gehele_naam": informatie["invoer"]["gehele_naam"],
                                 "status": informatie["status"],
                                 "naam_begrippenkader": informatie["naam_begrippenkader"],
                                 "omschrijving": informatie["omschrijving"],
                                 "gewijzigd_op": informatie["gewijzigd_op"],
                                 "vervalt_op": informatie["vervalt_op"]
                             }
        )
        self.session.commit()


    def maakBegrip(self, informatie:dict):
        self.session.execute(text("""
            INSERT INTO Begrip (FK_functie_id, FK_status_id, FK_begrippenkader_id, FK_begrip_code_id, 
                                voorkeursterm, definitie_begrip, toelichting_begrip, voorbeeld_begrip, 
                                aangemaakt_op, gewijzigd_op, vervalt_op, bron) 
            VALUES ((SELECT Functie.functie_id
                     FROM Functie
                     JOIN Gebruiker ON Gebruiker.FK_functie_id =  Functie.functie_id
                     WHERE UPPER(Gebruiker.gehele_naam) = UPPER(:gehele_naam)
                     LIMIT 1),
                    (SELECT status_id FROM Status 
                     WHERE UPPER(status) = UPPER(:status)
                     LIMIT 1),
                    (SELECT begrippenkader_id FROM Begrippenkader
                     WHERE UPPER(naam_begrippenkader) = UPPER(:naam_begrippenkader)
                     LIMIT 1),
                    (SELECT begrip_code_id FROM Begrip_code
                     WHERE UPPER(code) = UPPER(:code)
                     LIMIT 1),
                     :voorkeursterm, :definitie_begrip, :toelichting_begrip, :voorbeeld_begrip, (SELECT strftime('%Y-%m-%dT%H:%M:%SZ', 'now')), 
                     :gewijzigd_op, :vervalt_op, :bron
                   ) 
        """),
                             {
                                 "gehele_naam": informatie["invoer"]["gehele_naam"],
                                 "status": informatie["status"],
                                 "naam_begrippenkader": informatie["naam_begrippenkader"],
                                 "code": informatie["code"],
                                 "voorkeursterm": informatie["voorkeursterm"],
                                 "definitie_begrip": informatie["definitie_begrip"],
                                 "toelichting_begrip": informatie["toelichting_begrip"],
                                 "voorbeeld_begrip": informatie["voorbeeld_begrip"],
                                 # "aangemaakt_op": informatie["aangemaakt_op"],
                                 "gewijzigd_op": informatie["gewijzigd_op"],
                                 "vervalt_op": informatie["vervalt_op"],
                                 "bron": informatie["bron"]
                             }
        )
        self.session.commit()


    def maakAlternatieve_term(self, informatie:dict):
        self.session.execute(text("""
            INSERT INTO Alternatieve_term (alternatieve_term, FK_begrip_id, FK_status_id, FK_functie_id, 
                                           FK_begrippenkader_id, aangemaakt_op, gewijzigd_op, vervalt_op)
            VALUES (:alternatieve_term,
                    (SELECT Begrip.begrip_id FROM Begrip
                     JOIN Begrippenkader ON Begrippenkader.begrippenkader_id = Begrip.FK_begrippenkader_id
                     WHERE UPPER(Begrippenkader.naam_begrippenkader) = UPPER(:naam_begrippenkader) AND UPPER(Begrip.voorkeursterm) = UPPER(:voorkeursterm)
                     LIMIT 1),
                    (SELECT status_id FROM Status 
                     WHERE UPPER(status) = UPPER(:status)
                     LIMIT 1),
                    (SELECT Functie.functie_id
                     FROM Functie
                     JOIN Gebruiker ON Gebruiker.FK_functie_id =  Functie.functie_id
                     WHERE UPPER(Gebruiker.gehele_naam) = UPPER(:gehele_naam)
                     LIMIT 1),
                    (SELECT begrippenkader_id FROM Begrippenkader 
                     WHERE UPPER(naam_begrippenkader) = UPPER(:naam_begrippenkader)
                     LIMIT 1),
                    (SELECT strftime('%Y-%m-%dT%H:%M:%SZ', 'now')), :gewijzigd_op, :vervalt_op
                   )
        """),
                             {
                                 "gehele_naam": informatie["invoer"]["gehele_naam"],
                                 "alternatieve_term": informatie["alternatieve_term"],
                                 "voorkeursterm": informatie["voorkeursterm"],
                                 "naam_begrippenkader": informatie["naam_begrippenkader"],
                                 "status": informatie["status"],
                                 "vervalt_op": informatie["vervalt_op"],
                                 "gewijzigd_op": informatie["gewijzigd_op"]
                             }
        )
        self.session.commit()


    ###
    ## ZOEKEN
    #
    def zoekGebruiker_algemeen(self, informatie:dict):


        resultaat_query = self.session.execute(text("""
            SELECT DISTINCT Gebruiker.gebruiker_id, Rol.rol_naam, Functie.functie_naam, Status.status, 
                   Gebruiker.voornaam, Gebruiker.achternaam, Gebruiker.gehele_naam, Gebruiker.e_mail 
            FROM Gebruiker
            FULL OUTER JOIN Rol ON Rol.rol_id = Gebruiker.FK_rol_id
            FULL OUTER JOIN Functie ON Functie.functie_id = Gebruiker.FK_functie_id
            FULL OUTER JOIN Status ON Status.status_id = Gebruiker.FK_status_id  
            WHERE UPPER(voornaam) LIKE UPPER(:zoek_opdracht) OR UPPER(achternaam) LIKE UPPER(:zoek_opdracht) 
               OR UPPER(gehele_naam) LIKE UPPER(:zoek_opdracht) 
               OR UPPER(e_mail) LIKE UPPER(:zoek_opdracht)
            ORDER BY gebruiker_id
        """),
                             {
                                 "zoek_opdracht": f"%{informatie["zoek_opdracht"]}%"
                             }
        )


        resulaat_verwerkt = []
        for resultaat_query_in in resultaat_query:
            resulaat_verwerkt.append({
                "gebruiker_id": resultaat_query_in[0],
                "rol_naam": resultaat_query_in[1],
                "functie_naam": resultaat_query_in[2],
                "status_naam": resultaat_query_in[3],
                "voornaam": resultaat_query_in[4],
                "achternaam": resultaat_query_in[5],
                "gehele_naam": resultaat_query_in[6],
                "e_mail": resultaat_query_in[7]
            })

        return resulaat_verwerkt

    def zoekGebruiker_op_status(self, informatie:dict):


        resultaat_query = self.session.execute(text("""
            SELECT Gebruiker.gebruiker_id, Rol.rol_naam, Functie.functie_naam, Status.status, 
                   Gebruiker.voornaam, Gebruiker.achternaam, Gebruiker.gehele_naam, Gebruiker.e_mail 
            FROM Gebruiker
            JOIN Rol ON Rol.rol_id = Gebruiker.FK_rol_id
            JOIN Functie ON Functie.functie_id = Gebruiker.FK_functie_id
            JOIN Status ON Status.status_id = Gebruiker.FK_status_id  
            WHERE UPPER(Status.status) = UPPER(:status)
            ORDER BY gebruiker_id
        """),
                             {
                                 "status": informatie["status"]
                             }
        )


        resulaat_verwerkt = []
        for resultaat_query_in in resultaat_query:
            resulaat_verwerkt.append({
                "gebruiker_id": resultaat_query_in[0],
                "rol_naam": resultaat_query_in[1],
                "functie_naam": resultaat_query_in[2],
                "status_naam": resultaat_query_in[3],
                "voornaam": resultaat_query_in[4],
                "achternaam": resultaat_query_in[5],
                "gehele_naam": resultaat_query_in[6],
                "e_mail": resultaat_query_in[7]
            })

        return resulaat_verwerkt

    def zoekGebruiker_op_rol(self, informatie:dict):


        resultaat_query = self.session.execute(text("""
            SELECT Gebruiker.gebruiker_id, Rol.rol_naam, Functie.functie_naam, Status.status, 
                   Gebruiker.voornaam, Gebruiker.achternaam, Gebruiker.gehele_naam, Gebruiker.e_mail 
            FROM Gebruiker
            JOIN Rol ON Rol.rol_id = Gebruiker.FK_rol_id
            JOIN Functie ON Functie.functie_id = Gebruiker.FK_functie_id
            JOIN Status ON Status.status_id = Gebruiker.FK_status_id  
            WHERE UPPER(Rol.rol_naam) = UPPER(:rol_naam)
            ORDER BY gebruiker_id
        """),
                             {
                                 "rol_naam": informatie["rol_naam"]
                             }
        )


        resulaat_verwerkt = []
        for resultaat_query_in in resultaat_query:
            resulaat_verwerkt.append({
                "gebruiker_id": resultaat_query_in[0],
                "rol_naam": resultaat_query_in[1],
                "functie_naam": resultaat_query_in[2],
                "status_naam": resultaat_query_in[3],
                "voornaam": resultaat_query_in[4],
                "achternaam": resultaat_query_in[5],
                "gehele_naam": resultaat_query_in[6],
                "e_mail": resultaat_query_in[7]
            })

        return resulaat_verwerkt


    def zoekGebruiker_op_functie(self, informatie:dict):


        resultaat_query = self.session.execute(text("""
            SELECT Gebruiker.gebruiker_id, Rol.rol_naam, Functie.functie_naam, Status.status, 
                   Gebruiker.voornaam, Gebruiker.achternaam, Gebruiker.gehele_naam, Gebruiker.e_mail 
            FROM Gebruiker
            JOIN Rol ON Rol.rol_id = Gebruiker.FK_rol_id
            JOIN Functie ON Functie.functie_id = Gebruiker.FK_functie_id
            JOIN Status ON Status.status_id = Gebruiker.FK_status_id  
            WHERE UPPER(Functie.functie_naam) = UPPER(:functie_naam)
            ORDER BY gebruiker_id
        """),
                             {
                                 "functie_naam": informatie["functie_naam"]
                             }
        )


        resulaat_verwerkt = []
        for resultaat_query_in in resultaat_query:
            resulaat_verwerkt.append({
                "gebruiker_id": resultaat_query_in[0],
                "rol_naam": resultaat_query_in[1],
                "functie_naam": resultaat_query_in[2],
                "status_naam": resultaat_query_in[3],
                "voornaam": resultaat_query_in[4],
                "achternaam": resultaat_query_in[5],
                "gehele_naam": resultaat_query_in[6],
                "e_mail": resultaat_query_in[7]
            })

        return resulaat_verwerkt

    def zoekGebruiker_op_id(self, informatie:dict):
        resultaat_query = self.session.execute(text("""
            SELECT Gebruiker.gebruiker_id, Rol.rol_naam, Functie.functie_naam, Status.status, 
                   Gebruiker.voornaam, Gebruiker.achternaam, Gebruiker.gehele_naam, Gebruiker.e_mail 
            FROM Gebruiker
            JOIN Rol ON Rol.rol_id = Gebruiker.FK_rol_id
            JOIN Functie ON Functie.functie_id = Gebruiker.FK_functie_id
            JOIN Status ON Status.status_id = Gebruiker.FK_status_id
            WHERE UPPER(Gebruiker.gebruiker_id) = UPPER(:gebruiker_id)
            ORDER BY gebruiker_id
            LIMIT 1
        """),
                             {
                                 "gebruiker_id": informatie["gebruiker_id"]
                             }
        )

        resulaat_verwerkt = []
        for resultaat_query_in in resultaat_query:
            resulaat_verwerkt.append({
                "gebruiker_id": resultaat_query_in[0],
                "rol_naam": resultaat_query_in[1],
                "functie_naam": resultaat_query_in[2],
                "status_naam": resultaat_query_in[3],
                "voornaam": resultaat_query_in[4],
                "achternaam": resultaat_query_in[5],
                "gehele_naam": resultaat_query_in[6],
                "e_mail": resultaat_query_in[7]
            })

        return resulaat_verwerkt


    def geefAlle_gebruikers(self):
        resultaat_query = self.session.execute(text("""
            SELECT Gebruiker.gebruiker_id, Rol.rol_naam, Functie.functie_naam, Status.status, 
                   Gebruiker.voornaam, Gebruiker.achternaam, Gebruiker.gehele_naam, Gebruiker.e_mail 
            FROM Gebruiker
            JOIN Rol ON Rol.rol_id = Gebruiker.FK_rol_id
            JOIN Functie ON Functie.functie_id = Gebruiker.FK_functie_id
            JOIN Status ON Status.status_id = Gebruiker.FK_status_id  
            ORDER BY gebruiker_id
        """),
                             {
                             }
        )


        resulaat_verwerkt = []
        for resultaat_query_in in resultaat_query:

            resulaat_verwerkt.append({
                "gebruiker_id": resultaat_query_in[0],
                "rol_naam": resultaat_query_in[1],
                "functie_naam": resultaat_query_in[2],
                "status_naam": resultaat_query_in[3],
                "voornaam": resultaat_query_in[4],
                "achternaam": resultaat_query_in[5],
                "gehele_naam": resultaat_query_in[6],
                "e_mail": resultaat_query_in[7]
            })

        return resulaat_verwerkt

    ##
    ##
    ##
    ##
    ## TODO: Kunnen zoeken op functie/status/code. Kan later
    ##
    def zoekBegrippen_algemeen(self, informatie:dict):
        resultaat_query = self.session.execute(text("""
            SELECT DISTINCT Functie.functie_naam, Status.status, Begrippenkader.naam_begrippenkader, Begrip_code.code,
                   Begrip.voorkeursterm, Begrip.definitie_begrip,  Begrip.toelichting_begrip,
                   Begrip.voorbeeld_begrip, Begrip.aangemaakt_op, Begrip.gewijzigd_op, Begrip.vervalt_op, Begrip.bron,
                   Begrip.begrip_id
            FROM Begrip
            FULL OUTER JOIN Functie ON Functie.functie_id = Begrip.FK_functie_id
            FULL OUTER JOIN Status ON Status.status_id = Begrip.FK_status_id
            FULL OUTER JOIN Begrippenkader ON Begrippenkader.begrippenkader_id = Begrip.FK_begrippenkader_id
            FULL OUTER JOIN Begrip_code ON Begrip_code.begrip_code_id = Begrip.FK_begrip_code_id
            FULL OUTER JOIN Alternatieve_term ON Begrip.begrip_id = Alternatieve_term.FK_begrip_id
            WHERE UPPER(Begrip.voorkeursterm ) LIKE UPPER(:zoek_opdracht)
                OR UPPER(Begrip.definitie_begrip) LIKE UPPER(:zoek_opdracht)
                OR UPPER(Begrippenkader.naam_begrippenkader) LIKE UPPER(:zoek_opdracht)
                OR UPPER(Alternatieve_term.alternatieve_term) LIKE UPPER(:zoek_opdracht)
            ORDER BY Begrip.begrip_id
        """),
                             {
                                 "zoek_opdracht": f"%{informatie["zoek_opdracht"]}%"
                             }
        )


        resulaat_verwerkt = []
        for resultaat_query_in in resultaat_query:
            resulaat_verwerkt.append({
                "begrip_id": resultaat_query_in[12],
                "functie_naam": resultaat_query_in[0],
                "status_naam": resultaat_query_in[1],
                "naam_begrippenkader": resultaat_query_in[2],
                "begrip_code": resultaat_query_in[3],
                "voorkeursterm": resultaat_query_in[4],
                "definitie_begrip": resultaat_query_in[5],
                "toelichting_begrip": resultaat_query_in[6],
                "voorbeeld_begrip":  resultaat_query_in[7],
                "aangemaakt_op": resultaat_query_in [8],
                "gewijzigd_op": resultaat_query_in[9],
                "vervalt_op": resultaat_query_in[10],
                "bron": resultaat_query_in[11]

            })

        return resulaat_verwerkt


    def geefAlle_Begrippenkaders(self):
        resultaat_query = self.session.execute(text("""
            SELECT Begrippenkader.begrippenkader_id, Functie.functie_naam, Status.status, 
                   Begrippenkader.naam_begrippenkader, Begrippenkader.omschrijving, Begrippenkader.aangemaakt_op,
                   Begrippenkader.gewijzigd_op, Begrippenkader.vervalt_op
            FROM Begrippenkader
            JOIN Functie ON Functie.functie_id = Begrippenkader.FK_functie_id
            JOIN Status ON Status.status_id = Begrippenkader.FK_status_id
           
            ORDER BY Begrippenkader.begrippenkader_id
        """),
                             {

                             }
        )

        resulaat_verwerkt = []
        for resultaat_query_in in resultaat_query:
            resulaat_verwerkt.append({
                "begrippenkader_id": resultaat_query_in[0],
                "functie_naam": resultaat_query_in[1],
                "status_naam": resultaat_query_in[2],
                "naam_begrippenkader": resultaat_query_in[3],
                "omshrijving": resultaat_query_in[4],
                "aangemaakt_op": resultaat_query_in [5],
                "gewijzigd_op": resultaat_query_in[6],
                "vervalt_op": resultaat_query_in[7]
            })

        return resulaat_verwerkt


    def geefAlle_Begrippen_bijhorend_tot_begrippenkader(self, informatie:dict):
        resultaat_query = self.session.execute(text("""
            SELECT Functie.functie_naam, Status.status, Begrippenkader.naam_begrippenkader, Begrip_code.code,
                   Begrip.voorkeursterm, Begrip.definitie_begrip,  Begrip.toelichting_begrip,
                   Begrip.voorbeeld_begrip, Begrip.aangemaakt_op, Begrip.gewijzigd_op, Begrip.vervalt_op, Begrip.bron,
                   Begrip.begrip_id
            FROM Begrip
            JOIN Functie ON Functie.functie_id = Begrip.FK_functie_id
            JOIN Status ON Status.status_id = Begrip.FK_status_id
            JOIN Begrippenkader ON Begrippenkader.begrippenkader_id = Begrip.FK_begrippenkader_id
            JOIN Begrip_code ON Begrip_code.begrip_code_id = Begrip.FK_begrip_code_id
            WHERE UPPER(Begrippenkader.naam_begrippenkader) = UPPER(:naam_begrippenkader)
            ORDER BY Begrip.begrip_id
        """),
                             {
                                 "naam_begrippenkader": informatie["naam_begrippenkader"]
                             }
        )


        resulaat_verwerkt = []
        for resultaat_query_in in resultaat_query:
            resulaat_verwerkt.append({
                "begrip_id": resultaat_query_in[12],
                "functie_naam": resultaat_query_in[0],
                "status_naam": resultaat_query_in[1],
                "naam_begrippenkader": resultaat_query_in[2],
                "begrip_code": resultaat_query_in[3],
                "voorkeursterm": resultaat_query_in[4],
                "definitie_begrip": resultaat_query_in[5],
                "toelichting_begrip": resultaat_query_in[6],
                "voorbeeld_begrip":  resultaat_query_in[7],
                "aangemaakt_op": resultaat_query_in [8],
                "gewijzigd_op": resultaat_query_in[9],
                "vervalt_op": resultaat_query_in[10],
                "bron": resultaat_query_in[11]

            })

        return resulaat_verwerkt


    def geefBegrip_bijhorend_tot_begrippenkader(self, informatie:dict):
        resultaat_query = self.session.execute(text("""
            SELECT Functie.functie_naam, Status.status, Begrippenkader.naam_begrippenkader, Begrip_code.code,
                   Begrip.voorkeursterm, Begrip.definitie_begrip,  Begrip.toelichting_begrip,
                   Begrip.voorbeeld_begrip, Begrip.aangemaakt_op, Begrip.gewijzigd_op, Begrip.vervalt_op, Begrip.bron,
                   Begrip.begrip_id
            FROM Begrip
            JOIN Functie ON Functie.functie_id = Begrip.FK_functie_id
            JOIN Status ON Status.status_id = Begrip.FK_status_id
            JOIN Begrippenkader ON Begrippenkader.begrippenkader_id = Begrip.FK_begrippenkader_id
            JOIN Begrip_code ON Begrip_code.begrip_code_id = Begrip.FK_begrip_code_id
            WHERE UPPER(Begrippenkader.naam_begrippenkader) = UPPER(:naam_begrippenkader) 
            ORDER BY Begrip.begrip_id
        """),
                             {
                                 "naam_begrippenkader": informatie["naam_begrippenkader"],
                             }
        )


        resulaat_verwerkt = []
        for resultaat_query_in in resultaat_query:
            resulaat_verwerkt.append({
                "begrip_id": resultaat_query_in[12],
                "functie_naam": resultaat_query_in[0],
                "status_naam": resultaat_query_in[1],
                "naam_begrippenkader": resultaat_query_in[2],
                "begrip_code": resultaat_query_in[3],
                "voorkeursterm": resultaat_query_in[4],
                "definitie_begrip": resultaat_query_in[5],
                "toelichting_begrip": resultaat_query_in[6],
                "voorbeeld_begrip":  resultaat_query_in[7],
                "aangemaakt_op": resultaat_query_in [8],
                "gewijzigd_op": resultaat_query_in[9],
                "vervalt_op": resultaat_query_in[10],
                "bron": resultaat_query_in[11]

            })

        return resulaat_verwerkt

    def ID_geefAlle_Begrippen_bijhorend_tot_begrippenkader(self, informatie:dict):
        resultaat_query = self.session.execute(text("""
            SELECT Functie.functie_naam, Status.status, Begrippenkader.naam_begrippenkader, Begrip_code.code,
                   Begrip.voorkeursterm, Begrip.definitie_begrip,  Begrip.toelichting_begrip,
                   Begrip.voorbeeld_begrip, Begrip.aangemaakt_op, Begrip.gewijzigd_op, Begrip.vervalt_op, Begrip.bron,
                   Begrip.begrip_id
            FROM Begrip
            JOIN Functie ON Functie.functie_id = Begrip.FK_functie_id
            JOIN Status ON Status.status_id = Begrip.FK_status_id
            JOIN Begrippenkader ON Begrippenkader.begrippenkader_id = Begrip.FK_begrippenkader_id
            JOIN Begrip_code ON Begrip_code.begrip_code_id = Begrip.FK_begrip_code_id
            WHERE Begrippenkader.begrippenkader_id = :begrippenkader_id
            ORDER BY Begrip.begrip_id
        """),
                             {
                                 "begrippenkader_id": informatie["begrippenkader_id"]
                             }
        )


        resulaat_verwerkt = []
        for resultaat_query_in in resultaat_query:
            resulaat_verwerkt.append({
                "begrip_id": resultaat_query_in[12],
                "functie_naam": resultaat_query_in[0],
                "status_naam": resultaat_query_in[1],
                "naam_begrippenkader": resultaat_query_in[2],
                "begrip_code": resultaat_query_in[3],
                "voorkeursterm": resultaat_query_in[4],
                "definitie_begrip": resultaat_query_in[5],
                "toelichting_begrip": resultaat_query_in[6],
                "voorbeeld_begrip":  resultaat_query_in[7],
                "aangemaakt_op": resultaat_query_in [8],
                "gewijzigd_op": resultaat_query_in[9],
                "vervalt_op": resultaat_query_in[10],
                "bron": resultaat_query_in[11]

            })

        return resulaat_verwerkt

    def geefAlle_Alternatieve_termen_bijhorend_tot_begrip(self, informatie:dict):
        resultaat_query = self.session.execute(text("""
            SELECT Alternatieve_term.alternatieve_term_id, Begrip.voorkeursterm, Status.status, Functie.functie_naam,
                   Begrippenkader.naam_begrippenkader, Alternatieve_term.alternatieve_term,Alternatieve_term.aangemaakt_op, Alternatieve_term.gewijzigd_op,
                   Alternatieve_term.vervalt_op
            FROM Alternatieve_term
            JOIN Begrip ON Begrip.begrip_id = Alternatieve_term.FK_begrip_id
            JOIN Status ON Status.status_id = Alternatieve_term.FK_status_id
            JOIN Functie ON Functie.functie_id = Alternatieve_term.FK_functie_id
            JOIN Begrippenkader ON Begrippenkader.begrippenkader_id = Alternatieve_term.FK_begrippenkader_id
            
            WHERE UPPER(Begrippenkader.naam_begrippenkader) = UPPER(:naam_begrippenkader) 
              AND UPPER(Begrip.voorkeursterm) = UPPER(:voorkeursterm)
            ORDER BY Alternatieve_term.alternatieve_term_id
        """),
                             {
                                 "naam_begrippenkader": informatie["naam_begrippenkader"],
                                 "voorkeursterm": informatie["voorkeursterm"]
                             }
        )


        resulaat_verwerkt = []
        for resultaat_query_in in resultaat_query:
            resulaat_verwerkt.append({
                "alternatieve_term_id": resultaat_query_in[0],
                "voorkeursterm": resultaat_query_in[1],
                "status_naam": resultaat_query_in[2],
                "functie_naam": resultaat_query_in[3],
                "naam_begrippenkader": resultaat_query_in[4],
                "alternatieve_term": resultaat_query_in[5],
                "aangemaakt_op": resultaat_query_in [6],
                "gewijzigd_op": resultaat_query_in[7],
                "vervalt_op": resultaat_query_in[8]

            })

        return resulaat_verwerkt

    def ID_geefAlle_Alternatieve_termen_bijhorend_tot_begrip(self, informatie:dict):
        resultaat_query = self.session.execute(text("""
            SELECT Alternatieve_term.alternatieve_term_id, Begrip.voorkeursterm, Status.status, Functie.functie_naam,
                   Begrippenkader.naam_begrippenkader, Alternatieve_term.alternatieve_term,Alternatieve_term.aangemaakt_op, Alternatieve_term.gewijzigd_op,
                   Alternatieve_term.vervalt_op
            FROM Alternatieve_term
            JOIN Begrip ON Begrip.begrip_id = Alternatieve_term.FK_begrip_id
            JOIN Status ON Status.status_id = Alternatieve_term.FK_status_id
            JOIN Functie ON Functie.functie_id = Alternatieve_term.FK_functie_id
            JOIN Begrippenkader ON Begrippenkader.begrippenkader_id = Alternatieve_term.FK_begrippenkader_id
            
            WHERE Begrip.begrip_id = :begrip_id
            ORDER BY Alternatieve_term.alternatieve_term_id
        """),
                             {
                                 "begrip_id": informatie["begrip_id"]
                             }
        )


        resulaat_verwerkt = []
        for resultaat_query_in in resultaat_query:
            resulaat_verwerkt.append({
                "alternatieve_term_id": resultaat_query_in[0],
                "voorkeursterm": resultaat_query_in[1],
                "status_naam": resultaat_query_in[2],
                "functie_naam": resultaat_query_in[3],
                "naam_begrippenkader": resultaat_query_in[4],
                "alternatieve_term": resultaat_query_in[5],
                "aangemaakt_op": resultaat_query_in [6],
                "gewijzigd_op": resultaat_query_in[7],
                "vervalt_op": resultaat_query_in[8]

            })

        return resulaat_verwerkt


    def zoekBegrip(self, informatie:dict):
        resultaat_query = self.session.execute(text("""
            SELECT DISTINCT Functie.functie_naam, Status.status, Begrippenkader.naam_begrippenkader, Begrip_code.code,
                   Begrip.voorkeursterm, Begrip.definitie_begrip,  Begrip.toelichting_begrip,
                   Begrip.voorbeeld_begrip, Begrip.aangemaakt_op, Begrip.gewijzigd_op, Begrip.vervalt_op, Begrip.bron,
                   Begrip.begrip_id
            FROM Begrip
            FULL OUTER JOIN Functie ON Functie.functie_id = Begrip.FK_functie_id
            FULL OUTER JOIN Status ON Status.status_id = Begrip.FK_status_id
            FULL OUTER JOIN Begrippenkader ON Begrippenkader.begrippenkader_id = Begrip.FK_begrippenkader_id
            FULL OUTER JOIN Begrip_code ON Begrip_code.begrip_code_id = Begrip.FK_begrip_code_id
            WHERE UPPER(Begrip.voorkeursterm ) = UPPER(:voorkeursterm)
                AND UPPER(Begrippenkader.naam_begrippenkader) = UPPER(:naam_begrippenkader)
            ORDER BY Begrip.begrip_id
            LIMIT 1
        """),
                             {
                                 "naam_begrippenkader": informatie["naam_begrippenkader"],
                                 "voorkeursterm": informatie["voorkeursterm"]
                             }
        )


        resulaat_verwerkt = []
        for resultaat_query_in in resultaat_query:
            resulaat_verwerkt.append({
                "begrip_id": resultaat_query_in[12],
                "functie_naam": resultaat_query_in[0],
                "status_naam": resultaat_query_in[1],
                "naam_begrippenkader": resultaat_query_in[2],
                "begrip_code": resultaat_query_in[3],
                "voorkeursterm": resultaat_query_in[4],
                "definitie_begrip": resultaat_query_in[5],
                "toelichting_begrip": resultaat_query_in[6],
                "voorbeeld_begrip":  resultaat_query_in[7],
                "aangemaakt_op": resultaat_query_in [8],
                "gewijzigd_op": resultaat_query_in[9],
                "vervalt_op": resultaat_query_in[10],
                "bron": resultaat_query_in[11]

            })

        return resulaat_verwerkt

    def ID_zoekBegrip(self, informatie:dict):
        resultaat_query = self.session.execute(text("""
            SELECT DISTINCT Functie.functie_naam, Status.status, Begrippenkader.naam_begrippenkader, Begrip_code.code,
                   Begrip.voorkeursterm, Begrip.definitie_begrip,  Begrip.toelichting_begrip,
                   Begrip.voorbeeld_begrip, Begrip.aangemaakt_op, Begrip.gewijzigd_op, Begrip.vervalt_op, Begrip.bron,
                   Begrip.begrip_id
            FROM Begrip
            FULL OUTER JOIN Functie ON Functie.functie_id = Begrip.FK_functie_id
            FULL OUTER JOIN Status ON Status.status_id = Begrip.FK_status_id
            FULL OUTER JOIN Begrippenkader ON Begrippenkader.begrippenkader_id = Begrip.FK_begrippenkader_id
            FULL OUTER JOIN Begrip_code ON Begrip_code.begrip_code_id = Begrip.FK_begrip_code_id
            WHERE Begrip.begrip_id = :begrip_id
            ORDER BY Begrip.begrip_id
            LIMIT 1
        """),
                             {
                                 "begrip_id": informatie["begrip_id"]
                             }
        )


        resulaat_verwerkt = []
        for resultaat_query_in in resultaat_query:
            resulaat_verwerkt.append({
                "begrip_id": resultaat_query_in[12],
                "functie_naam": resultaat_query_in[0],
                "status_naam": resultaat_query_in[1],
                "naam_begrippenkader": resultaat_query_in[2],
                "begrip_code": resultaat_query_in[3],
                "voorkeursterm": resultaat_query_in[4],
                "definitie_begrip": resultaat_query_in[5],
                "toelichting_begrip": resultaat_query_in[6],
                "voorbeeld_begrip":  resultaat_query_in[7],
                "aangemaakt_op": resultaat_query_in [8],
                "gewijzigd_op": resultaat_query_in[9],
                "vervalt_op": resultaat_query_in[10],
                "bron": resultaat_query_in[11]

            })

        return resulaat_verwerkt

    def geefAlle_statussen(self):
        resultaat_query = self.session.execute(text("""
            SELECT status_id, status
            FROM Status
            ORDER BY status_id    
        """),
                             {
                             }
        )

        resulaat_verwerkt = []
        for resultaat_query_in in resultaat_query:
            resulaat_verwerkt.append({
                "status_id": resultaat_query_in[0],
                "status_naam": resultaat_query_in[1]


            })

        return resulaat_verwerkt

    def geefAlle_functies(self):
        resultaat_query = self.session.execute(text("""
            SELECT Functie.functie_id, Functie.omschrijving_functie, Functie.functie_naam, Status.status
            FROM Functie
            JOIN Status ON Status.status_id = Functie.FK_status_id
            ORDER BY functie_id
        """),
                             {
                             }
        )

        resulaat_verwerkt = []
        for resultaat_query_in in resultaat_query:
            resulaat_verwerkt.append({
                "functie_id": resultaat_query_in[0],
                "functie_omschrijving": resultaat_query_in[1],
                "functie_naam": resultaat_query_in[2],
                "functie_status": resultaat_query_in[3],

            })

        return resulaat_verwerkt

    def geefAlle_begripcodes(self):
        resultaat_query = self.session.execute(text("""
            SELECT begrip_code_id, code, begrip_code_betekenis
            FROM Begrip_code
            ORDER BY begrip_code_id    
        """),
                             {
                             }
        )

        resulaat_verwerkt = []
        for resultaat_query_in in resultaat_query:
            resulaat_verwerkt.append({
                "begrip_code_id": resultaat_query_in[0],
                "code_naam": resultaat_query_in[1],
                "begrip_code_betekenis": resultaat_query_in[2]
            })

        return resulaat_verwerkt

    def ID_geef_Begrippenkader(self, informatie:dict):
        resultaat_query = self.session.execute(text("""
            SELECT Begrippenkader.begrippenkader_id, Functie.functie_naam, Status.status, 
                   Begrippenkader.naam_begrippenkader, Begrippenkader.omschrijving, Begrippenkader.aangemaakt_op,
                   Begrippenkader.gewijzigd_op, Begrippenkader.vervalt_op
            FROM Begrippenkader
            JOIN Functie ON Functie.functie_id = Begrippenkader.FK_functie_id
            JOIN Status ON Status.status_id = Begrippenkader.FK_status_id    
            WHERE Begrippenkader.begrippenkader_id = :begrippenkader_id
            ORDER BY begrippenkader_id    
            LIMIT 1
        """),
                             {
                                 "begrippenkader_id": informatie["begrippenkader_id"]
                             }
        )

        resulaat_verwerkt = []
        for resultaat_query_in in resultaat_query:
            resulaat_verwerkt.append({
                "begrippenkader_id": resultaat_query_in[0],
                "functie_naam": resultaat_query_in[1],
                "status_naam": resultaat_query_in[2],
                "naam_begrippenkader": resultaat_query_in[3],
                "omschrijving": resultaat_query_in[4],
                "aangemaakt_op": resultaat_query_in[5],
                "gewijzigd_op": resultaat_query_in[6],
                "vervalt_op": resultaat_query_in[7]

            })

        return resulaat_verwerkt

    def geef_Begrippenkader_op_naam(self, informatie:dict):
        resultaat_query = self.session.execute(text("""
            SELECT Begrippenkader.begrippenkader_id, Functie.functie_naam, Status.status, 
                   Begrippenkader.naam_begrippenkader, Begrippenkader.omschrijving, Begrippenkader.aangemaakt_op,
                   Begrippenkader.gewijzigd_op, Begrippenkader.vervalt_op
            FROM Begrippenkader
            JOIN Functie ON Functie.functie_id = Begrippenkader.FK_functie_id
            JOIN Status ON Status.status_id = Begrippenkader.FK_status_id    
            WHERE UPPER(Begrippenkader.naam_begrippenkader) = UPPER(:naam_begrippenkader)
            ORDER BY begrippenkader_id    
            LIMIT 1
        """),
                             {
                                 "naam_begrippenkader": informatie["naam_begrippenkader"]
                             }
        )

        resulaat_verwerkt = []
        for resultaat_query_in in resultaat_query:
            resulaat_verwerkt.append({
                "begrippenkader_id": resultaat_query_in[0],
                "functie_naam": resultaat_query_in[1],
                "status_naam": resultaat_query_in[2],
                "naam_begrippenkader": resultaat_query_in[3],
                "omschrijving": resultaat_query_in[4],
                "aangemaakt_op": resultaat_query_in[5],
                "gewijzigd_op": resultaat_query_in[6],
                "vervalt_op": resultaat_query_in[7]

            })

        return resulaat_verwerkt

    def geefAlle_begrippen(self):
        resultaat_query = self.session.execute(text("""
            SELECT DISTINCT Functie.functie_naam, Status.status, Begrippenkader.naam_begrippenkader, Begrip_code.code,
                   Begrip.voorkeursterm, Begrip.definitie_begrip,  Begrip.toelichting_begrip,
                   Begrip.voorbeeld_begrip, Begrip.aangemaakt_op, Begrip.gewijzigd_op, Begrip.vervalt_op, Begrip.bron,
                   Begrip.begrip_id
            FROM Begrip
            FULL OUTER JOIN Functie ON Functie.functie_id = Begrip.FK_functie_id
            FULL OUTER JOIN Status ON Status.status_id = Begrip.FK_status_id
            FULL OUTER JOIN Begrippenkader ON Begrippenkader.begrippenkader_id = Begrip.FK_begrippenkader_id
            FULL OUTER JOIN Begrip_code ON Begrip_code.begrip_code_id = Begrip.FK_begrip_code_id
            ORDER BY Begrip.begrip_id
        """),
                            {
                             }
        )


        resulaat_verwerkt = []
        for resultaat_query_in in resultaat_query:
            resulaat_verwerkt.append({
                "begrip_id": resultaat_query_in[12],
                "functie_naam": resultaat_query_in[0],
                "status_naam": resultaat_query_in[1],
                "naam_begrippenkader": resultaat_query_in[2],
                "begrip_code": resultaat_query_in[3],
                "voorkeursterm": resultaat_query_in[4],
                "definitie_begrip": resultaat_query_in[5],
                "toelichting_begrip": resultaat_query_in[6],
                "voorbeeld_begrip":  resultaat_query_in[7],
                "aangemaakt_op": resultaat_query_in [8],
                "gewijzigd_op": resultaat_query_in[9],
                "vervalt_op": resultaat_query_in[10],
                "bron": resultaat_query_in[11]

            })

        return resulaat_verwerkt

   # def geefInformatie_voor_detailpagina(self, informatie):
    #     resultaat_query = self.session.execute(text("""
    #         SELECT Begrip.begrip_id, Functie.functie_naam , Status.status, Begrip.voorkeursterm, Begrip.naam_begrippenkader, Begrip.voorkeursterm, Begrip.definitie_begrip, Begrip.toelichting_begrip, Begrip.voorbeeld_begrip, Begrip.aangemaakt_op, Begrip.gewijzigd_op, Begrip.vervalt_op
    #         FROM Alternatieve_term
    #         FULL OUTER JOIN Begrip ON Begrip.begrip_id = Alternatieve_term.FK_begrip_id
    #         ORDER BY begrip_id
    #     """),
    #                          {
    #                          }
    #     )

    #TODO: Maak controle functie of begrip al bestaat en ook een functie die controleert of begrippenkader al bestaat.

    def controleer_of_begrip_al_bestaat(self, informatie:dict) -> bool:
        resultaat_query = self.session.execute(text("""
            SELECT Begrip.begrip_id
            FROM Begrip
            JOIN Begrippenkader ON Begrippenkader.begrippenkader_id = Begrip.FK_begrippenkader_id
            WHERE UPPER(:voorkeursterm) = UPPER(Begrip.voorkeursterm)
                AND UPPER(:naam_begrippenkader) = UPPER(Begrippenkader.naam_begrippenkader)
            LIMIT 1;
        """),
        {
                    "naam_begrippenkader": informatie["naam_begrippenkader"],
                    "voorkeursterm": informatie["voorkeursterm"]
                }
        )

        bestaat = False

        for _ in resultaat_query:
            bestaat = True

        return bestaat


    def controleer_of_alternatieve_term_bestaat(self, informatie:dict) -> bool:
        resultaat_query = self.session.execute(text("""
            SELECT begrippenkader_id
            FROM Begrippenkader
            WHERE UPPER(:naam_begrippenkader) = UPPER(naam_begrippenkader)
            LIMIT 1;
        """),
        {
                    "naam_begrippenkader": informatie["naam_begrippenkader"],
                }
        )

        bestaat = False

        for _ in resultaat_query:
            bestaat = True

        return bestaat

    def controleer_of_alternatieve_term_bestaat(self, informatie:dict) -> bool:
        resultaat_query = self.session.execute(text("""
            SELECT Alternatieve_term.alternatieve_term_id
            FROM Alternatieve_term
            JOIN Begrippenkader ON Begrippenkader.begrippenkader_id = Alternatieve_term.FK_begrippenkader_id
            JOIN Begrip ON Begrip.begrip_id = Alternatieve_term.FK_begrip_id  
            WHERE UPPER(:voorkeursterm) = UPPER(Begrip.voorkeursterm)
                AND UPPER(:naam_begrippenkader) = UPPER(Begrippenkader.naam_begrippenkader)
                AND UPPER(:alternatieve_term) = UPPER(Alternatieve_term.alternatieve_term)
            LIMIT 1;
        """),
        {
                    "naam_begrippenkader": informatie["naam_begrippenkader"],
                    "voorkeursterm": informatie["voorkeursterm"],
                    "alternatieve_term": informatie["alternatieve_term"]
                }
        )

        bestaat = False

        for _ in resultaat_query:
            bestaat = True

        return bestaat
