package io.github.redbrain.observant.aggregator

import java.nio.charset.Charset

import io.github.redbrain.observant.caches.{ProcCache, LogCache, HostCache}
import org.jboss.netty.buffer.ChannelBuffer
import org.jboss.netty.channel.{ExceptionEvent, MessageEvent, ChannelHandlerContext, SimpleChannelHandler}
import org.slf4j.LoggerFactory
import play.api.libs.json._

object StatsAggregator extends SimpleChannelHandler with ProtocolFactory {

  private var hostsObservers = Set[StatsObserver]()
  private var procObservers = Set[StatsObserver]()
  private var logObservers = Set[StatsObserver]()

  val logger = LoggerFactory.getLogger(getClass)

  def handleHostMessage(json: JsValue): Unit = {
    val key:String = (json \ "key").as[String]
    val model = getHostDataModel(json)
    HostCache.pushDataForKey(key, model)
    hostsObservers.foreach(_.observedHostStat(model))
  }

  def handleLogMessage(json: JsValue): Unit = {
    val key:String = (json \ "key").as[String]
    val model = getLogDataModel(json)
    LogCache.pushDataForKey(key, model)
    logObservers.foreach(_.observedLogStat(model))
  }

  def handlePidMessage(json: JsValue): Unit = {
    val key:String = (json \ "key").as[String]
    val model = getProcessDataModel(json)
    ProcCache.pushDataForKey(key, model)
    procObservers.foreach(_.observedProcStats(model))
  }

  def handleMessage(json: JsValue): Unit = {
    val messageType:String = (json \ "type").as[String]
    messageType match {
      case "host" => handleHostMessage(json)
      case "log" => handleLogMessage(json)
      case "pid" => handlePidMessage(json)
      case _ => logger.error("Unhandled message of type [{}]", messageType)
    }
  }

  override def messageReceived(context: ChannelHandlerContext, e: MessageEvent): Unit = {
    val buffer = e.getMessage().asInstanceOf[ChannelBuffer]
    val value = buffer.toString(Charset.forName("UTF-8"))
    logger.debug(value)
    handleMessage(Json.parse(value))
  }

  override def exceptionCaught(ctx: ChannelHandlerContext, e: ExceptionEvent) = {
    logger.error(e.getCause.getLocalizedMessage())
    e.getChannel().close()
  }

  def registerHostStatObsever(observer: StatsObserver): Unit = {
    hostsObservers += observer
  }

  def unregisterHostStatObserver(observer: StatsObserver): Unit = {
    hostsObservers -= observer
  }

  def registerLogStatObserver(observer: StatsObserver): Unit = {
    logObservers += observer
  }

  def unregisterLogStatObserver(observer: StatsObserver): Unit = {
    logObservers -= observer
  }

  def registerProcStatObserver(observer: StatsObserver): Unit = {
    procObservers += observer
  }

  def unregisterProcStatObserver(observer: StatsObserver): Unit = {
    procObservers -= observer
  }
}
