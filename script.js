$.getJSON('data.json', function(f1data) {
    F1_DATA = f1data;
    success: buildPage();
});

const copyToClipboard = str => {
    const el = document.createElement('textarea');
    el.value = str;
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
};

function buildPage() {
    var years = [...Object.getOwnPropertyNames(F1_DATA).reverse()];

    year_dropdown = document.getElementById("year_dropdown");
    for (i = 0; i < years.length; i++) {
        option = document.createElement("option");
        option.setAttribute("value", years[i]);
        option.innerHTML = years[i];
        year_dropdown.appendChild(option)
    }

    loadState();
    refreshGP();
    refreshSessions();
    updateLink();
};

function refreshGP() {
    year_locations = F1_DATA[year_dropdown.options[year_dropdown.selectedIndex].value];
    loc_dropdown = document.getElementById("loc_dropdown");
    loc_dropdown.innerHTML = '';
    for (i = 0; i < Object.keys(year_locations).length; i++) {
        var location = Object.keys(year_locations)[i];
        option = document.createElement("option");
        option.setAttribute("value", location);
        var str = location.split("_")[1];
        var num = location.split("_")[0];
        var finalStr = "";
        var splitstr = str.split(" ");
        for (var substr in splitstr) {
            finalStr = finalStr + splitstr[substr][0].toUpperCase() + splitstr[substr].slice(1, 999) + " ";
        }
        splitstr = finalStr.split("-");
        finalStr = "";
        for (var substr in splitstr) {
            finalStr = finalStr + splitstr[substr][0].toUpperCase() + splitstr[substr].slice(1, 999) + "-";
        }
        finalStr = num + ": " +finalStr.slice(0, -2);
        option.innerHTML = finalStr;
        loc_dropdown.appendChild(option);
    }
    refreshSessions();
}

function refreshSessions() {
    var conditions = []
    var options = ["f2", "f3", "supercup", "psc"]
    var filters = []
    conditions[0] = document.getElementById("f2-checkbox").checked;
    conditions[1] = document.getElementById("f3-checkbox").checked;
    conditions[2] = document.getElementById("supercup-checkbox").checked;
    conditions[3] = conditions[2]

    for (i = 0; i < conditions.length; i++) {
        if (conditions[i]) {
            filters[i] = "asdfasdfasdf"
        } else {
            filters[i] = options[i]
        }
    }
    location_sessions = F1_DATA[year_dropdown.options[year_dropdown.selectedIndex].value][loc_dropdown.options[loc_dropdown.selectedIndex].value];
    session_dropdown = document.getElementById("session_dropdown");
    session_dropdown.innerHTML = '';

    outerloop:
    for (i = Object.keys(location_sessions).length-1; i >= 0; i--) {
        for (j = 0; j < filters.length;j++){
            if (Object.keys(location_sessions)[i].toLowerCase().includes(filters[j])) {
                console.log("Removed '", Object.keys(location_sessions)[i], "' based on filters");
                continue outerloop;
            }
        }
        option = document.createElement("option");
        option.setAttribute("value", Object.values(location_sessions)[i]);
        option.innerHTML = Object.keys(location_sessions)[i];
        session_dropdown.appendChild(option);
    }

    saveState();
}

function updateLink() {
    final_link = session_dropdown.options[session_dropdown.selectedIndex].value;
}

function copyLink() {
    copyToClipboard(final_link);
}

function saveState() {
    localStorage.clear();
    localStorage.setItem("saved_year_index", year_dropdown.selectedIndex);
    localStorage.setItem("saved_gp_index", loc_dropdown.selectedIndex);
    localStorage.setItem("saved_session_index", session_dropdown.selectedIndex);
}

function loadState() {

    saved_year_index = localStorage.getItem("saved_year_index");
    saved_gp_index = localStorage.getItem("saved_gp_index");
    saved_session_index = localStorage.getItem("saved_session_index");

    year_dropdown.selectedIndex = saved_year_index;
    loc_dropdown.selectedIndex = saved_gp_index;
    session_dropdown.selectedIndex = saved_session_index;
}

function changeSelection(whichSelectMenu, byHowMuch) {
    if (whichSelectMenu == "year") {
        if (year_dropdown.options[year_dropdown.selectedIndex + byHowMuch] != undefined) {
            year_dropdown.selectedIndex = year_dropdown.selectedIndex + byHowMuch;
            refreshGP();
        }
    }
    if (whichSelectMenu == "gp") {
        if (loc_dropdown.options[loc_dropdown.selectedIndex + byHowMuch] != undefined) {
            loc_dropdown.selectedIndex = loc_dropdown.selectedIndex + byHowMuch;
            refreshSessions();
        }
    }
    if (whichSelectMenu == "session") {
        if (session_dropdown.options[session_dropdown.selectedIndex + byHowMuch] != undefined) {
            session_dropdown.selectedIndex = session_dropdown.selectedIndex + byHowMuch;
        }
    }
}