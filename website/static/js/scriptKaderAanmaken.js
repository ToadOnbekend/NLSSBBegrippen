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

async function laadKeuzeMenus() {
    const response = await fetch("http://127.0.0.1:5000/invoerschermdata");
    const data = await response.json();

    vulSelect("status", data.statussen);
    vulSelect("aangemaakt_door_functie", data.functies);
}

function vulSelect(id, lijst) {
    const select = document.getElementById(id);

    select.innerHTML = "";

    lijst.forEach(item => {
        const optie = document.createElement("option");

        optie.value = item;
        optie.textContent = item;

        select.appendChild(optie);
    });
}


laadKeuzeMenus();


const begriptoevoegen = document.getElementById("begrippenkader_toevoegen");

begriptoevoegen.addEventListener("click", async function () {

    const data = {
        invoer: {
            gehele_naam: "Gebruiker1"
        },

        status: document.getElementById("status").value,

        naam_begrippenkader: document.getElementById("naam_begrippenkader_invulveld").value.trim(),

        omschrijving: document.getElementById("omschrijving_begrippenkader").value.trim(),

        gewijzigd_op: "datum 2",

        vervalt_op: document.getElementById("vervalt_op").value.trim(),

    };
    console.log(data);

    if (!heeftLeegVeld(data)){
        const post_status = await maakBegrippenkaderAanAPI(data);
        const d = post_status.post_status

        if (d !== "OK") {
            alert("Er is iets fout gegaan\nFout: " + d);
        } else {
            alert("Begrippenkader is aangemaakt");
            location.reload();
        }
    } else {
        alert("Vul alle velden in aangegeven met \"*\"");
    }

});

async function maakBegrippenkaderAanAPI(data) {
    const response = await fetch("http://127.0.0.1:5000/aanmaken_begrippenkader", {
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




//TODO: Valideer datums
function heeftLeegVeld(object) {
    return Object.values(object).some(waarde => {
        if (typeof waarde === "object" && waarde !== null) {
            return heeftLeegVeld(waarde);
        }

        return typeof waarde === "string" && waarde.trim() === "";
    });
}

async function controleerKader(data){

    const begrippenkader = document.getElementById("naam_begrippenkader_invulveld").value.trim();

    if (begrippenkader !== "") {
        const response = await fetch("http://127.0.0.1:5000/controleer_of_begrippenkader_bestaat", {
            method: "POST",
            body: JSON.stringify(
                {
                    "naam_begrippenkader": begrippenkader
                }
            ),
            headers: {
                "Content-Type": "application/json; charset=UTF-8"
            }
        });

        const bestaat = await response.json();
        if (bestaat.controle) {
            alert("Begrippenkader bestaat al");
        }
    }
}