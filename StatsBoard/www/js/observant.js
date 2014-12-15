require.config({
    paths: {
        jquery: [
            '//code.jquery.com/jquery-2.1.1.min',
            '/js/lib/jquery/dist/jquery.min'],

        vis: [
            '//cdnjs.cloudflare.com/ajax/libs/vis/3.7.1/vis.min',
            '/js/lib/vis/dist/vis.min'
        ],

        bootstrap: [
            '//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.2.0/js/bootstrap.min',
            '/js/lib/bootstrap/dist/js/bootstrap'],

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
        'vis': {
          exports: 'vis'
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

define('app', ["jquery", "angular", "vis", "angularBootstrap", "angularRoute", "bootstrap"], function($, angular, vis) {

    var app = angular.module("ObservantApp", ['ngRoute', 'ui.bootstrap']);



    angular.bootstrap(document, ['ObservantApp']);
    $('[data-toggle=offcanvas]').click(function() {
        $('.row-offcanvas').toggleClass('active');
    });

    return app;
});