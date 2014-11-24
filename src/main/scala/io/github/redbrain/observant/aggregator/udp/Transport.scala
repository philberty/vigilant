package io.github.redbrain.observant.aggregator.udp

import java.util.concurrent.Executors

import io.github.redbrain.observant.aggregator.StatsAggregator
import org.jboss.netty.bootstrap.ConnectionlessBootstrap
import org.jboss.netty.channel.socket.nio.NioDatagramChannelFactory

/**
 * Created by redbrain on 24/11/2014.
 */
class Transport(val port: Int) extends Runnable with StatsAggregator {

  var _port: Int = port

  def run(): Unit = {
    val factory = new NioDatagramChannelFactory(Executors.newCachedThreadPool())
    val bootstrap = new ConnectionlessBootstrap(factory)



  }
}
