function migrateIfNeeded(data) {
    if(!data.price){
        data.price = "-1";
    }else if(data.price.includes("$")){
        data.price = data.price.replace("$", "");
    }
    if(typeof data.price === "string"){
        data.price = parseFloat(data.price);
    }
    return data;
}


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
                        return migrateIfNeeded({...statistic, ...JSON.parse(statistic.data)});
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

                    let prodLink = document.createElement("a");
                    prodLink.className = "product-link";
                    prodLink.href = webpageInfo.url;
                    prodLink.innerText = webpageInfo.url;
                    dataDiv.appendChild(prodLink);

                    let priceDiv = document.createElement("div");
                    priceDiv.className = "product-last-price";
                    priceDiv.innerText = "Last price: " + collectedWebpageData[0].price;
                    dataDiv.appendChild(priceDiv);

                    let priceGraph = document.createElement("canvas");
                    priceGraph.className = "product-price-graph";
                    priceGraph.id = "price-graph-" + product.id + "-" + webpage.id;
                    priceGraph.width = "800";
                    priceGraph.height = "600";

                    // maxmin
                    let arrMax = collectedWebpageData.map(s => s.price).reduce((a,b) => Math.max(a,b));
                    let arrMin = collectedWebpageData.map(s => s.price).reduce((a,b) => Math.min(a,b));

                    console.log(collectedWebpageData);
                    console.log(arrMin,arrMax,collectedWebpageData[0].date, collectedWebpageData[collectedWebpageData.length - 1].date);
                    let points = collectedWebpageData.map(statistic => {
                        return {
                            x: statistic.date,
                            y: statistic.price
                        };
                    });

                    console.log(points);
                    
                    let priceGraphobj = new Chart(priceGraph.getContext("2d"), {
                        type: "line",
                        datasets: [{
                            label: "Price",
                            data: points,
                           // borderWidth: 1,
                           // backgroundColor: 'rgb(255, 99, 132)',
                           // borderColor: 'rgb(255, 99, 132)',
                          //  borderColor: "#ff0400",
                          //  backgroundColor: "#ff0400",
                        }],
                        options:{
                            scales: {
                                x:{
                                    min: collectedWebpageData[collectedWebpageData.length - 1].date,
                                    max: collectedWebpageData[0].date,
                                    type: "linear"
                                },
                                y:{
                                    min: arrMin - 10,
                                    max: Math.max(arrMax,arrMin + 10) + 10,
                                    type: "linear"
                                }
                            }
                        }
                    });
                    window.lc = priceGraphobj;

                    console.log(priceGraphobj);

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