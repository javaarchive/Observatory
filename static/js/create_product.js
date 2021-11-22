docReady(() => {
    document.getElementById("product-creation-form").addEventListener("submit", (ev) => {
        fetch("/api/product_name/" + document.getElementById("product-name").value,{
            method: "POST"
        }).then(res => res.json()).then(data => {
            if(data.ok){
                show_alert_success("Action successful!");
                wipe_forms();
            }else{
                show_alert_danger("Server error: " + data.message);
            }
        });
        ev.preventDefault();
        return false;
    });
});