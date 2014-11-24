package io.github.redbrain.observant.aggregator.udp

import java.net.InetSocketAddress
import java.util.concurrent.Executors

import io.github.redbrain.observant.aggregator.StatsAggregator
import org.jboss.netty.bootstrap.ConnectionlessBootstrap
import org.jboss.netty.channel.{Channels, ChannelPipelineFactory, ChannelPipeline}
import org.jboss.netty.channel.socket.nio.NioDatagramChannelFactory
import org.slf4j.LoggerFactory

/**
 * Created by redbrain on 24/11/2014.
 */
class Transport(val port: Int) {

  var _port: Int = port
  var _factory: NioDatagramChannelFactory = null
  var _bootstrap: ConnectionlessBootstrap = null

  val logger = LoggerFactory.getLogger(getClass)

  def close(): Unit = {
    _factory.shutdown()
    _bootstrap.shutdown()
    logger.info("UDP Stats transport shutdown on port [{}]", _port)
  }

  def start(): Unit = {
    _factory = new NioDatagramChannelFactory(Executors.newCachedThreadPool())
    _bootstrap = new ConnectionlessBootstrap(_factory)
    _bootstrap.setPipelineFactory(new ChannelPipelineFactory() {
      def getPipeline(): ChannelPipeline = {
        Channels.pipeline(StatsAggregator)
      }
    })

    _bootstrap.setOption("child.tcpNoDelay", true)
    _bootstrap.setOption("child.keepAlive", true)
    _bootstrap.bind(new InetSocketAddress(_port))

    logger.info("UDP Stats transport ready on port [{}]", _port)
  }
}
