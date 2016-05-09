// Usage: $('#yourID').multiselect();
$.fn.multiselect = function(init_as) {

    var $check = this;
    var the_ones = document.getElementsByName($check.data('who'))
    var init_as = init_as || false;

    $check.prop('checked', init_as); // avoid errors

    $check.click(function(){
        var state = $(this).prop('checked')
        $.each(the_ones, function(key, value){$(value).prop('checked', state)})
    })

};
