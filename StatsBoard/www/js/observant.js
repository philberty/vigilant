/**
 * Created by redbrain on 25/11/2014.
 */
"use strict";
require.config({
    paths: {
        jquery: [
            'https://code.jquery.com/jquery-2.1.1.min',
            '/js/lib/jquery/dist/jquery.min'],

        bootstrap: [
            '//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.2.0/js/bootstrap.min',
            '/js/lib/bootstrap/dist/js/bootstrap'],

        bootstrapAutoHiding: [
            '/js/lib/bootstrap-autohidingnavbar/dist/jquery.bootstrap-autohidingnavbar'],

        angular: [
            '//cdnjs.cloudflare.com/ajax/libs/angular.js/1.2.20/angular.min',
            '/js/lib/angular/angular'],

        angularRoute: [
            '//cdnjs.cloudflare.com/ajax/libs/angular.js/1.2.20/angular-route.min',
            '/js/lib/angular-route/angular-route'],

        angularBootstrap: [
            '//cdnjs.cloudflare.com/ajax/libs/angular-ui-bootstrap/0.10.0/ui-bootstrap-tpls.min',
            '/js/lib/angular-bootstrap/ui-bootstrap-tpls']
    },
    shim: {
        'bootstrapAutoHiding': {
            deps: ['bootstrap'],
            exports: 'bootstrapAutoHiding'
        },
        'bootstrap': {
            deps: ['jquery'],
            exports: 'bootstrap'
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

define('app', ["jquery", "angular", "angularBootstrap", "angularRoute", "bootstrap", "bootstrapAutoHiding"],  function($, angular) {

    var app = angular.module("ObservantApp", ['ngRoute', 'ui.bootstrap', ]);

    app.config(
        ['$routeProvider',
            function($routeProvider) {
                $routeProvider
                    .when('/about', {
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

    app.controller('dashboard', function($scope, $http) {
        $http.get('/api/state').success(function(data) {

        });
    });

    angular.bootstrap(document, ['ObservantApp']);
    $("div.navbar-fixed-top").autoHidingNavbar();

    return app;
})