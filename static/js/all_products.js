docReady(() => {
    document.getElementById("products-list").innerText = "Loading...";
    fetch("/api/all_products").then(async resp => {
        try{
            let data = await resp.json();
            let prodList = document.getElementById("products-list");
            prodList.innerText = ""; // clear
            await Promise.all(data.map(async product => {
                let prodDiv = document.createElement("div");
                prodDiv.className = "product-div card";
                prodDiv.id = "product-" + product.id;
                prodDiv.setAttribute("data-id", product.id);
                prodDiv.innerText = "Loading...";
                prodList.appendChild(prodDiv);
                let prodBody = document.createElement("div");
                prodBody.className = "card-body";
                let webpageReqResp = await fetch("/api/webpages_for/" + product.id);
                let webpageData = await webpageReqResp.json();
                prodDiv.innerText = "";
                let nameDiv = document.createElement("h3");
                nameDiv.className = "product-name card-title";
                nameDiv.innerText = product.name;
                prodBody.appendChild(nameDiv);
                let dataDiv = document.createElement("div");
                prodBody.appendChild(dataDiv);
                prodDiv.appendChild(prodBody);
                dataDiv.className = "card-text";
                dataDiv.innerText = "Loading data from " + webpageData.length + " webpages...";
                let clearedLoading = false;
                await Promise.all(webpageData.map(async webpage => {
                    let webpageReqResp = await fetch("/api/webpage/" + webpage.id);
                    let webpageInfo = await webpageReqResp.json();
                    let collectedWebpageDataReqResp = await fetch("/api/data_for/" + webpage.id);
                    let collectedWebpageData = await collectedWebpageDataReqResp.json();
                    collectedWebpageData = collectedWebpageData.sort((a, b) => {
                        return b.date - a.date;
                    }).map(statistic => {
                        return {...statistic, ...JSON.parse(statistic.data)}
                    });
                    if(!clearedLoading){
                        clearedLoading = true;
                        dataDiv.className = "product-price-data";
                        dataDiv.innerText = "";
                    }

                    let prodTitle = document.createElement("h5");
                    prodTitle.className = "product-title";
                    prodTitle.innerText = webpageInfo.name;
                    dataDiv.appendChild(prodTitle);

                    let priceDiv = document.createElement("div");
                    priceDiv.className = "product-last-price";
                    priceDiv.innerText = "Last price: " + collectedWebpageData[0].price;
                    dataDiv.appendChild(priceDiv);

                    let priceGraph = document.createElement("div");
                    priceGraph.className = "product-price-graph";
                    dataDiv.appendChild(priceGraph);

                }));
                dataDiv.className = "product-all-data";
            }));
        }catch(ex){
            set_alert_danger("Error" + ex);
        }
    }).catch(err => {
        set_alert_danger("Error" + err);
    });
});