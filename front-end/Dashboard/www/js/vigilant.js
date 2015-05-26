'use strict';

define(['angular',
        'angularRoute',
        'angularBootstrap',
        'angularSpinner',
        'util/graphs',
        'dashboard/dashboard'
    ], function(angular, angularRoute)
{
    var app = angular.module('vigilant', [
        'ngRoute',
        'ui.bootstrap',
        'angularSpinner',
        'vigilant.dashboard',
        'vigilant.util.graphs'
    ]);

    app.config(['$routeProvider', function($routeProvider) {
        $routeProvider
            .otherwise({
                redirectTo: '/dashboard'
            });
    }]);

    return app;
});
