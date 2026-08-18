var parameters = new URLSearchParams(window.location.search);
const begripId=parameters.get('begrip_id');
const voorkeursterm=parameters.get('voorkeursterm');
const begrippenkader = parameters.get('naam_begrippenkader');
const begrip_naam = document.querySelector("#begrip_naam")
const port_website="3500"



async function laadBegrippenkaders() {


    if (begripId != null) {
        response = await fetch("http://127.0.0.1:5000/geef_begrip_details?begrip_id=" + begripId);
    }
    if (voorkeursterm != null && begrippenkader != null && begripId == null) {
        response = await fetch("http://127.0.0.1:5000/geef_begrip_details?naam_begrippenkader=" + kaderNaam +"&voorkeursterm=" + voorkeursterm);
    }
    if (begripId == null && kaderNaam == null && begripId == null) {

        begrip_naam.textContent = "Gebruik ?id= of ?naam_begrippenkader= en ?voorkeursterm= om de begrip te bekijken"
    }

    const begrip = await response.json();
    console.log(begrip);


    if (!Object.hasOwn(begrip, 'fout')) {

        begrip.forEach(kader => {

            document.getElementById("begrip_naam").textContent = kader.voorkeursterm


            document.getElementById("begrip_status").textContent =kader.status_naam
            document.getElementById("begrip_aangemaakt_op").textContent =kader.aangemaakt_op
            document.getElementById("begrip_gewijzigd_op").textContent =kader.gewijzigd_op
            document.getElementById("link_naam_begrippenkader").textContent = kader.naam_begrippenkader

            //TODO: Links genereren zoals hier
            document.getElementById("link_naam_begrippenkader").href = "/begrippenkader?naam_begrippenkader=" + kader.naam_begrippenkader

            kader.alternatieve_termen.forEach(term => {
                //const lijst = ;
                const item = document.createElement("span");

                item.textContent = term.alternatieve_term;
                item.classList.add("alternatieve_term");

                document.getElementById("alternatieve_termen_lijst").appendChild(item);
            })

            document.getElementById("definitie_begrip").textContent = kader.definitie_begrip
            document.getElementById("toelichting_begrip").textContent = kader.toelichting_begrip
            document.getElementById("voorbeeld_begrip").textContent = kader.voorbeeld_begrip

            document.getElementById("heeft_bron").textContent = kader.bron


            document.getElementById("status").textContent = kader.status_naam
            document.getElementById("vervalt_op").textContent = kader.vervalt_op
            document.getElementById("begrip_code").textContent = kader.begrip_code
            document.getElementById("aangemaakt_door_functie").textContent = kader.functie_naam






        });
    } else {

        begrip_naam.textContent = begrip.fout
    }
}


laadBegrippenkaders();