// Usage: $form.find('input[type="checkbox"]').shiftSelectable();
// replace input[type="checkbox"] with the selector to match your list of checkboxes

$.fn.shiftSelectable = function() {
    var $boxes = this;

    //$.each($boxes, function(key, value){
    //    $(value).prop('checked', false);
    //})

    $boxes.click(function(evt) {
        if(!_lastChecked) {
            _lastChecked = this;
            return;
        }

        if(evt.shiftKey) {
            var start = $boxes.index(this),
                end = $boxes.index(_lastChecked);
            /*$boxes.slice(Math.min(start, end), Math.max(start, end) + 1)
                .prop('checked', lastChecked.checked)
                .trigger('change');*/
            var boxes = $boxes.slice(Math.min(start, end), Math.max(start, end) + 1);
            // para cada elemento seleccionado
            $.each(boxes, function(key, value){
                // cambiamos su estado en funcion del ultimo seleccionado
                $(value).prop('checked', _lastChecked.checked)
                // avisamos a angularjs de que hemos cambiado su estado para que actualize el scope
                angular.element(value).triggerHandler('click');
            })

        }

        _lastChecked = this;
    });


};