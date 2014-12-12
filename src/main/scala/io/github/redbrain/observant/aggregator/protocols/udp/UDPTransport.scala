package io.github.redbrain.observant.aggregator.protocols.udp

import java.net.InetSocketAddress
import java.util.concurrent.Executors

import io.github.redbrain.observant.aggregator.{StatsAggregator, TransportType}
import org.jboss.netty.bootstrap.ConnectionlessBootstrap
import org.jboss.netty.channel.socket.nio.NioDatagramChannelFactory
import org.jboss.netty.channel.{ChannelPipeline, ChannelPipelineFactory, Channels}
import org.slf4j.LoggerFactory

/**
 * Created by redbrain on 24/11/2014.
 */
class UDPTransport(private val port: Int) extends TransportType {

  private var factory: NioDatagramChannelFactory = null
  private var bootstrap: ConnectionlessBootstrap = null
  private val logger = LoggerFactory.getLogger(getClass)

  override def close(): Unit = {
    factory.shutdown()
    bootstrap.shutdown()
    logger.info("UDP Stats transport shutdown on port [{}]", port)
  }

  override def start(): Unit = {
    factory = new NioDatagramChannelFactory(Executors.newCachedThreadPool())
    bootstrap = new ConnectionlessBootstrap(factory)
    bootstrap.setPipelineFactory(new ChannelPipelineFactory() {
      def getPipeline(): ChannelPipeline = {
        Channels.pipeline(StatsAggregator)
      }
    })

    bootstrap.bind(new InetSocketAddress(port))
    logger.info("UDP Stats transport ready on port [{}]", port)
  }
}
