async function laadBegrippenkaders() {
    const response = await fetch("http://127.0.0.1:5000/alle_begrippen_met_begrippenkaders/");

    const begrippenkaders = await response.json();
    console.log(begrippenkaders);

    const grid = document.getElementById("begrippenrooster");

    begrippenkaders.forEach(kader => {

        // Hele begrippenkader
        const kaderElement = document.createElement("div");
        kaderElement.classList.add("begrippenkader");


        // Titel
        const titel = document.createElement("div");
        titel.classList.add("begrippenkader-titel");

        const link = document.createElement("a");
        link.classList.add("begrippenkader_link");

        link.textContent =
            "Begrippenkader " + kader.naam_begrippenkader + " ↗";

        link.href =
            "/begrippenkader?begrippenkader_id=" + kader.begrippenkader_id;

        titel.appendChild(link);


        // Container voor begrippen
        const begrippenLijst = document.createElement("div");
        begrippenLijst.classList.add("begrippen-lijst");




        // Alle begrippen binnen dit kader
        kader.begrippen_tot_begrippenkader.forEach(begrip => {

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


        kaderElement.appendChild(titel);
        kaderElement.appendChild(begrippenLijst);

        grid.appendChild(kaderElement);
    });
}


laadBegrippenkaders();