//loadding screen
$(window).on('load', () => {
    //let loader = document.querySelector(".loader-wrapper")
    let txt1 = document.getElementById("waitingtxt1")
    let txt2 = document.getElementById("waitingtxt2")
    txt1.style.webkitTextStroke = "1px var(--main-color1)"
    txt2.style.color = 'var(--main-color1)'
    txt1.innerHTML = "LOADING"
    txt2.innerHTML = "LOADING"
    //loader.className += " hidden"
    $('.loader-wrapper').fadeOut("slow");
});
//waiting training show page
$("#myTraining").on('click', () => {
    //let loader = document.getElementById('loaderpage')
    let txt1 = document.getElementById("waitingtxt1")
    let txt2 = document.getElementById("waitingtxt2")
    txt1.style.webkitTextStroke = "1px blue"
    txt2.style.color = 'blue'
    txt1.innerHTML = "TRAINING"
    txt2.innerHTML = "TRAINING"
    $('.loader-wrapper').fadeIn("slow");
    //loader.className = loader.className.replace(/(?:^|\s)hidden(?!\S)/g, '')
});