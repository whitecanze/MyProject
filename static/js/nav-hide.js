let getname = "nav"

$(getname).hide();

$("body").mousemove(function (event) {
    $(getname).fadeIn('slow')
    $('body').css({
        cursor: 'default'
    });
    myStopFunction()
    myFunction()
});

function myFunction() {
    myVar = setTimeout(function () {
        $(getname).fadeOut('slow')
        $('body').css({
            cursor: 'none'
        });
    }, 2000);
}

function myStopFunction() {
    if (typeof myVar != 'undefined') {
        clearTimeout(myVar)
    }
}