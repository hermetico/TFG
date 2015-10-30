var annonApp = angular.module('annonApp', ['infinite-scroll']);

// changes the default behaviour of the {{ in angular in order to not colide
// with jinja2 templates

annonApp.config(['$interpolateProvider', function($interpolateProvider) {
      $interpolateProvider.startSymbol('{a');
            $interpolateProvider.endSymbol('a}');
}]);


annonApp.factory('AnnonLoader', function($http){
    var date = '';
    var userid = 0;
    var page = 1;
    var labelid = 1;
    var busy = false;
    var after = '';
    var finished = false;

    var AnnonLoader = function(date_, userid_, labelid_){
        // init params
        this.pictures = {};
        date = date_;
        userid = userid_;
        page = 1;
        labelid = labelid_;
    }
    AnnonLoader.prototype.nextPage = function(){
        if(busy || finished) return;
        busy = true;
        if(labelid)
        {
            var url = '/api/get/' + userid + '/' + date + '/' + page + '/' + labelid;
        }
        else
        {
            var url = '/api/get/' + userid + '/' + date + '/' + page;
        }

        $http.get(url).success(
            function(data){
                if(!data) return;
                finished = !data['more-pages']; // no hay mas paginas que cargar
                page = data['next-page'];
                items = data.pictures;
                for(var key in items){
                    picture = items[key];
                    //console.log(picture)
                    this.pictures[key] = picture;
                    //deserializamos la fecha para poder ordenar despues
                    this.pictures[key].datetime = new Date(picture.datetime)
                }
                busy = false;

            }.bind(this))
    };

    AnnonLoader.prototype.updateServer = function(keys, label, callback){
        // this will send a form to the server
        data = {keys: keys , label: label}
        $http({
            method : 'POST',
            url : '/api/set',
            data: data
        }).success(function(){
            callback();
        })
    }

    AnnonLoader.prototype.orderedPictures = function( param )
    {
        var order = [];
        order = Object.keys(this.pictures);
        //TODO order by time
        /*
        var param = param || 'datetime';
        // esto las ordena por id : Object.keys(this.pictures);

        // las ordenamos por el parametro de entrada o por defecto
        for (var key in this.pictures)
        {
            order.push([key, this.pictures[key][param]])
        }
        order.sort(function(a, b) {return a[1] - b[1]})
        */
        return order
    }
    return AnnonLoader;
});

annonApp.filter('orderObjectBy', function() {
  return function(items, field, reverse) {
    var filtered = [];
    angular.forEach(items, function(item) {
      filtered.push(item);
    });
    filtered.sort(function (a, b) {
      return (a[field] > b[field] ? 1 : -1);
    });
    if(reverse) filtered.reverse();
    return filtered;
  };
});

annonApp.controller('pictures-list', function($scope, AnnonLoader) {

    var dataset = document.body.dataset;
    var date = dataset.date;
    var userid = dataset.userid;
    var labelid = dataset.labelid || false;

    $scope.annonLoader = new AnnonLoader(date, userid, labelid);

    // the selected checkboxes will be stored here
    $scope.selectedCheckboxes = {} 
    
    // this will retrieve the click function in each button
    $scope.showSelected = function(label){
        // get the checkboxes that are in true state
        var selected = $scope.selectedCheckboxes
        var keys = []
        // recuperamos los checkboxes seleccionados y añadimos cada key al array que enviaremos al server
        for(var key in $scope.selectedCheckboxes)
        {
            if(selected[key]) keys.push(key);
        }

        if(keys.length)
        {
            //console.dir(keys)
            //console.dir($scope.selectedCheckboxes)
            // ahora por cada key, modificamos el aspecto en el scope, asociandole el label
            for(var i in keys){
                var key = keys[i]
                $scope.annonLoader.pictures[key].label = label
            }
             $scope.annonLoader.updateServer(keys, label, $scope.uncheckAll)
        }
    }

    $scope.uncheckAll = function(){
        $scope.selectedCheckboxes = {};
    }


});


