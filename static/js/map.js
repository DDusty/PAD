var paal = document.getElementsByClassName("paal");
var moving = false;
var delete_button = document.getElementsByClassName("delete_stop");

$("#cancel_form").click(function(){
    $("#form_add_stop").css("display", "none");
});

$("#add_stop").click(function(){
    $("#form_add_stop").css("display", "block");
});

// geeft een eventlistener mee
for(var i=0; i < 10; i++){
    paal[i].addEventListener("mousedown", initialClick, false);
    delete_button[i].addEventListener("mousedown", initialClick, false);
}

// als er 1x is geklikt dan wordt deze functie uitgevoerd en geeft hij een nieuwe
// x en y as mee die hij vervolgens aan de style meegeeft van het paaltje dat wordt geklikt.
function move(e){

  var newX = e.clientX - 10;
  var newY = e.clientY - 10;

  image.style.left = newX + "px";
  image.style.top = newY + "px";

//  console.log(newX)
//  console.log(newY)
}

// als je klikt dan voert hij deze functie uit die de save_stop functie uitvoert als de
// paaltje voor de 2e x wordt geklikt. wordt verwijdere geklikt wordt delete_stop uitgevoerd
function initialClick(e) {
    $(delete_button).click(function(){
          delete_stop(e, $(this));
          console.log('clicked');
     });

  if(moving){
    document.removeEventListener("mousemove", move);
    moving = !moving;
    save_stop(e, $(this));
    return;
  }

  moving = !moving;
  image = this;

  document.addEventListener("mousemove", move, false);

}
// functie die de paaltje cordi's update
function save_stop(e, paalElement){
    var Y = e.clientY - 10;
    var X = e.clientX - 10;
    // geef de stop id en cordinaten mee met een ajax call aan de webserver pi
    $.ajax(
    {
        type:'POST',
        contentType:'application/json;charset-utf-08',
        dataType:'json',
        url: 'http://localhost:3333/loc_val?x='+X+"&y="+Y+"&stop_id="+ paalElement.data("stopid") ,
        success:function (data) {
            var reply=data.reply;
            if (reply=="success")
                {
                    console.log("succes")
                    return;
                }
                else
                {
                    alert("some error ocured in session agent")
                }

            }
        }
    );
}

// geef een id mee zodat je de id heb die je wilt verwijderen
function delete_stop(e, stopElement){
$.ajax(
    {
        type:'POST',
        contentType:'application/json;charset-utf-08',
        dataType:'json',
        url: 'http://localhost:3333/delete_stop?id=' + stopElement.data("id") ,
        success:function (data) {
            var reply=data.reply;
            if (reply=="success")
                {
                    alert("stop deleted");
                    return;
                }
                else
                {
                    alert("some error ocured in session agent")
                }

            }
        }
    );

}