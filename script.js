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
    
    

    // for (var yr in F1_DATA) {
    //     for (var gp in F1_DATA[yr]) {

    //     }
    // }

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
        var finalStr = ""
        var splitstr = str.split(" ")
        for (var substr in splitstr) {
            finalStr = finalStr + splitstr[substr][0].toUpperCase() + splitstr[substr].slice(1, 999) + " "
        }
        splitstr = finalStr.split("-")
        finalStr = ""
        for (var substr in splitstr) {
            finalStr = finalStr + splitstr[substr][0].toUpperCase() + splitstr[substr].slice(1, 999) + "-"
        }
        finalStr = num + ": " +finalStr.slice(0, -2)
        option.innerHTML = finalStr;
        loc_dropdown.appendChild(option);
    }

    refreshSessions();
}

function refreshSessions() {
    location_sessions = F1_DATA[year_dropdown.options[year_dropdown.selectedIndex].value][loc_dropdown.options[loc_dropdown.selectedIndex].value];
    session_dropdown = document.getElementById("session_dropdown");
    session_dropdown.innerHTML = '';
    for (i = Object.keys(location_sessions).length-1; i >= 0; i--) {
        if (Object.values(location_sessions)[i].includes("f3") || 
        Object.values(location_sessions)[i].includes("f2") || 
        Object.values(location_sessions)[i].includes("supercup") || 
        Object.values(location_sessions)[i].includes("psc")) {
            console.log("Removed", Object.keys(location_sessions)[i]);
            continue;
        }
        option = document.createElement("option");
        option.setAttribute("value", Object.values(location_sessions)[i]);
        console.log("value", Object.values(location_sessions)[i])
        option.innerHTML = Object.keys(location_sessions)[i];
        session_dropdown.appendChild(option);
    }
}

function updateLink() {
    
    final_link = session_dropdown.options[session_dropdown.selectedIndex].value
    console.log(final_link);
    
}

function copyLink() {
    copyToClipboard(final_link);
}

