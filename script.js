var years = [];
var locations = {
    "Australia: Albert Park (Melbourne)": "australian",
    "Bahrain: Bahrain": "bahrain",
    "China: Shanghai": "chinese",
    "Azerbaijan: Baku": "azerbaijan",
    "Spain: Barcelona": "spanish",
    "Monaco: Monaco": "monaco",
    "Canada: Gilles-Villeneuve (Montreal)": "canadian",
    "France: Paul Ricard (Le Castellet)": "french",
    "Austria: Red Bull Ring (Spielberg)": "austrian",
    "Great Britain: Silverstone": "british",
    "Germany: Hockenheimring": "german",
    "Hungary: Hungaroring (Mogyorod)": "hungarian",
    "Belgium: Spa-Franchorchamps": "belgian",
    "Italy: Monza": "italian",
    "Singapore: Marina Bay": "singapore",
    "Japan: Suzuka": "japanese",
    "Mexico: Mexico City": "mexican",
    "USA: CoTA": "united-states",
    "Brazil: Interlagos": "brazilian",
    "Abu Dhabi: Yas Marina": "abu-dhabi"
}

var sessions = {
    "Race": "race",
    "Qualifying": "qualifying",
    "Practice 1": "practice-1",
    "Practice 2": "practice-2",
    "Practice 3": "practice-3"
}

var final_link = ""
const link_start = "https://f1tv.formula1.com/en/archive/"

const copyToClipboard = str => {
    const el = document.createElement('textarea');
    el.value = str;
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
};

function buildPage() {
    for (i = 2020; i > 1981; i--) {
        years.push(i);
    }

    year_dropdown = document.getElementById("year_dropdown");
    for (i = 0; i < years.length; i++) {
        option = document.createElement("option");
        option.setAttribute("value", years[i]);
        option.innerHTML = years[i];
        year_dropdown.appendChild(option)
    }
    
    loc_dropdown = document.getElementById("loc_dropdown");
    for (i = 0; i < Object.keys(locations).length; i++) {
        option = document.createElement("option");
        option.setAttribute("value", Object.values(locations)[i]);
        option.innerHTML = Object.keys(locations)[i];
        loc_dropdown.appendChild(option)
    }

    session_dropdown = document.getElementById("session_dropdown");
    for (i = 0; i < Object.keys(sessions).length; i++) {
        option = document.createElement("option");
        option.setAttribute("value", Object.values(sessions)[i]);
        option.innerHTML = Object.keys(sessions)[i];
        session_dropdown.appendChild(option)
    }
};

function updateLink() {
    year = year_dropdown.options[year_dropdown.selectedIndex].value;
    loc = loc_dropdown.options[loc_dropdown.selectedIndex].value;
    session = session_dropdown.options[session_dropdown.selectedIndex].value;
    
    final_link = link_start + year + "/" + loc + "-grand-prix/" + year + "-" + loc + "-grand-prix-" + session;
    console.log(final_link);
    
}

function generateLink() {
    copyToClipboard(final_link);
}

