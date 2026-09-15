from flask import Flask, jsonify, request
from tussen_laag import TussenLaag as Ts
from flask_cors import CORS
import re
import datetime

#TODO
#TODO: Voeg datum check nu toe aan allemaal
#TODO
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def check_datum(datum:str) -> tuple[bool,str]:
    datum_nl = "^(0?[1-9]|1[0-2])-(0?[1-9]|[12][0-9]|3[01])-(19\\d{2}|2\\d{3}|3000)$"
    tijd_nul = "00:00:00"
    datum_nu = datetime.datetime.fromisoformat(datetime.datetime.now().isoformat())


    datum = re.fullmatch(datum_nl, datum)

    if datum is not None:
        # datum_jaar = "0" if len(datum.group(3)) == 1 else "" + datum.group(3)
        datum_maand = "0" if len(datum.group(1)) == 1 else ""
        datum_dag = "0" if len(datum.group(2)) == 1 else ""
        format_iso_1 = f"{datum.group(3)}-{datum_maand+datum.group(1)}-{datum_dag+datum.group(2)}T{tijd_nul}"
        print(format_iso_1, "<<<<<<<<<<<<<<<<<<<<<<<<")
        datum_iso = datetime.datetime.fromisoformat(format_iso_1)

        return datum_iso > datum_nu, format_iso_1+"Z"

    return False, "0"

@app.route("/geef_alle_statussen", methods=['GET']  )
def geefstatusen():

    v = t.geef_alle_statussen()
    print(v)

    return jsonify(v), 201

@app.route("/geef_begrip_details", methods=['GET'])
def geef_begrip_details():
    begrip_id = request.args.get("begrip_id")
    begrippenkader = request.args.get("naam_begrippenkader")
    voorkeursterm = request.args.get("voorkeursterm")

    if begrip_id:
        return jsonify(
                t.ID_zoek_detail_begrip(
                    {
                        "begrip_id":begrip_id
                    }
                )
        ), 201

    if begrippenkader and voorkeursterm and not begrip_id:
        return jsonify(t.zoek_detail_begrip(
                    {
                        "naam_begrippenkader":begrippenkader,
                        "voorkeursterm":voorkeursterm
                    }
                )
        ), 201
    else:
        return jsonify({"informatie": "Zoekopdracht niet geldig"}), 201

@app.route("/zoek_begrip", methods=['GET'])
def zoeken_op_begrip_algemeen():
    zoekopdracht = request.args.get("zoek_opdracht")

    if zoekopdracht:
        return jsonify(
            t.zoek_begrip_algemeen(
                    {
                "zoek_opdracht":zoekopdracht
                    }
        )
        ), 201
    else:
        return jsonify({"informatie": "Zoekopdracht niet geldig"}), 201

@app.route("/alle_begrippen_met_begrippenkaders", methods=['GET'])
def alle_begrippen_met_begrippenkaders():
    return jsonify(t.geef_alle_begrippen_met_begrippenkaders()), 201

@app.route("/begrippenkader_detail", methods=['GET'])
def alle_begrippenkaders():
    naam_begrippenkader = request.args.get("naam_begrippenkader")
    begrippenkader_id = request.args.get("begrippenkader_id")
    if begrippenkader_id:
        return jsonify(t.ID_geef_begrippenkader_detail(
            {
                "begrippenkader_id":begrippenkader_id
            }
        )), 201
    if naam_begrippenkader:
        return jsonify(t.geef_begrippenkader_detail(
            {
                "naam_begrippenkader":naam_begrippenkader
            }
        )), 201
    else:
        return jsonify({"informatie": "Zoekopdracht niet geldig"}), 201



@app.route("/invoerschermdata", methods=['GET'])
def geef_invoerscherm_data():

    return jsonify(
           t.geef_invoerscherm_data()
        ), 201

@app.route("/allebegrippen", methods=['GET'])
def geef_allebegrippen():

    return jsonify(
            {
                "informatie":t.geef_alle_begrippen()
            }
        ), 201


#TODO: Alle begrippenkaders
@app.route("/aanmaken_begrip", methods=['POST'])
def aanmaken_begrip():
    data = request.get_json()

    valide_datum, datum_iso = check_datum(data["vervalt_op"])

    if not valide_datum:
        return jsonify({"post_status": "Datum is in het verleden of invalide ingevuld"}), 201

    data["vervalt_op"] = datum_iso

    if not t.controleer_of_voorkeurs_term_bestaat(data):
        w = t.aanmaken_begrip(data)

        if w is not None:
            return jsonify({"post_status": w["fout"]}), 201

        return jsonify({"post_status": "OK"}), 201

    else:
        return jsonify({"post_status": "Voorkeursterm bestaat al"}), 201

@app.route("/aanmaken_begrippenkader", methods=['POST'])
def aanmaken_begrippenkader():
    data = request.get_json()

    valide_datum, datum_iso = check_datum(data["vervalt_op"])

    if not valide_datum:
        return jsonify({"post_status": "Datum is in het verleden of invalide ingevuld"}), 201

    data["vervalt_op"] = datum_iso


    if not t.controleer_of_begrippenkader_bestaat(data):
        w = t.aanmaken_begrippenkader(data)

        if w is not None:
            return jsonify({"post_status": w}), 201

        return jsonify({"post_status": "OK"}), 201
    else:
        return jsonify({"post_status": "Begrippenkader bestaat al"}), 201

@app.route("/controleer_of_voorkeursterm_bestaat", methods=['POST'])
def controleer_of_voorkeursterm_bestaat():
    data = request.get_json()

    print("\033[32mVanaf server",data)

    if t.controleer_of_voorkeurs_term_bestaat(data):
        return jsonify({"controle": True}), 201
    else:
        return jsonify({"controle": False}), 201

@app.route("/controleer_of_begrippenkader_bestaat", methods=['POST'])
def controleer_of_begrippenkader_bestaat():
    data = request.get_json()

    print("\033[32mVanaf server",data)

    if t.controleer_of_begrippenkader_bestaat(data):
        return jsonify({"controle": True}), 201
    else:
        return jsonify({"controle": False}), 201



@app.route("/aanmaken_alternatieve_termen", methods=['POST'])
def aanmaken_alternatieve_termen():
    data = request.get_json()

    print("\033[32mVanaf server",data)

    w = t.aanmaken_alternatieve_term(data)

    if w is not None:
        return jsonify({"post_status": w["fout"]}), 201

    return jsonify({"post_status": "OK"}), 201



if __name__ == '__main__':
    t = Ts("T03")
    t.controleer_of_database_bestaat()
    app.run(debug=True, port=5000 )