require.config({
    paths: {
        jquery: [
            //'//code.jquery.com/jquery-2.1.1.min',
            '/js/lib/jquery/dist/jquery.min'],

        vis: [
            //'//cdnjs.cloudflare.com/ajax/libs/vis/3.7.1/vis.min',
            '/js/lib/vis/dist/vis.min'
        ],

        bootstrap: [
            //'//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.2.0/js/bootstrap.min',
            '/js/lib/bootstrap/dist/js/bootstrap'],

        angular: [
            //'//cdnjs.cloudflare.com/ajax/libs/angular.js/1.2.20/angular.min',
            '/js/lib/angular/angular'],

        angularRoute: [
            //'//cdnjs.cloudflare.com/ajax/libs/angular.js/1.2.20/angular-route.min',
            '/js/lib/angular-route/angular-route'],

        angularBootstrap: [
            //'//cdnjs.cloudflare.com/ajax/libs/angular-ui-bootstrap/0.10.0/ui-bootstrap-tpls.min',
            '/js/lib/angular-bootstrap/ui-bootstrap-tpls'],

        angularLoadingBar: [
            '/js/lib/angular-loading-bar/build/loading-bar.min'
        ]
    },
    shim: {
        'bootstrap': {
            deps: ['jquery'],
            exports: 'bootstrap'
        },
        'angularLoadingBar': {
            deps: ['angular'],
            exports: 'angularLoadingBar'
        },
        'angularBootstrap': {
            deps: ['angular'],
            exports: 'angular'
        },
        'angularRoute': {
            deps: ['angular'],
            exports: 'angular'
        },
        'angular': {
            deps: ['jquery'],
            exports: 'angular'
        }
    },
    deps: ['app']
});

define('app', ["jquery", "angular", "vis", "angularBootstrap",
                "angularRoute", "angularLoadingBar", "bootstrap"],
    function($, angular, vis)
{
    var app = angular.module("ObservantApp", ['ngRoute', 'ui.bootstrap', 'angular-loading-bar']);
    app.config(
        ['$routeProvider',
            function($routeProvider) {
                $routeProvider
		            .when('/host', {
			            templateUrl: 'host.html',
			            controller: 'host'
		            })
                    .when('/dashboard', {
                        templateUrl: 'dashboard.html',
                        controller: 'dashboard'
                    })
                    .when('/', {
                        redirectTo: "/dashboard"
                    })
                    .otherwise({
                        redirectTo: '/'
                    })
            }
        ]
    );

    app.controller('dashboard', function($scope, $http, $interval) {
        var state = function() {
            $http.get('/api/state').success(function (data) {
                $scope.data = data;
                $scope.datastores = [];
                for (var key in data) $scope.datastores.push(
                    {
                        key: key,
                        name: decodeURIComponent(key)
                    }
                );
            });
        };
        state();
        var promise = $interval(state, 4000);
        $scope.$on("$destroy", function(){
            $interval.cancel(promise);
        });
    });

    app.controller('host', function($scope, $http, $interval, $route, $routeParams) {
	    var store = encodeURI($routeParams.store);
	    var host = encodeURI($routeParams.key);
        var sock = null;

        $http.get('/api/host/' + host + '?store=' + store).success(function (data) {
            console.log(data)

            if (data.alive) {
                // realtime
                if (store.substring(0, 7) == "http://") {
                    store = store.substring(7, store.length);
                }

                sock = new WebSocket("ws://" + store + "/api/host/sock/" + host);
                sock.onmessage = function (event) {
                    var data = $.parseJSON(event.data);
                    console.log(data);
                };
            } else {
                // quick display
            }
        });

        $scope.$on("$destroy", function(){
            if (sock) { sock.close (); }
        });
    });

    angular.bootstrap(document, ['ObservantApp']);
    $('[data-toggle=offcanvas]').click(function() {
        $('.row-offcanvas').toggleClass('active');
    });

    return app;
});
