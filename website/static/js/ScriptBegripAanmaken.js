// var parameters = new URLSearchParams(window.location.search);
// const port_website="3500"

    // if (begripId != null) {
    //     response = await fetch("http://127.0.0.1:5000/geef_begrip_details?begrip_id=" + begripId);
    // }
    // if (voorkeursterm != null && begrippenkader != null && begripId == null) {
    //
    // }
    // if (begripId == null && kaderNaam == null && begripId == null) {
    //
    //     begrip_naam.textContent = "Gebruik ?id= of ?naam_begrippenkader= en ?voorkeursterm= om de begrip te bekijken"
    // }

const parameters = new URLSearchParams(window.location.search);
const kaderNaam=parameters.get('naam_begrippenkader');

async function laadKeuzeMenus() {
    const response = await fetch("http://127.0.0.1:5000/invoerschermdata");
    const data = await response.json();

    vulSelect("naam_begrippenkader", data.begrippenkaders, kaderNaam);
    vulSelect("status", data.statussen);
    vulSelect("begrip_code", data.begripcodes);
    vulSelect("aangemaakt_door_functie", data.functies);
}

function vulSelect(id, lijst, linked=null) {
    const select = document.getElementById(id);

    select.innerHTML = "";

    if (linked && lijst.includes(linked)) {

        const index_double_option = lijst.indexOf(linked)
        if (index_double_option > -1)
            lijst.splice(index_double_option, 1)
        lijst = [linked].concat(lijst);
    }
    console.log("Nieuwe lijst: ",lijst);
    lijst.forEach(item => {
        const optie = document.createElement("option");

        optie.value = item;
        optie.textContent = item;

        select.appendChild(optie);
    });
}


laadKeuzeMenus();


const begriptoevoegen = document.getElementById("begrip_toevoegen");

begriptoevoegen.addEventListener("click", async function () {

    const data = {
        invoer: {
            gehele_naam: "Gebruiker1"
        },

        status: document.getElementById("status").value,

        naam_begrippenkader: document.getElementById("naam_begrippenkader").value,

        code: document.getElementById("begrip_code").value,

        voorkeursterm:  document.getElementById("voorkeurs_term").value.trim(),

        definitie_begrip: document.getElementById("definitie_begrip").value.trim(),

        toelichting_begrip: document.getElementById("toelichting_begrip").value.trim(),

        voorbeeld_begrip: document.getElementById("voorbeeld_begrip").value.trim(),

        test_alternatieve_termen_is_leeg: document.getElementById("alternatieve_termen"),

        gewijzigd_op: "datum 2",

        vervalt_op: document.getElementById("vervalt_op").value.trim(),

        bron: document.getElementById("heeft_bron").value
    };
    console.log(data);

    if (!heeftLeegVeld(data)){
        const post_status = await maakBegripAanAPI(data);
        const d = post_status.post_status

        if (d !== "OK") {
            alert("Er is iets fout gegaan\nFout: " + d);
        } else {

            alert("Begrip is aangemaakt");
            const status_alternatieve_termen_maken = await maakAlternatieveTermen(data);
            const e = status_alternatieve_termen_maken.post_status
            if (e !== "OK") {
                alert("Er is iets fout gegaan\nFout: " + e);
            } else {
                alert("Alternatieve termen zijn aangemaakt");
            }
        }
    } else {
        alert("Vul alle velden in");
    }

});

async function maakBegripAanAPI(data) {
    const response = await fetch("http://127.0.0.1:5000/aanmaken_begrip", {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            "Content-Type": "application/json; charset=UTF-8"
        }
    });

    const status = await response.json();

    console.log(status);

    return status;
}


async function maakAlternatieveTermen(data) {
    const alternatieveTermen1 = document
    .getElementById("alternatieve_termen")
    .value
    .split(",")
    .map(term => term.trim())
    .filter(term => term !== "");

    let alternatieveTermen_geen_dubbele = [];
    alternatieveTermen1.forEach(element => {
        if (!alternatieveTermen_geen_dubbele.includes(element)) {
            alternatieveTermen_geen_dubbele.push(element);
        } else {
            alert("Alternatie term: \'"+element + " \' bestaat al, term is overgeslagen");
        }
    });



    const data_api = {
        invoer: {
            gehele_naam: "Gebruiker1"
        },

        alternatieve_termen: alternatieveTermen_geen_dubbele ,

        voorkeursterm:  document.getElementById("voorkeurs_term").value.trim(),

        naam_begrippenkader: document.getElementById("naam_begrippenkader").value,

        status: document.getElementById("status").value,

        vervalt_op: document.getElementById("vervalt_op").value.trim(),

        gewijzigd_op: "datum 2",
    };

    console.log("Alternatieve termen: "+data_api);

    const response = await fetch("http://127.0.0.1:5000/aanmaken_alternatieve_termen", {
        method: "POST",
        body: JSON.stringify(data_api),
        headers: {
            "Content-Type": "application/json; charset=UTF-8"
        }
    });

    const status = await response.json();
    console.log(status);
    return status
}

//TODO: Valideer datums
function heeftLeegVeld(object) {
    return Object.values(object).some(waarde => {
        if (typeof waarde === "object" && waarde !== null) {
            return heeftLeegVeld(waarde);
        }

        return typeof waarde === "string" && waarde.trim() === "";
    });
}

async function controleerVoorkeursterm(data){
    const voorkeursterm = document.getElementById("voorkeurs_term").value.trim();
    const begrippenkader = document.getElementById("naam_begrippenkader").value;

    if (voorkeursterm !== "") {
        const response = await fetch("http://127.0.0.1:5000/controleer_of_voorkeursterm_bestaat", {
            method: "POST",
            body: JSON.stringify(
                {
                    "voorkeursterm": voorkeursterm,
                    "naam_begrippenkader": begrippenkader
                }
            ),
            headers: {
                "Content-Type": "application/json; charset=UTF-8"
            }
        });

        const bestaat = await response.json();
        if (bestaat.controle) {
            alert("Voorkeursterm bestaat al");
        }
    }
}