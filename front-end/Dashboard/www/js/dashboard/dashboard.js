'use strict';

define(['angular',
    'underscore',
    'vis',
    'angularRoute',
    "angularLoadingBar",
    'angularSpinner',
    "dashboard/host/host"
    ], function(angular, _, vis)
{
    var app = angular.module('vigilant.dashboard', [
        'ngRoute',
        'angular-loading-bar',
        'angularSpinner',
        'vigilant.dashboard.host']);

    app.config(['$routeProvider', function($routeProvider) {
        $routeProvider.when('/dashboard', {
            templateUrl: 'js/dashboard/dashboard.html',
            controller: 'dashboard_controller'
        });
    }]);

    app.controller('dashboard_controller', [
        '$scope',
        '$http',
        '$interval',
        '$routeParams',
        'graphs',
        'usSpinnerService',
        function($scope, $http, $interval, $routeParams, graphs)
        {
            var store = encodeURI($routeParams.store);
            $scope.store = store;

            var model = function () {
                $http.get('/api/state' + '?store=' + store).success(function (resp) {
                    var nodes = resp['nodes'];
                    var edges = resp['edges'];

                    new vis.Network(document.getElementById('cluster'), {
                            nodes: nodes,
                            edges: edges
                        },
                        graphs.node_options);
                });
            };

            var state = function () {
                $http.get('/api/hosts/state?store=' + store).success(function (data) {
                    $scope.hosts = data.hosts;
                });
            };

            state();
            model();

            var promise = $interval(state, 5000);
            $scope.$on("$destroy", function () {
                $interval.cancel(promise);
            });
        }
    ]);

    return app;
});
