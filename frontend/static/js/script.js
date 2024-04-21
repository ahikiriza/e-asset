// brand click
$(".brand").click(function (){
    // alert("clicked");

    document.querySelector(".sidebar").classList.toggle("active");
    document.querySelector(".content").classList.toggle("active");


});

$(".dismiss").click(function (){
    $('.sidebar').removeClass("active");
    $('.content').removeClass("active");
})

// brand click