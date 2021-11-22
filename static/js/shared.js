function constructAlert(parent,type,text){
    let alert = document.createElement("div");
    alert.className = "alert alert-dismissible fade show alert-" + type;
    alert.setAttribute("role","alert");
    let p = document.createElement("p");
    alert.innerText = text;
    alert.appendChild(p);
    let x = document.createElement("button");
    x.innerHTML = "<span aria-hidden=\"true\">&times;</span>";
    x.className = "close";
    x.setAttribute("data-dismiss", "alert");
    x.setAttribute("type","button");
    alert.appendChild(x);
    parent.appendChild(alert);
}


function set_alert_success(text){
    document.getElementById("alerts").innerHTML = "";
    constructAlert(document.getElementById("alerts"), "success", text);
}

function set_alert_danger(text){
    document.getElementById("alerts").innerHTML = "";
    constructAlert(document.getElementById("alerts"), "danger", text);
}

function wipe_forms(){
    Array.from(document.getElementsByTagName("forms")).forEach(elem => {
        let type = elem.getAttribute("type");
        if(type == "text" || type == "password"){
            elem.value = ""; // clear
        }
    })
}