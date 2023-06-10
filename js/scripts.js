$("form[name=signup_form").submit(function(e){

    var $form = $(this);
    var $error = $form.find(".error")
    var data = $form.serialize();

    $ajax({
        url: "usr/login",
        type: "POST",
        data: data,
        dataType: "json",
        sucess: function(resp){
            console.log(resp)
            window.location.href = "/usr/dashboard";
        },
        error: function(resp){
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    })


    e.preventDefault();
});