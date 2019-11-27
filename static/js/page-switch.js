function checkNewPage(){

    let response = $.ajax({ type: "GET",
        url: "http://localhost:3333/newpage",
        async: false
    }).responseText;

    if (response !== "None"){
        window.location.href = response;
        $.ajax({ type: "GET",
            url: "http://localhost:3333/reset_new_page",
            async: false
        })
    }
    setTimeout(checkNewPage, 500);
}

checkNewPage();