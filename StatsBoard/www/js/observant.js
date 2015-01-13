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
        ],

        angularUiGrid: [
            '/js/lib/angular-ui-grid/ui-grid.min'
        ]
    },
    shim: {
        'bootstrap': {
            deps: ['jquery'],
            exports: 'bootstrap'
        },
        'angularUiGrid': {
            deps: ['angular'],
            exports: 'angularUiGrid'
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

define('app', ["jquery", "angular", "vis", "angularBootstrap", "angularRoute", "angularLoadingBar", "angularUiGrid", "bootstrap"],
    function($, angular, vis)
{
    var app = angular.module("ObservantApp", ['ngRoute', 'ui.bootstrap', 'ui.grid', 'angular-loading-bar']);
    app.config(
        ['$routeProvider',
            function($routeProvider) {
                $routeProvider
		            .when('/host', {
			            templateUrl: 'host.html',
			            controller: 'host'
		            })
                    .when('/proc/:process', {
                        templateUrl: 'proc.html',
                        controller: 'proc'
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

    var usageOptions = {
        start: vis.moment().add(-30, 'seconds'), // changed so its faster
        end: vis.moment(),
        dataAxis: {
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
        dataAxis: {
            title: {
                left: {
                    text: "Usage (%)"
                }
            }
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

    app.controller('dashboard', function($scope, $http, $interval, $routeParams) {
        var store = encodeURI($routeParams.store);
        if (store == 'undefined') {
            $scope.valid = false;
        } else {
            $scope.valid = true;
            var state = function () {
                $http.get('/api/state?store=' + store).success(function (data) {
                    $scope.valid = true;
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
            $scope.$on("$destroy", function () {
                $interval.cancel(promise);
            });
        }
    });

    app.controller('proc', function($scope, $http, $interval, $route, $routeParams) {
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
                dataAxis: {
                    title: {
                        left: {
                            text: "Memory Usage (%)"
                        }
                    }
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
    });

    app.controller('host', function($scope, $http, $interval, $route, $routeParams) {
	    var store = encodeURI($routeParams.store);
	    var host = encodeURI($routeParams.key);
        $scope.host = host;
        $scope.store = store;

        var sock = null;
        var sockAddr = null;
        if (store.substring(0, 7) == "http://") {
            sockAddr = store.substring(7, store.length);
        }

        $scope.host = host;
        $scope.store = store;
        $scope.isWatchingProc = false;
        $scope.watchProc = function(proc) {};

        $http.get('/api/host/' + host + '?store=' + store).success(function (data) {

            $scope.platform = data.payload.platform;
            $scope.hostname = data.payload.hostname;
            $scope.version = data.payload.version;
            $scope.machine = data.payload.machine;
            $scope.pids = data.payload.process;
            $scope.cores = data.payload.cores;
            $scope.usage = Math.round(data.payload.usage);
            $scope.memory = Math.round(data.payload.memoryUsed/1024/1024);

            // create a graph2d with an (currently empty) dataset
            var usageContainer = document.getElementById('usage');
            var memoryContainer = document.getElementById('memory');
            var cpuContainer = document.getElementById('cpu');

            var usageDataSet = new vis.DataSet();
            var memoryDataSet = new vis.DataSet();
            var cpuDataSet = new vis.DataSet();
            var cpuGroups = new vis.DataSet();

            for (var i in data.payload.cpuStats) {
                cpuGroups.add({
                    id: i,
                    content: 'Core ' + (parseInt(i) + 1),
                    options: {
                        drawPoints: {
                            style: 'circle' // square, circle
                        }
                    }
                });
            }

            var memoryOptions = {
                start: vis.moment().add(-30, 'seconds'), // changed so its faster
                end: vis.moment(),
                dataAxis: {
                    customRange: {
                        left: {
                            min:0, max: data.payload.memoryTotal/1024/1024
                        }
                    }
                },
                drawPoints: {
                    style: 'circle' // square, circle
                },
                shaded: {
                    orientation: 'bottom' // top, bottom
                },
                dataAxis: {
                    title: {
                        left: {
                            text: "Memory Usage (mb)"
                        }
                    }
                },
                zoomMax: 100000,
                zoomMin: 100000
            };

            var cpuOptions = {
                legend: true,
                start: vis.moment().add(-30, 'seconds'), // changed so its faster
                end: vis.moment(),
                dataAxis: {
                    customRange: {
                        left: {
                            min:0, max: 100
                        }
                    },
                    title: {
                        left: {
                            text: "Percentage Usage"
                        }
                    }
                },
                zoomMax: 100000,
                zoomMin: 100000
            };

            var usageGraph = new vis.Graph2d(usageContainer, usageDataSet, usageOptions);
            var memoryGraph = new vis.Graph2d(memoryContainer, memoryDataSet, memoryOptions);
            var cpuGraph = new vis.Graph2d(cpuContainer, cpuDataSet, cpuGroups, cpuOptions);

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
            function renderStepCpu() {
                // move the window (you can think of different strategies).
                var now = vis.moment();
                var range = cpuGraph.getWindow();
                var interval = range.end - range.start;

                // continuously move the window
                cpuGraph.setWindow(now - interval, now, {animate: false});
                requestAnimationFrame(renderStepCpu);
            }

            if (data.alive) {
                renderStepUsage();
                renderStepMemory();
                renderStepCpu();

                sock = new WebSocket("ws://" + sockAddr + "/api/host/sock/" + host);
                sock.onmessage = function (event) {
                    var data = $.parseJSON(event.data);

                    $scope.pids = data.process;
                    $scope.usage = Math.round(data.usage);
                    $scope.memory = Math.round(data.memoryUsed/1024/1024);

                    usageDataSet.add({
                        x: data.ts,
                        y: data.usage
                    });
                    memoryDataSet.add({
                        x: data.ts,
                        y: data.memoryUsed/1024/1024
                    });
                    for (var cpu in data.cpuStats) {
                        cpuDataSet.add({
                            x: data.ts,
                            y: data.cpuStats[cpu],
                            group: cpu
                        });
                    };

                    removeOldData(cpuGraph, cpuDataSet);
                    removeOldData(memoryGraph, memoryDataSet);
                    removeOldData(usageGraph, usageDataSet);
                };
            }
        });

        $http.get('/api/host/procs/' + host + '?store=' + store).success(function (data) {
            $scope.procs = data.payload;
        });

        $scope.$on("$destroy", function(){
            if (sock) { sock.close(); }
        });
    });

    angular.bootstrap(document, ['ObservantApp']);
    $('[data-toggle=offcanvas]').click(function() {
        $('.row-offcanvas').toggleClass('active');
    });

    return app;
});
