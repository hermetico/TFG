// Usage: $form.find('input[type="checkbox"]').shiftSelectable();
// replace input[type="checkbox"] with the selector to match your list of checkboxes

$.fn.shiftSelectable = function() {
    var lastChecked,
        $boxes = this;

    $.each($boxes, function(key, value){
        $(value).prop('checked', false);
    })

    $boxes.click(function(evt) {
        if(!lastChecked) {
            lastChecked = this;
            return;
        }

        if(evt.shiftKey) {
            var start = $boxes.index(this),
                end = $boxes.index(lastChecked);
            /*$boxes.slice(Math.min(start, end), Math.max(start, end) + 1)
                .attr('checked', lastChecked.checked)
                .trigger('change');*/
            $boxes.slice(Math.min(start, end), Math.max(start, end) + 1)
                .prop('checked', lastChecked.checked)
                .trigger('change');
        }

        lastChecked = this;
    });


};

var numCheckBoxes = 0;

// checkboxes are loaded with angular, so, an easy way to find out if there are new checkboxes
// is an interval
var loadingCheckBoxes = setInterval(
    function(){
        var newChecks = $(document.body).find("input[type='checkbox']");
        if(newChecks.length > numCheckBoxes){
            numCheckBoxes = newChecks.length;
            newChecks.shiftSelectable();
        }

    },
    500
    )