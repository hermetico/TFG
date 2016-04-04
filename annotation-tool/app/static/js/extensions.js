var numCheckBoxes = 0;
var _lastChecked;

var launch_modal_box = function(){
    //TODO
}

// checkboxes are loaded with angular, so, an easy way to find out if there are new checkboxes
// is an interval
var loadingCheckBoxes = setInterval(
    function(){
        var newChecks = $(document.body).find("input[type='checkbox']");
        if(newChecks.length > numCheckBoxes){
            numCheckBoxes = newChecks.length;
            newChecks.shiftSelectable();
            // new buttons to load modal boxes
            var buttons = $(document.body).find(".button-comment");
            buttons.comment_modal_box();
        }
    },
    900
    )
