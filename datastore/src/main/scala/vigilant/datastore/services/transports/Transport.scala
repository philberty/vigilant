package vigilant.datastore.services.transports

trait Transport {
  def startMessage: AnyRef
  def stopMessage: AnyRef
}
