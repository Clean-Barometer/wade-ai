var uriBeginning = "data:image/jpeg;base64,"

data.forEach(function(myDoc) {

    var element = document.createElement("IMG");
    element.classList.add("miniImage");
    element.addEventListener('click', function() {
        document.getElementById("img01").src = element.src;
        document.getElementById("modal01").style.display = "block";
    }, false);
    element.src = uriBeginning + myDoc.predictedImage;
    var marker = L.marker(myDoc.loc.coordinates)
        .bindPopup(element)
        .addTo(map);
})

// img.onclick = 
function expandImage() {
    modal.style.display = "block";
    modalImg.src = this.src;
    captionText.innerHTML = this.alt;
}

// document.getElementById("img").src = icon_url;
// var x = document.createElement("IMG");
// x.src = icon_url;
// var marker = L.marker([51.508, -0.11])
//     .bindPopup(x)
//     .addTo(map);