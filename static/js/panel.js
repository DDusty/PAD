// als je op de knop annuleren klikt dan sluit de forum
$(".cancel_form").click(function(){
    $(".form_add_user").css("display", "none");
});

// klik je op de knop update dan laat hij de form zien en geeft hij een ID value mee aan een input in de form
$(".add").click(function(){
    $(".form_add_user").css("display", "block");
    var id = $(this).parent().find(".user-id").text();
    document.getElementById('idField').value = id;
});

