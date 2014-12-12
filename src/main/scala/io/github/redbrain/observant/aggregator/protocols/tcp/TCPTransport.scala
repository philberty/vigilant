package io.github.redbrain.observant.aggregator.protocols.tcp

import java.net.InetSocketAddress

import io.github.redbrain.observant.aggregator.{StatsAggregator, TransportType}
import org.jboss.netty.bootstrap.ConnectionlessBootstrap
import org.jboss.netty.channel.{Channels, ChannelPipeline, ChannelPipelineFactory}
import org.jboss.netty.channel.socket.nio.NioServerSocketChannelFactory
import org.slf4j.LoggerFactory

class TCPTransport(private val port: Int) extends TransportType {

  private var factory:NioServerSocketChannelFactory = null
  private var bootstrap: ConnectionlessBootstrap = null
  private val logger = LoggerFactory.getLogger(getClass)

  /* Non-blocking function to start the transport */
  override def start(): Unit = {
    factory = new NioServerSocketChannelFactory()
    bootstrap = new ConnectionlessBootstrap(factory)
    bootstrap.setPipelineFactory(new ChannelPipelineFactory() {
      def getPipeline(): ChannelPipeline = {
        Channels.pipeline(StatsAggregator)
      }
    })

    bootstrap.bind(new InetSocketAddress(port))
    logger.info("TCP Stats transport ready on port [{}]", port)
  }

  /* Function to dealloc the transport */
  override def close(): Unit = {
    factory.shutdown()
    bootstrap.shutdown()
    logger.info("TCP Stats transport shutdown on port [{}]", port)
  }
}