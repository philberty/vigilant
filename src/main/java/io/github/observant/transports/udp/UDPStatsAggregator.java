package io.github.observant.transports.udp;

import io.github.observant.transports.StatsAggregator;

/**
 * Created by redbrain on 19/11/2014.
 */
public class UDPStatsAggregator extends StatsAggregator {
    private String _host;
    private int _port;

    public UDPStatsAggregator(String host, int port) {
        this._host = host;
        this._port = port;
    }


    @Override
    public void run() {

    }
}
