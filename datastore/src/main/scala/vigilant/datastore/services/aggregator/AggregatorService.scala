package vigilant.datastore.services.aggregator

import akka.actor.{Actor, ActorRef, Props}
import org.slf4j.LoggerFactory
import play.api.libs.json._
import vigilant.datastore.caches.{HostCache, LogCache, ProcCache}
import vigilant.datastore.models.StatType

sealed trait Message
case class DataMessage(buffer: String) extends Message
case class RegisterObserver(stype: StatType.T, observer: StatsObserver) extends Message
case class DeregisterObserver(stype: StatType.T, observer: StatsObserver) extends Message

object AggregatorService {
  var actor:ActorRef = null

  def props: Props = {
    Props(classOf[AggregatorService])
  }

  def handleMessage(message: String) = {
    actor ! DataMessage(message)
  }

  def registerHostStatObsever(observer: StatsObserver) = {
    actor ! RegisterObserver(StatType.HOST, observer)
  }

  def unregisterHostStatObserver(observer: StatsObserver) = {
    actor ! DeregisterObserver(StatType.HOST, observer)
  }

  def registerLogStatObserver(observer: StatsObserver) = {
    actor ! RegisterObserver(StatType.LOG, observer)
  }

  def unregisterLogStatObserver(observer: StatsObserver) = {
    actor ! DeregisterObserver(StatType.LOG, observer)
  }

  def registerProcStatObserver(observer: StatsObserver) = {
    actor ! RegisterObserver(StatType.PROC, observer)
  }

  def unregisterProcStatObserver(observer: StatsObserver) = {
    actor ! DeregisterObserver(StatType.PROC, observer)
  }
}

class AggregatorService extends Actor with ProtocolFactory {

  private var hostsObservers = Set[StatsObserver]()
  private var procObservers = Set[StatsObserver]()
  private var logObservers = Set[StatsObserver]()

  private val logger = LoggerFactory.getLogger(getClass)

  private def handleHostMessage(json: JsValue) = {
    val model = host_data_model_from_json(json)
    HostCache.pushDataForKey(model.key, model)
    hostsObservers.foreach(_.observedHostStat(model))
  }

  private def handleLogMessage(json: JsValue) = {
    val model = log_data_model_from_json(json)
    val key = model.host + "." + model.key
    LogCache.pushDataForKey(key, model)
    logObservers.foreach(_.observedLogStat(model))
  }

  private def handlePidMessage(json: JsValue) = {
    val model = process_data_model_from_json(json)
    val key = model.host + "." + model.key
    ProcCache.pushDataForKey(key, model)
    procObservers.foreach(_.observedProcStats(model))
  }

  private def handleMessage(json: JsValue) = {
    val messageType:String = (json \ "type").as[String]
    messageType match {
      case "host" => handleHostMessage(json)
      case "log" => handleLogMessage(json)
      case "pid" => handlePidMessage(json)
      case _ => logger.error("Unhandled message of type [{}]", messageType)
    }
  }

  private def registerHostStatObsever(observer: StatsObserver) = {
    hostsObservers += observer
  }

  private def unregisterHostStatObserver(observer: StatsObserver) = {
    hostsObservers -= observer
  }

  private def registerLogStatObserver(observer: StatsObserver) = {
    logObservers += observer
  }

  private def unregisterLogStatObserver(observer: StatsObserver) = {
    logObservers -= observer
  }

  private def registerProcStatObserver(observer: StatsObserver) = {
    procObservers += observer
  }

  private def unregisterProcStatObserver(observer: StatsObserver) = {
    procObservers -= observer
  }

  def receive = {
    case DataMessage(buffer) => {
      scala.util.control.Exception.ignoring(classOf[Exception]) {
        val json = Json.parse(buffer)
        handleMessage(json)
      }
    }
    case RegisterObserver(stype, observer) => {
      stype match {
        case StatType.LOG => registerLogStatObserver(observer)
        case StatType.HOST => registerHostStatObsever(observer)
        case StatType.PROC => registerProcStatObserver(observer)
      }
    }
    case DeregisterObserver(stype, observer) => {
      stype match {
        case StatType.LOG => unregisterLogStatObserver(observer)
        case StatType.HOST => unregisterHostStatObserver(observer)
        case StatType.PROC => unregisterProcStatObserver(observer)
      }
    }
  }
}
