'use strict';

define(['jquery',
    'angular',
    'underscore',
    'vis',
    "angularRoute",
    "angularUiGrid",
    "angularLoadingBar",
    "dashboard/host/proc/proc"
], function($, angular, _, vis)
{
    var app = angular.module('vigilant.dashboard.host', [
        'ngRoute',
        'ui.grid',
        'angular-loading-bar',
        'vigilant.dashboard.host.proc'
    ]);

    app.config(['$routeProvider', function($routeProvider) {
        $routeProvider.when('/host/:key', {
            templateUrl: 'js/dashboard/host/host.html',
            controller: 'host_controller'
        });
    }]);

    var store = null;
    app.controller('add_trigger_controller', function($scope, $http, $modalInstance) {

        $scope.trigger = {
            identifier: "",
            key: "",
            string_threshold: "",
            sms: {
                to: ""
            },
            email: {
                to: ""
            }
        };

        $http.get('/api/hosts/keys' + '?store=' + store).success(function(resp) {
            console.log("Retrieved list of hosts: ", resp.keys);
            $scope.hosts = resp.keys;
        });

        $scope.cancel = function () {
            $modalInstance.dismiss('cancel', null);
        };

        $scope.confirm = function() {
            var trigger = {
                identifier: $scope.trigger.identifier,
                key: $scope.trigger.key,
                threshold: parseInt($scope.trigger.string_threshold),
                sms: {
                    to: $scope.trigger.sms.to
                },
                email: {
                    to: $scope.trigger.email.to
                }
            };

            $http.post('/api/hosts/usage_trigger' + '?store=' + store, trigger).success(function (resp) {
                if (resp.ok) {
                    console.log("New trigger added: ", trigger);
                    $modalInstance.close(trigger);
                } else {
                    alert("New trigger failed: " + trigger);
                }
            }).error(function (resp) {
                console.log(resp);
            });
        }
    });

    app.controller('delete_trigger_controller', function($scope, $http, $modalInstance) {

        $scope.cancel = function () {
            $modalInstance.dismiss('cancel', null);
        };

        $scope.confirm = function() {
            $modalInstance.close();
        }
    });

    app.controller('host_controller', [
        '$scope',
        '$http',
        '$modal',
        '$interval',
        '$route',
        '$routeParams',
        'graphs',
        function($scope, $http, $modal, $interval, $route, $routeParams, graphs)
        {
            var sock = null;
            store = encodeURI($routeParams.store);
            var host = encodeURI($routeParams.key);
            $scope.host = host;
            $scope.store = store;
            $scope.state = [];

            $http.get('/api/hosts/state/' + host + '?store=' + store).success(function (resp) {
                $scope.state = resp.state;
            });

            // -- -- -- -- -- -- -- -- -- -- --

            var triggers = function() {
                $http.get('/api/hosts/triggers/' + host + '?store=' + store).success(function (resp) {
                    $scope.triggers = resp.triggers;
                });
            };
            triggers();

            // -- -- -- -- -- -- -- -- -- -- --

            $scope.add_trigger = function() {
                var modalInstance = $modal.open({
                    templateUrl: 'AddTrigger.html',
                    controller: 'add_trigger_controller',
                    resolve: {
                        trigger: function () {
                            return $scope.trigger;
                        }

                    }
                });

                modalInstance.result.then(function (trigger) {
                    triggers();
                });
            };

            // -- -- -- -- -- -- -- -- -- -- --

            $scope.delete_trigger = function(identifier) {
                console.log("Trying to delete trigger: ", identifier);
                var modalInstance = $modal.open({
                    templateUrl: 'DeleteTrigger.html',
                    controller: 'delete_trigger_controller',
                    resolve: {
                        trigger: function () {
                            return $scope.trigger;
                        }

                    }
                });

                modalInstance.result.then(function () {
                    $http.delete('/api/hosts/triggers/' + identifier + '?store=' + store).success(function (resp) {
                        if (resp.ok) {
                            console.log("Trigger deleted: ", identifier);
                        } else {
                            console.log("Trigger failed to delete: ", identifier);
                        }
                        triggers();
                    }).error(function (resp) {
                        console.log(resp);
                    });
                });
            };

            // -- -- -- -- -- -- -- -- -- -- --

            var sock_addr = null;
            // wee bit of a hack but meh it will be fine for now
            if (store.substring(0, 7) == "http://") {
                sock_addr = store.substring(7, store.length);
                sock_addr.replace(/^\s+|\s+$/g, '');
            }
            console.log("Trying ws://", sock_addr);

            // create a graph2d with an (currently empty) dataset
            var cpu_usage_graph = document.getElementById('cpu');
            var memory_usage_graph = document.getElementById('memory');
            var overall_usage_graph = document.getElementById('usage');

            var cpu_data_set = new vis.DataSet();
            var cpu_groups = new vis.DataSet();

            var usage_data_set = new vis.DataSet();
            var usage_group = new vis.DataSet();

            var memory_data_set = new vis.DataSet();
            var memory_group = new vis.DataSet();

            $http.get('/api/hosts/rest/' + host + '?store=' + store).success(function (resp) {

                var data = resp.payload;

                if (data.length > 0) {
                    var head = data[data.length - 1];
                    $scope.grid_data = [
                        {
                            "Hostname": head.hostname,
                            "Platform": head.platform,
                            "Processes": head.process,
                            "Cores": head.cores,
                            "Machine": head.machine,
                            "Disk Free": head.diskFree /1024/102,
                            "Disk Total": head.diskTotal /1024/1024/1024
                        }
                    ];
                }

                for (var i in data[0].cpuStats) {
                    cpu_groups.add({
                        id: i,
                        content: 'Core ' + (parseInt(i) + 1),
                        options: {
                            drawPoints: {
                                style: 'circle' // square, circle
                            }
                        }
                    });
                }
                memory_group.add({
                    id: 0,
                    content: "Memory Usage (mb)",
                    options: {
                        drawPoints: {
                            style: 'circle' // square, circle
                        }
                    }
                });
                usage_group.add({
                    id: 0,
                    content: "Usage Usage (%)",
                    options: {
                        drawPoints: {
                            style: 'circle' // square, circle
                        }
                    }
                });

                _.each(data, function(stat) {
                    for (var i in stat.cpuStats) {
                        cpu_data_set.add({
                            x: stat.ts,
                            y: stat.cpuStats[i],
                            group: i
                        });
                    }
                    usage_data_set.add({
                        x: stat.ts,
                        y: stat.usage,
                        group: 0
                    });
                    memory_data_set.add({
                        x: stat.ts,
                        y: stat.memoryUsed/1024/1024,
                        group: 0
                    });
                });

                var cpu_graph = new vis.Graph2d(
                    cpu_usage_graph,
                    cpu_data_set,
                    cpu_groups,
                    graphs.cpu_utilization_options(
                        data[0].ts,
                        data[data.length - 1].ts,
                        "Percentage Utilization Per Core"
                    ));

                var usage_graph = new vis.Graph2d(
                    overall_usage_graph,
                    usage_data_set,
                    usage_group,
                    graphs.cpu_utilization_options(
                        data[0].ts,
                        data[data.length - 1].ts,
                        "Percentage Overall Usage"
                    ));

                var memory_graph = new vis.Graph2d(
                    memory_usage_graph,
                    memory_data_set,
                    memory_group,
                    graphs.memory_utilization_options(
                        data[0].ts,
                        data[data.length - 1].ts,
                        "Memory Usage (mb)",
                        data[0].memoryTotal/1024/1024
                    ));

                // if it is alive we can listen to new data on the web-socket interface
                if (resp.alive) {
                    sock = new WebSocket("ws://" + sock_addr + "/api/hosts/sock/" + host);
                    sock.onmessage = function (event) {
                        var data = $.parseJSON(event.data);

                        for (var i in data.cpuStats) {
                            cpu_data_set.add({
                                x: vis.moment(),
                                y: data.cpuStats[i],
                                group: i
                            });
                            usage_data_set.add({
                                x: data.ts,
                                y: data.usage,
                                group: 0
                            });
                            memory_data_set.add({
                                x: data.ts,
                                y: data.memoryUsed/1024/1024,
                                group: 0
                            });
                        }

                        graphs.remove_old_data(cpu_graph, cpu_data_set);
                        graphs.remove_old_data(memory_graph, memory_data_set);
                        graphs.remove_old_data(usage_graph, usage_data_set);

                        graphs.render_step(cpu_graph);
                        graphs.render_step(memory_graph);
                        graphs.render_step(usage_graph);
                    }
                }
            });

            $scope.$on("$destroy", function() {
                if (sock) {
                    sock.close();
                }
            });
        }
    ]);

    return app;
});
