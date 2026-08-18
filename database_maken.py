from sqlalchemy import create_engine
from sqlalchemy import text



def maak_database(database_naam:str) -> None:
    engine = create_engine(f'sqlite:///databases/{database_naam}.db')
    connection = engine.connect()

    transaction = connection.begin()

    #####
    ## INSTELLEN
    ####
    connection.execute(text("""
    PRAGMA foreign_keys = ON;
    """))
    transaction.commit()

    transaction = connection.begin()

    connection.execute(text("""
    PRAGMA case_sensitive_like = false;
    """))
    transaction.commit()


    transaction = connection.begin()

    #####
    ## DATABASE MAKEN
    ####
    connection.execute(text("""
    create table  Status
    (
        status_id INTEGER primary key autoincrement,
        status    VARCHAR(255)
    );
    """))

    connection.execute(text("""
    create table Functie
    (
        functie_id      INTEGER primary key autoincrement,
        FK_status_id               INTEGER not null ,
        omschrijving_functie         VARCHAR(255), -- Limiteer tot 255 woorden
    
        functie_naam        VARCHAR(255),
        FOREIGN KEY (FK_status_id)   REFERENCES Status(status_id)
    
    );
    """))

    connection.execute(text("""
    create table Rol
    (
        rol_id               INTEGER primary key autoincrement,
        rol_naam             VARCHAR(255)
        
    );
    """))

    connection.execute(text("""
    CREATE table Gebruiker
    (
        gebruiker_id            INTEGER primary key autoincrement,
        FK_rol_id               INTEGER not null ,
        FK_functie_id           INTEGER not null,
        FK_status_id            INTEGER not null ,
        voornaam                VARCHAR(255) not null ,
        achternaam              VARCHAR(255) not null ,
        gehele_naam             VARCHAR(255) not null ,
        e_mail                  VARCHAR(255) not null ,
    
    
        FOREIGN KEY (FK_rol_id) REFERENCES Rol(rol_id),
        FOREIGN KEY (FK_status_id)   REFERENCES Status(status_id),
        FOREIGN KEY (FK_functie_id) REFERENCES Functie(functie_id)
    );
    """))

    connection.execute(text("""
    create table Begrippenkader
    (
        begrippenkader_id       INTEGER primary key autoincrement,
        FK_functie_id           INTEGER not null ,
        FK_status_id            INTEGER not null ,
        naam_begrippenkader     VARCHAR(255) not null ,
        omschrijving            VARCHAR(255),
        aangemaakt_op           VARCHAR(255) not null ,
        gewijzigd_op            VARCHAR (255),
        vervalt_op              VARCHAR(255),
    
        FOREIGN KEY (FK_functie_id) REFERENCES Functie(functie_id),
        FOREIGN KEY (FK_status_id)  REFERENCES Status(status_id)
    );
    """))

    connection.execute(text("""
    CREATE table Begrip_code
    (
        begrip_code_id INTEGER primary key autoincrement,
        code            VARCHAR(255),
        begrip_code_betekenis TEXT
    );
    """))

    connection.execute(text("""
    create table Begrip
    (
        begrip_id               INTEGER primary key autoincrement,
        FK_functie_id           INTEGER not null ,
        FK_status_id            INTEGER not null ,
        FK_begrippenkader_id    INTEGER not null ,
        FK_begrip_code_id       INTEGER,
        voorkeursterm           VARCHAR(255) not null,
        definitie_begrip        VARCHAR(255), -- Limiteer gebruiker in aantal karakters tot 255
        toelichting_begrip      TEXT,
        voorbeeld_begrip        TEXT,
        aangemaakt_op           VARCHAR(255) not null ,
        gewijzigd_op            VARCHAR (255),
        vervalt_op              VARCHAR(255),
        bron                    TEXT,
         
        FOREIGN KEY  (FK_begrip_code_id) REFERENCES  Begrip_code(Begrip_code_id),
        FOREIGN KEY (FK_functie_id) REFERENCES Functie(functie_id),
        FOREIGN KEY (FK_status_id)   REFERENCES Status(status_id),
        FOREIGN KEY (FK_begrippenkader_id) REFERENCES Begrippenkader(begrippenkader_id)
    );
    """))

    connection.execute(text("""
    create table Alternatieve_term
    (
        alternatieve_term_id    INTEGER primary key autoincrement,
        alternatieve_term       VARCHAR(255) not null ,
        FK_begrip_id            INTEGER not null ,
        FK_status_id            INTEGER not null,
        FK_functie_id           INTEGER not null ,
        FK_begrippenkader_id    INTEGER not null ,
        aangemaakt_op           VARCHAR(255) not null ,
        gewijzigd_op            VARCHAR (255),
        vervalt_op              VARCHAR(255),
    
        FOREIGN KEY (FK_begrip_id) REFERENCES Begrip(begrip_id),
        FOREIGN KEY (FK_status_id) REFERENCES Status(status_id),
        FOREIGN KEY (FK_functie_id ) REFERENCES Functie(functie_id),
        FOREIGN KEY (FK_begrippenkader_id) REFERENCES Begrippenkader(begrippenkader_id)
    );
    """))

    transaction.commit()

    #####
    ## DATABASE VULLEN VOOR MVP
    ####
    transaction = connection.begin()

    connection.execute(text("""
        INSERT INTO Rol (rol_naam)
            VALUES ("Testgegruiker")
    """))


    connection.execute(text("""
        INSERT INTO Begrip_code (begrip_code_betekenis, code)
            VALUES ("Testcode", "Test-001")
    """))


    connection.execute(text("""
        INSERT INTO Status (status)
            VALUES ("Status_test")
    """))

    connection.execute(text("""
        INSERT INTO Functie (FK_status_id, omschrijving_functie, functie_naam)
            VALUES (
                (SELECT status_id 
                FROM Status 
                WHERE UPPER(status) = UPPER("status_test") 
                LIMIT 1),
                "Test functie", "Functie1")
    """))

    connection.execute(text("""
        INSERT INTO Gebruiker(FK_rol_id, FK_functie_id, FK_status_id, voornaam, achternaam, gehele_naam, e_mail)
        VALUES (
                (SELECT rol_id FROM Rol where UPPER(rol_naam) = UPPER(:rol_naam)),
                (SELECT functie_id FROM Functie where UPPER(functie_naam) = UPPER(:functie_naam)),
                (SELECT status_id FROM Status where UPPER(status) = UPPER(:status)
               ),
                 :voornaam, :achternaam, :gehele_naam, :email)
        """),
                    {
                        "rol_naam": "Testgegruiker",
                        "functie_naam": "Functie1",
                        "status": "Status_test",
                        "voornaam": "Gebruiker1",
                        "achternaam": "X",
                        "gehele_naam": "Gebruiker1",
                        "email": "x@x.x"
                    }
        )
    transaction.commit()

    connection.close()


