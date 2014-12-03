package io.github.redbrain.observant.aggregator

import java.nio.charset.Charset

import io.github.redbrain.observant.caches.{ProcessCache, LogCache, HostCache}
import org.jboss.netty.buffer.ChannelBuffer
import org.jboss.netty.channel.{ExceptionEvent, MessageEvent, ChannelHandlerContext, SimpleChannelHandler}
import org.slf4j.LoggerFactory
import play.api.libs.json._

/**
 * Created by redbrain on 24/11/2014.
 */
object StatsAggregator extends SimpleChannelHandler with ObservantProtocolFactory {

  val logger =  LoggerFactory.getLogger(getClass)

  def handleHostMessage(json: JsValue): Unit = {
    val key:String = (json \ "key").as[String]
    HostCache.pushDataForKey(key, getHostDataModel(json))
  }

  def handleLogMessage(json: JsValue): Unit = {
    val key:String = (json \ "key").as[String]
    LogCache.pushDataForKey(key, getLogDataModel(json))
  }

  def handlePidMessage(json: JsValue): Unit = {
    val key:String = (json \ "key").as[String]
    ProcessCache.pushDataForKey(key, getProcessDataModel(json))
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
    handleMessage(Json.parse(value))
  }

  override def exceptionCaught(ctx: ChannelHandlerContext, e: ExceptionEvent) = {
    logger.error(e.getCause.getLocalizedMessage())
    e.getChannel().close()
  }
}
