const zoekveld = document.getElementById("zoekveld");
const resultatenlijst = document.getElementById("resultatenlijst");
const melding = document.getElementById("melding_zoeken");
const port_website="3500";


zoekveld.addEventListener("input", async function () {
    const zoekterm = zoekveld.value.trim();

    resultatenlijst.innerHTML = "";

    if (zoekterm === "") {
        melding.textContent = "Typ hierboven om te zoeken";
        return;
    }

    const response = await fetch(
        "http://127.0.0.1:5000/zoek_begrip?zoek_opdracht=" + encodeURIComponent(zoekterm)
    );

    const data = await response.json();

   if (!Object.hasOwn(data, 'fout')) {
        melding.textContent = "";
        data.forEach(begrip => {

            const resultaat = document.createElement("div");
            resultaat.classList.add("zoekresultaat");

            // const alternatieveTermen = begrip.alternatieve_termen.map(
            //     term => term.alternatieve_term
            // );
            link_voorkeursterm = "/begrip?begrip_id=" + begrip.begrip_id;
            link_begrippenkader = "/begrippenkader?naam_begrippenkader=" + begrip.naam_begrippenkader;
            resultaat.innerHTML = `
                <div class="resultaat_regel">
                    Voorkeursbegrip: <a href="${link_voorkeursterm}\" >${begrip.voorkeursterm}</a><br>

                </div>
                <div class="resultaat_regel">
                    Begrippenkader: <a href="${link_begrippenkader}\">${begrip.naam_begrippenkader}</a>

                </div>
                <div class="resultaat_regel">
                                    Alternatievetermen:
                    <span class="alternatieve-termen"></span>
                </div>
    
                <div class="resultaat_regel">
                    Definitie: ${begrip.definitie_begrip}
                </div>
            `;

            const alternatieveTermen = resultaat.querySelector(".alternatieve-termen");

            begrip.alternatieve_termen.forEach(term => {
                const span = document.createElement("span");

                span.textContent = term.alternatieve_term;
                span.classList.add("alternatieve-term");

                alternatieveTermen.appendChild(span);
            });

            resultatenlijst.appendChild(resultaat);
        });


   }else{
        melding.textContent = "Geen resultaten gevonden";
   }

});

/*
    if (data.length === 0) {
        melding.textContent = "Geen resultaten gevonden";
        return;
    }
 */