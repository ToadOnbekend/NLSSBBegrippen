const parameters = new URLSearchParams(window.location.search);
const kaderId=parameters.get('begrippenkader_id');
const kaderNaam=parameters.get('naam_begrippenkader');
const begrippenkader_tekst = document.querySelector("#naam_begrippenkader p")
const link_aanmaken_begrip = document.getElementById("link_aanmaken_begrip")

const port_website="3500"

async function laadBegrippenkaders() {
   let response;

    if (kaderId != null) {
        response = await fetch("http://127.0.0.1:5000/begrippenkader_detail?begrippenkader_id=" + kaderId);
    }
    if (kaderNaam != null && kaderId == null) {
        response = await fetch("http://127.0.0.1:5000/begrippenkader_detail?naam_begrippenkader=" + kaderNaam);
    }
    if (kaderId == null && kaderNaam == null) {

        begrippenkader_tekst.textContent = "Gebruik ?id= of ?naam_begrippenkader= om de begrippenkader te bekijken"
    }


//const response = await fetch("http://127.0.0.1:5000/begrippenkader_detail?naam_begrippenkader=" + kaderNaam);
    const begrippenkaders = await response.json();
    console.log(begrippenkaders);

    const grid = document.getElementById("begrippenrooster");
    if (!Object.hasOwn(begrippenkaders, 'fout')) {

        begrippenkaders.forEach(kader => {
            begrippenkader_tekst.textContent =kader.naam_begrippenkader
            // Hele begrippenkader
            const kaderElement = document.createElement("div");
            kaderElement.classList.add("begrippenkader")

            document.getElementById("begrippenkader_status").textContent ="Status: "+kader.status_naam
            document.getElementById("begrippenkader_aangemaakt_op").textContent ="Aangemaakt: "+kader.aangemaakt_op
            document.getElementById("begrippenkader_gewijzigd_op").textContent ="Gewijzigd: "+kader.gewijzigd_op
            document.getElementById("informatie_over_kader").textContent =kader.omschrijving
            link_aanmaken_begrip.href = "/begripaanmaken?naam_begrippenkader=" + kader.naam_begrippenkader


            // Container voor begrippen
            const begrippenLijst = document.createElement("div");
            begrippenLijst.classList.add("begrippen-lijst");


            // Alle begrippen binnen dit kader
            kader.begrippen.forEach(begrip => {

                const begripElement = document.createElement("div");
                begripElement.classList.add("begrip-item");


                // Voorkeursterm
                const voorkeursterm = document.createElement("a");

                voorkeursterm.textContent = begrip.voorkeursterm;
                voorkeursterm.href = "/begrip?begrip_id=" + begrip.begrip_id;


                // Definitie-popup
                const tooltip = document.createElement("div");
                tooltip.classList.add("tooltip");

                tooltip.textContent = "Definitie: "+begrip.definitie_begrip;


                // Alles samenvoegen
                begripElement.appendChild(voorkeursterm);
                begripElement.appendChild(tooltip);

                begrippenLijst.appendChild(begripElement);
            });



            kaderElement.appendChild(begrippenLijst);

            grid.appendChild(kaderElement);
        });
    } else {
        const begrippenkader_tekst = document.querySelector("#naam_begrippenkader p")
        begrippenkader_tekst.textContent = begrippenkaders.fout
    }
}


laadBegrippenkaders();