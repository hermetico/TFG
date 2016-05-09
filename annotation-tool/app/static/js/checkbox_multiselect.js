// Usage: $('#yourID').multiselect();
$.fn.multiselect = function() {

    var $check = this;
    var the_ones = document.getElementsByName($check.data('who'))

    $check.prop('checked', false); // avoid errors

    $check.click(function(){
        var state = $(this).prop('checked')
        $.each(the_ones, function(key, value){$(value).prop('checked', state)})
    })

};
