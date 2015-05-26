package vigilant.datastore.services.transports

import akka.actor.ActorRef

object TransportService {

  private var _transport: Transport = null
  private var _actor: ActorRef = null

  def start() = _actor ! _transport.startMessage

  def stop() = _actor ! _transport.stopMessage

  def setTransport(actor: ActorRef, transport: Transport) = {
    _actor = actor
    _transport = transport
  }

}
