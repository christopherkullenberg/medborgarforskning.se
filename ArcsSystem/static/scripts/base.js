$(document).ready(function(){
    $(".change-language-item").click(function(){

        language_code = $(this).attr("value");
        $("#language-input-value").val(language_code);
        $("#form-languages-submit").submit();
    });

    $("#dropdownMenuButton").click(function(){
        $(this).removeClass("hide-extend-language-icon");
    });

    $(document).click(function(){
        $("#dropdownMenuButton").addClass("hide-extend-language-icon");
    });
});
