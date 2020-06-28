$.getJSON('data.json', function(f1data) {
    F1_DATA = f1data;
    success: buildPage();
});

const copyToClipboard = str => {
    if (!navigator.clipboard){
        const el = document.createElement('textarea');
        el.value = str;
        document.body.appendChild(el);
        el.select();
        document.execCommand('copy');
        document.body.removeChild(el);
    } else {
        navigator.clipboard.writeText(str).then(
            function(){
            })
        .catch(
            function() {
                alert("Couldn't copy URL to clipboard"); // error
        });
    }       
};

function buildPage() {
    var years = [...Object.getOwnPropertyNames(F1_DATA).reverse()];

    year_dropdown = document.getElementById("year_dropdown");
    gp_dropdown = document.getElementById("gp_dropdown");
    session_dropdown = document.getElementById("session_dropdown");
    for (i = 0; i < years.length; i++) {
        option = document.createElement("option");
        option.setAttribute("value", years[i]);
        option.innerHTML = years[i];
        year_dropdown.appendChild(option)
    }

    loadState();
    updateLink();
};

function refreshGP() {
    year_gps = F1_DATA[year_dropdown.options[year_dropdown.selectedIndex].value];
    gp_dropdown.innerHTML = '';
    for (i = 0; i < Object.keys(year_gps).length; i++) {
        var gp = Object.keys(year_gps)[i];
        option = document.createElement("option");
        option.setAttribute("value", gp);
        var str = gp.split("_")[1];
        var num = gp.split("_")[0];
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
        gp_dropdown.appendChild(option);
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
    sessions_in_gp = F1_DATA[year_dropdown.options[year_dropdown.selectedIndex].value][gp_dropdown.options[gp_dropdown.selectedIndex].value];
    session_dropdown.innerHTML = '';

    outerloop:
    for (i = Object.keys(sessions_in_gp).length-1; i >= 0; i--) {
        for (j = 0; j < filters.length;j++){
            if (Object.keys(sessions_in_gp)[i].toLowerCase().includes(filters[j])) {
                console.log("Removed '", Object.keys(sessions_in_gp)[i], "' based on filters");
                continue outerloop;
            }
        }
        option = document.createElement("option");
        option.setAttribute("value", Object.values(sessions_in_gp)[i]);
        option.innerHTML = Object.keys(sessions_in_gp)[i];
        session_dropdown.appendChild(option);
    }

    
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
    localStorage.setItem("saved_gp_index", gp_dropdown.selectedIndex);
    localStorage.setItem("saved_session_index", session_dropdown.selectedIndex);
}

function loadState() {
    saved_year_index = localStorage.getItem("saved_year_index");
    saved_gp_index = localStorage.getItem("saved_gp_index");
    saved_session_index = localStorage.getItem("saved_session_index");

    year_dropdown.selectedIndex = saved_year_index;
    refreshGP();
    gp_dropdown.selectedIndex = saved_gp_index;
    refreshSessions();
    session_dropdown.selectedIndex = saved_session_index;
    saveState();
}

function changeSelection(p_which_select_menu, p_by_how_much) {
    if (p_which_select_menu == "year") {
        if (year_dropdown.options[year_dropdown.selectedIndex + p_by_how_much] != undefined) {
            year_dropdown.selectedIndex = year_dropdown.selectedIndex + p_by_how_much;
            refreshGP();
        }
    }
    if (p_which_select_menu == "gp") {
        if (gp_dropdown.options[gp_dropdown.selectedIndex + p_by_how_much] != undefined) {
            gp_dropdown.selectedIndex = gp_dropdown.selectedIndex + p_by_how_much;
            refreshSessions();
        }
    }
    if (p_which_select_menu == "session") {
        if (session_dropdown.options[session_dropdown.selectedIndex + p_by_how_much] != undefined) {
            session_dropdown.selectedIndex = session_dropdown.selectedIndex + p_by_how_much;
        }
    }
}