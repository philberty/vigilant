'use strict';

define(['angular',
    "vis",
    "angularRoute",
    "angularUiGrid",
    "angularLoadingBar"
], function(angular, vis)
{
    var app = angular.module('vigilant.dashboard.host.proc',
        [
            'ngRoute',
            'angular-loading-bar'
        ]);

    app.config(['$routeProvider', function($routeProvider) {
        $routeProvider.when('/proc/:process', {
            templateUrl: 'js/dashboard/host/proc/proc.html',
            controller: 'proc_controller'
        });
    }]);

    var usageOptions = {
        start: vis.moment().add(-30, 'seconds'), // changed so its faster
        end: vis.moment(),
        dataAxis: {
            title: {
                left: {
                    text: "Usage (%)"
                }
            },
            customRange: {
                left: {
                    min:0, max: 100
                }
            }
        },
        drawPoints: {
            style: 'circle' // square, circle
        },
        shaded: {
            orientation: 'bottom' // top, bottom
        },
        zoomMax: 100000,
        zoomMin: 100000
    };

    // remove all data points which are no longer visible
    var removeOldData = function(graph, dataset) {
        var range = graph.getWindow();
        var interval = range.end - range.start;
        var oldIds = dataset.getIds({
            filter: function (item) {
                return item.x < range.start - interval;
            }
        });
        dataset.remove(oldIds);
    };


    app.controller('proc_controller', [
        '$scope',
        '$http',
        '$interval',
        '$route',
        '$routeParams',
        function($scope, $http, $interval, $route, $routeParams)
        {
            var store = encodeURI($routeParams.store);
            var host = encodeURI($routeParams.key);
            var proc = $routeParams.process;

            $scope.host = host;
            $scope.store = store;
            $scope.proc = proc;

            var sock = null;
            var sockAddr = null;
            if (store.substring(0, 7) == "http://") {
                sockAddr = store.substring(7, store.length);
            }

            $scope.procData = [];

            $http.get('/api/proc/' + proc + '?store=' + store).success(function (data) {

                // create a graph2d with an (currently empty) dataset
                var usageContainer = document.getElementById('usage');
                var memoryContainer = document.getElementById('memory');

                var usageDataSet = new vis.DataSet();
                var memoryDataSet = new vis.DataSet();

                var memoryOptions = {
                    start: vis.moment().add(-30, 'seconds'), // changed so its faster
                    end: vis.moment(),
                    dataAxis: {
                        title: {
                            left: {
                                text: "Memory Usage (%)"
                            }
                        },
                        customRange: {
                            left: {
                                min:0, max: 100
                            }
                        }
                    },
                    drawPoints: {
                        style: 'circle' // square, circle
                    },
                    shaded: {
                        orientation: 'bottom' // top, bottom
                    },
                    zoomMax: 100000,
                    zoomMin: 100000
                };

                var usageGraph = new vis.Graph2d(usageContainer, usageDataSet, usageOptions);
                var memoryGraph = new vis.Graph2d(memoryContainer, memoryDataSet, memoryOptions);

                function renderStepUsage() {
                    // move the window (you can think of different strategies).
                    var now = vis.moment();
                    var range = usageGraph.getWindow();
                    var interval = range.end - range.start;

                    // continuously move the window
                    usageGraph.setWindow(now - interval, now, {animate: false});
                    requestAnimationFrame(renderStepUsage);
                }
                function renderStepMemory() {
                    // move the window (you can think of different strategies).
                    var now = vis.moment();
                    var range = memoryGraph.getWindow();
                    var interval = range.end - range.start;

                    // continuously move the window
                    memoryGraph.setWindow(now - interval, now, {animate: false});
                    requestAnimationFrame(renderStepMemory);
                }

                if (data.alive) {
                    renderStepUsage();
                    renderStepMemory();

                    sock = new WebSocket("ws://" + sockAddr + "/api/proc/sock/" + proc);
                    sock.onmessage = function (event) {
                        var data = $.parseJSON(event.data);

                        usageDataSet.add({
                            x: data.ts,
                            y: data.usage
                        });
                        memoryDataSet.add({
                            x: data.ts,
                            y: data.memory
                        });

                        removeOldData(usageGraph, usageDataSet);
                        removeOldData(memoryGraph, memoryDataSet);
                    }
                }
            });

            $scope.$on("$destroy", function(){
                if (sock) { sock.close(); }
            });
        }
    ]);

    return app;
});
