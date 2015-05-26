package vigilant.datastore.services.transports.udp

import java.net.InetSocketAddress

import akka.actor.{Actor, ActorRef}
import akka.io.{IO, Udp}
import vigilant.datastore.services.aggregator.AggregatorService
import vigilant.datastore.services.transports.Transport

object UDPTransport extends Transport {
  def startMessage = Udp.Bound
  def stopMessage = Udp.Unbound
}

class UDPTransport(address: InetSocketAddress) extends Actor {
  import context.system
  IO(Udp) ! Udp.Bind(self, address)

  def receive = {
    case Udp.Bound(local) =>
      context.become(ready(sender()))
  }

  def ready(socket: ActorRef): Receive = {
    case Udp.Received(data, remote) =>
      AggregatorService.handleMessage(data.decodeString("UTF-8"))
    case Udp.Unbind  => socket ! Udp.Unbind
    case Udp.Unbound => context.stop(self)
  }

}
