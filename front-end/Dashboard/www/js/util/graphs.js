'use strict';

define(['angular', "vis"], function(angular, vis)
{
    var app = angular.module('vigilant.util.graphs', []);

    app.service('graphs', function() {

        this.remove_old_data = function(graph, dataset) {
            var range = graph.getWindow();
            var interval = range.end - range.start;
            var oldIds = dataset.getIds({
                filter: function (item) {
                    return item.x < range.start - interval;
                }
            });
            dataset.remove(oldIds);
        };

        this.cpu_utilization_options = function(start, end, name) {
            return {
                legend: true,
                start: start,
                end: end,
                dataAxis: {
                    customRange: {
                        left: {
                            min:0,
                            max: 100
                        }
                    },
                    title: {
                        left: {
                            text: name
                        }
                    }
                },
                zoomMax: 100000,
                zoomMin: 100000
            };
        };

        this.memory_utilization_options = function(start, end, name, max) {
            return {
                legend: true,
                start: start,
                end: end,
                dataAxis: {
                    customRange: {
                        left: {
                            min: 0,
                            max: max
                        }
                    },
                    title: {
                        left: {
                            text: name
                        }
                    }
                },
                zoomMax: 100000,
                zoomMin: 100000
            };
        };

        this.render_step = function(graph) {
            // move the window (you can think of different strategies).
            var now = vis.moment();
            var range = graph.getWindow();
            var interval = range.end - range.start;

            // continuously move the window
            graph.setWindow(now - interval, now, {animate: true});
        };

        this.node_options = {
            nodes: {
                shape: 'dot',
                radius: 30,
                borderWidth: 2
            },
            groups: {
                online: {
                    border: 'black',
                    color: 'green'
                },
                offline: {
                    border: 'black',
                    color: 'red'
                },
                root: {
                    color: {
                        border: 'black',
                        background: 'gray',
                        highlight: {
                            border: 'black',
                            background: 'lightgray'
                        }
                    },
                    fontSize: 18,
                    fontFace: 'arial',
                    shape: 'circle'
                }
            }
        };

    });

    return app;
});
