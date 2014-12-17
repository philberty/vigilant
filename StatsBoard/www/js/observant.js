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
    var promise = null;

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
	if (promise) {
	    $interval.cancel(promise);
	    promise = null;
	}

        var state = function () {
            $http.get('/api/state').success(function(data) {
                $scope.data = data;
                $scope.datastores = [];
                for(var key in data) $scope.datastores.push(
                    {
                        key: key,
                        name: decodeURIComponent(key)
                    }
                );
            });
        };
        state();
        promise = $interval(state, 5000);
    });

    app.controller('host', function($scope, $http, $interval, $routeParams) {
	if (promise) {
	    $interval.cancel(promise);
	    promise = null;
	}

	var store = encodeURI($routeParams.store);
	var host = encodeURI($routeParams.key);

	console.log(host);
	console.log(store);
    });

    angular.bootstrap(document, ['ObservantApp']);
    $('[data-toggle=offcanvas]').click(function() {
        $('.row-offcanvas').toggleClass('active');
    });

    return app;
});
