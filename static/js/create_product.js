docReady(() => {
    document.getElementById("product-creation-form").addEventListener("submit", (ev) => {
        fetch("/api/product_name/" + document.getElementById("product-name").value,{
            method: "POST"
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