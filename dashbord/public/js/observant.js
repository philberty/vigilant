/**
 * Created by redbrain on 25/11/2014.
 */
require.config({
    paths: {
        jquery: [
            'https://code.jquery.com/jquery-2.1.1.min',
            '/js/lib/jquery/dist/jquery'],

        spin: [
            '/js/lib/spin.js/spin'],

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

        angularScroll: [
            '/js/lib/angular-scroll/angular-scroll'],

        angularBootstrap: [
            '//cdnjs.cloudflare.com/ajax/libs/angular-ui-bootstrap/0.10.0/ui-bootstrap-tpls.min',
            '/js/lib/angular-bootstrap/ui-bootstrap-tpls'],

        angularSpinner: [
            '/js/lib/angular-spinner/angular-spinner']
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
        'angularScroll': {
            deps: ['angular'],
            exports: 'angularScroll'
        },
        'angularSpinner': {
            deps: ['angular', 'spin'],
            exports: 'angular'
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

define('app', ["jquery", "angular", "angularBootstrap", "angularRoute", "angularScroll", "angularSpinner", "bootstrap", "bootstrapAutoHiding"],  function($, angular) {
    console.log('Hello World')

    var app = angular.module("ObservantApp", ['ngRoute', 'ui.bootstrap', 'duScroll', 'angularSpinner']);

    angular.bootstrap(document, ['ObservantApp']);
    //$("div.navbar-fixed-top").autoHidingNavbar();

    return app;
})