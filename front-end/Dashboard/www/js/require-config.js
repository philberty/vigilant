require.config({
    paths: {
        jquery: [
            //'//code.jquery.com/jquery-2.1.1.min',
            '/js/lib/jquery/dist/jquery.min'],

        underscore: [
            '/js/lib/underscore/underscore-min'
        ],

        spin: [
            '/js/lib/spin.js/spin'
        ],

        vis: [
            //'//cdnjs.cloudflare.com/ajax/libs/vis/3.7.1/vis.min',
            '/js/lib/vis/dist/vis.min'
        ],

        bootstrap: [
            '/js/lib/bootstrap/dist/js/bootstrap.min'
        ],

        bootstrapAutoHiding: [
            '/js/lib/bootstrap-autohidingnavbar/dist/jquery.bootstrap-autohidingnavbar'
        ],

        angular: [
            //'//cdnjs.cloudflare.com/ajax/libs/angular.js/1.2.20/angular.min',
            '/js/lib/angular/angular.min'
        ],

        angularRoute: [
            //'//cdnjs.cloudflare.com/ajax/libs/angular.js/1.2.20/angular-route.min',
            '/js/lib/angular-route/angular-route.min'
        ],

        angularLoadingBar: [
            '/js/lib/angular-loading-bar/build/loading-bar.min'
        ],

        angularUiGrid: [
            '/js/lib/angular-ui-grid/ui-grid.min'
        ],

        angularBootstrap: [
            '/js/lib/angular-bootstrap/ui-bootstrap-tpls.min'
        ],

        angularSpinner: [
            '/js/lib/angular-spinner/angular-spinner'
        ]
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
        'angularSpinner': {
            deps: ['angular', 'spin'],
            exports: 'angular'
        },
        'angularUiGrid': {
            deps: ['angular'],
            exports: 'angularUiGrid'
        },
        'angularLoadingBar': {
            deps: ['angular'],
            exports: 'angularLoadingBar'
        },
        'angularRoute': {
            deps: ['angular'],
            exports: 'angular'
        },
        'angularBootstrap': {
            deps: ['angular'],
            exports: 'angular'
        },
        'angular': {
            deps: ['jquery'],
            exports: 'angular'
        }
    }
});

require(["vigilant", "jquery", "angular", "bootstrap", "bootstrapAutoHiding"],
    function(vigilant, $, angular)
{
    angular.bootstrap(document, ["vigilant"]);
    $("div.navbar-fixed-top").autoHidingNavbar();
});
