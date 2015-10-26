var annonApp = angular.module('annonApp', ['infinite-scroll']);

// changes the default behaviour of the {{ in angular in order to not colide
// with jinja2 templates

annonApp.config(['$interpolateProvider', function($interpolateProvider) {
      $interpolateProvider.startSymbol('{a');
            $interpolateProvider.endSymbol('a}');
}]);
/*
annonApp.directive('imageonload', function() {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            element.bind('load', function() {
                alert('image is loaded');
            });
        }
    };
});
*/

annonApp.factory('AnnonLoader', function($http){
    var date = '';
    var userid = 0;
    var page = 1;
    var labelid = 1; //TODO load label id dynamically
    var busy = false;
    var after = '';

    var AnnonLoader = function(date_, userid_){
        // init params
        this.pictures = {};
        date = date_;
        userid = userid_;
        page = 1;
    }
    AnnonLoader.prototype.nextPage = function(){
        if(busy) return;
        busy = true;
        var url = '/api/get/' + userid + '/' + date + '/' + labelid + '/' + page;

        $http.get(url).success(function(data){
            if(!data) return;
            page = data['next-page'];
            items = data.pictures;
            for(var key in items){
                picture = items[key];
                //console.log(picture)
                this.pictures[key] = picture;
            }
            busy = false;

        }.bind(this))
    };

    return AnnonLoader;
});

annonApp.controller('pictures-list', function($scope, AnnonLoader) {

    var dataset = document.body.dataset;
    var date = dataset.date;
    var userid = dataset.userid;

    $scope.annonLoader = new AnnonLoader(date, userid);

/*
    $http.get('/api/get/'+userid+'/'+date).success(function(data){
        $scope.pictures = data;
    }).then(function(){
        jQuery(document.body).find('input[type="checkbox"]').shiftSelectable();
    });
*/
    // the selected checkboxes will be stored here
    $scope.selectedCheckboxes = {} 
    
    // this will retrieve the click function in each button
    $scope.showSelected = function(label){
       
        // get the checkboxes that are in true state 
        var selected = $scope.selectedCheckboxes
        var keys = []
        for(var key in $scope.selectedCheckboxes){
            if(selected[key]) keys.push(key);
        }

        if(keys.length)
        {
            console.dir(keys)
            console.dir($scope.selectedCheckboxes)
            for(var i in keys){
                var key = keys[i]
                $scope.things[key].label = label
            }
             $scope.updateServer(keys, label)
        }
    }

    // this will send a form to the server
    $scope.updateServer = function(keys, label){
        data = {keys: keys , label: label}
        $http({
            method : 'POST',
            url : '/db-set',
            data: data
        })
        $scope.uncheckAll();
    }

    $scope.uncheckAll = function(){
        $scope.selectedCheckboxes = {};
    }


});


