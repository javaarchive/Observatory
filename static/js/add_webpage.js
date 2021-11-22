docReady(() => {
    document.getElementById("add-webpage-form").addEventListener("submit", (ev) => {
        fetch("/api/add_webpage_for_product/" + document.getElementById("product-name").value,{
            method: "POST",
            headers:{
                "Content-Type": "application/json"
            },body:JSON.stringify({
                "url": document.getElementById("url").value,
                "name": document.getElementById("name").value
            })
        }).catch(err => {
            set_alert_danger("Bad server resp " + err.message);
        }).then(res => res.json()).then(data => {
            if(data.status == "ok"){
                set_alert_success("Action successful!");
                wipe_forms();
            }else{
                set_alert_danger("Server error: " + data.message);
            }
        });
        ev.preventDefault();
        return false;
    });
});