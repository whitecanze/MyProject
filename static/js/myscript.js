//tooltip hint
$(document).ready(() => {
    $('[data-toggle="tooltip1"]').tooltip();
});

//close aleart
window.setTimeout(() => {
    $(".alert").fadeTo(500, 0).slideUp(500, () => {
        $(this).remove();
    });
}, 2000);

//toggle icon
toggleChevron = (a) => {
    $(a).find('i').toggleClass('fas fa-caret-down fas fa-caret-up');
}
togglestd = (div) => {
    $(div).find('i').toggleClass('fas fa-eye fas fa-eye-slash');
    let stdtable = document.getElementById("card-table-student")
    let mainleft = document.getElementById("main-left-content")
    let stdcontainer = document.getElementById("student-table-container")
    let stdtable2 = document.getElementById("card-table-student")
    let sjlist2 = document.getElementById("card-sj-list")
    let faclist2 = document.getElementById("card-fac-list")
    let mainrow = document.getElementById("mian-container")
    let footer = document.getElementById("footer")
    let delayInMilliseconds = 500;

    if (stdtable.className == "card showing-card") {
        stdtable.className = stdtable.className.replace(/(?:^|\s)showing-card(?!\S)/g, '')
        stdtable.className += " hide-card"

        if (stdtable2.className == "card hide-card" && sjlist2.className == "card hide-card" && faclist2.className == "card hide-card") {
            mainrow.style.display = "none"
            footer.className += " hide-card"
        } else {
            mainrow.style.display = "flex"
        }
        setTimeout(function () {
            mainleft.style.width = "0";
            mainleft.style.height = "0";
            stdcontainer.style.width = "0";
            stdcontainer.style.height = "0";
        }, delayInMilliseconds);

    } else {
        stdtable.className = stdtable.className.replace(/(?:^|\s)hide-card(?!\S)/g, '')
        stdtable.className += " showing-card"
        mainleft.style.width = "95%";
        mainleft.style.height = "auto";
        stdcontainer.style.width = "100%";
        stdcontainer.style.height = "auto";
        mainrow.style.display = "flex"
        footer.className = footer.className.replace(/(?:^|\s)hide-card(?!\S)/g, '')
    }
}
togglefac = (div) => {
    $(div).find('i').toggleClass('fas fa-eye fas fa-eye-slash');
    let faclist = document.getElementById("card-fac-list")
    let stdtable2 = document.getElementById("card-table-student")
    let sjlist2 = document.getElementById("card-sj-list")
    let faclist2 = document.getElementById("card-fac-list")
    let mainrow = document.getElementById("mian-container")
    let footer = document.getElementById("footer")
    if (faclist.className == "card showing-card") {
        faclist.className = faclist.className.replace(/(?:^|\s)showing-card(?!\S)/g, '')
        faclist.className += " hide-card"

        if (stdtable2.className == "card hide-card" && sjlist2.className == "card hide-card" && faclist2.className == "card hide-card") {
            mainrow.style.display = "none"
            footer.className += " hide-card"
        } else {
            mainrow.style.display = "flex"
        }
    } else {
        faclist.className = faclist.className.replace(/(?:^|\s)hide-card(?!\S)/g, '')
        faclist.className += " showing-card"
        mainrow.style.display = "flex"
        footer.className = footer.className.replace(/(?:^|\s)hide-card(?!\S)/g, '')

    }
}
togglesj = (div) => {
    $(div).find('i').toggleClass('fas fa-eye fas fa-eye-slash');
    let sjlist = document.getElementById("card-sj-list")
    let stdtable2 = document.getElementById("card-table-student")
    let sjlist2 = document.getElementById("card-sj-list")
    let faclist2 = document.getElementById("card-fac-list")
    let mainrow = document.getElementById("mian-container")
    let footer = document.getElementById("footer")
    if (sjlist.className == "card showing-card") {
        sjlist.className = sjlist.className.replace(/(?:^|\s)showing-card(?!\S)/g, '')
        sjlist.className += " hide-card"

        if (stdtable2.className == "card hide-card" && sjlist2.className == "card hide-card" && faclist2.className == "card hide-card") {
            mainrow.style.display = "none"
            footer.className += " hide-card"
        } else {
            mainrow.style.display = "flex"
        }
    } else {
        sjlist.className = sjlist.className.replace(/(?:^|\s)hide-card(?!\S)/g, '')
        sjlist.className += " showing-card"
        mainrow.style.display = "flex"
        footer.className = footer.className.replace(/(?:^|\s)hide-card(?!\S)/g, '')
    }
}



// font awesome
(function () {
    var css = document.createElement('link');
    css.href = 'https://use.fontawesome.com/releases/v5.12.0/css/all.css';
    css.rel = 'stylesheet';
    css.type = 'text/css';
    document.getElementsByTagName('head')[0].appendChild(css);
})();