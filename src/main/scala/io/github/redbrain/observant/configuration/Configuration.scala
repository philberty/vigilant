package io.github.redbrain.observant.configuration

import io.github.redbrain.observant.aggregator.TransportType
import io.github.redbrain.observant.aggregator.protocols.tcp.TCPTransport
import io.github.redbrain.observant.aggregator.protocols.udp.UDPTransport

object Configuration {

  def getCacheThreshold(): Int = 20

  def getHostsDataTimeout(): Int = 30

  def getProcDataTimeout(): Int = 30

  def getLogDataTimeout(): Int = 30

  def getTransportFromConfiguration(): TransportType = {
    //new TCPTransport(8080)
    new UDPTransport(8080)
  }

}
