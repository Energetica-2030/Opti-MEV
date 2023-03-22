let selectButton = document.getElementById("selectButton");
selectButton.addEventListener("click", ()=>{
    let iframeMapa = document.getElementById("map");
    let selection = document.getElementById("route");
    if(selection.value!='0'){
        iframeMapa.style.display = "block";
    }
    else{
        iframeMapa.style.display = "none";
    }
});