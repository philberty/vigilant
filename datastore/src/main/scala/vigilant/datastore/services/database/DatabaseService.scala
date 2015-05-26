package vigilant.datastore.services.database

import akka.actor.{Actor, ActorRef, Props}
import sorm.{InitMode, Entity, Instance}
import org.slf4j.LoggerFactory
import vigilant.datastore.models.{ProcessDataModel, LogDataModel, HostsDataModel}
import vigilant.datastore.services.aggregator.{AggregatorService, StatsObserver}
import vigilant.datastore.services.configuration.ConfigurationService

sealed trait Message
case class Stop() extends Message
case class Start() extends Message

object DatabaseService extends StatsObserver {
  var actor: ActorRef = null

  def props: Props = {
    Props(classOf[DatabaseService])
  }

  def start() = {
    AggregatorService.registerLogStatObserver(this)
    AggregatorService.registerHostStatObsever(this)
    AggregatorService.registerProcStatObserver(this)
    actor ! Start()
  }

  def stop() = {
    AggregatorService.unregisterLogStatObserver(this)
    AggregatorService.unregisterHostStatObserver(this)
    AggregatorService.unregisterProcStatObserver(this)
    actor ! Stop()
  }

  override def observedHostStat(data: HostsDataModel) = {
    actor ! data
  }

  override def observedProcStats(data: ProcessDataModel) = {
    actor ! data
  }

  override def observedLogStat(data: LogDataModel) = {
    actor ! data
  }

}

class DatabaseService extends Actor {
  private val logger = LoggerFactory.getLogger(getClass)

  private val _TYPE_FIELD_NAME = "TYPE"
  private val _LOG_KEY_TABLE_NAME = "LOG_KEYS"
  private val _PROC_KEY_TABLE_NAME = "PROC_KEYS"
  private val _HOST_KEY_TABLE_NAME = "HOST_KEYS"

  case class KeySet(TYPE: String, keys: Set[String])
  private object _database extends Instance(
    entities = Set(
      Entity[KeySet](),
      Entity[HostsDataModel](),
      Entity[ProcessDataModel](),
      Entity[LogDataModel]()
    ),
    url = ConfigurationService.database_jdbc,
    initMode = InitMode.Create
  )

  private var _host_key_set = Set[String]()
  private var _log_key_set = Set[String]()
  private var _proc_key_set = Set[String]()

  def start() = {

  }

  def receive = {
    case _ =>
  }
}
