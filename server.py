from flask import Flask, jsonify, request
from tussen_laag import TussenLaag as ts
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


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
    t = ts("A16")
    t.controleer_of_database_bestaat()
    app.run(debug=True, port=5000 )