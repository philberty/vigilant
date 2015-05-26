package vigilant.datastore.services.triggers

import akka.actor._
import akka.pattern.ask
import akka.util.Timeout
import vigilant.datastore.caches.HostCache
import vigilant.datastore.models.{HostsDataModel, ProcessDataModel, LogDataModel}
import vigilant.datastore.services.aggregator.{AggregatorService, StatsObserver}
import vigilant.datastore.services.triggers.host.HostTrigger
import vigilant.datastore.services.triggers.log.LogTrigger
import vigilant.datastore.services.triggers.proc.ProcTrigger

import scala.concurrent.Await
import scala.concurrent.duration._
import scala.language.postfixOps

import org.slf4j.LoggerFactory

sealed trait Message
case class Start() extends Message
case class Stop() extends Message

case class AddHostTrigger(trigger: HostTrigger) extends Message
case class RemoveHostTrigger(identifier: String) extends Message

case class AddProcTrigger(trigger: ProcTrigger) extends Message
case class RemoveProcTrigger(identifier: String) extends Message

case class AddLogTrigger(trigger: LogTrigger) extends Message
case class RemoveLogTrigger(identifier: String) extends Message

case class ListHostTriggers() extends Message
case class ListProcTriggers() extends Message
case class ListLogTriggers() extends Message

object TriggersService extends StatsObserver {
  var actor: ActorRef = null

  implicit val timeout = Timeout(5 seconds)

  def props: Props = {
    Props(classOf[TriggersService])
  }

  def start() = {
    AggregatorService.registerLogStatObserver(this)
    AggregatorService.registerHostStatObsever(this)
    AggregatorService.registerProcStatObserver(this)
  }

  def stop() = {
    AggregatorService.unregisterLogStatObserver(this)
    AggregatorService.unregisterHostStatObserver(this)
    AggregatorService.unregisterProcStatObserver(this)
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

  def add_host_trigger(trigger: HostTrigger): Boolean = {
    val future = actor ? AddHostTrigger(trigger)
    Await.result(future, timeout.duration).asInstanceOf[Boolean]
  }

  def add_proc_trigger(trigger: ProcTrigger): Boolean = {
    val future = actor ? AddProcTrigger(trigger)
    Await.result(future, timeout.duration).asInstanceOf[Boolean]
  }

  def add_proc_trigger(trigger: LogTrigger): Boolean = {
    val future = actor ? AddLogTrigger(trigger)
    Await.result(future, timeout.duration).asInstanceOf[Boolean]
  }

  def remove_host_trigger(identifier: String): Boolean = {
    val future = actor ? RemoveHostTrigger(identifier)
    Await.result(future, timeout.duration).asInstanceOf[Boolean]
  }

  def remove_proc_trigger(identifier: String): Boolean = {
    val future = actor ? RemoveProcTrigger(identifier)
    Await.result(future, timeout.duration).asInstanceOf[Boolean]
  }

  def remove_log_trigger(identifier: String): Boolean = {
    val future = actor ? RemoveLogTrigger(identifier)
    Await.result(future, timeout.duration).asInstanceOf[Boolean]
  }

  def host_triggers_list: Set[HostTrigger] = {
    val future = actor ? ListHostTriggers
    Await.result(future, timeout.duration).asInstanceOf[Set[HostTrigger]]
  }

  def proc_triggers_list: Set[ProcTrigger] = {
    val future = actor ? ListProcTriggers
    Await.result(future, timeout.duration).asInstanceOf[Set[ProcTrigger]]
  }

  def log_triggers_list: Set[LogTrigger] = {
    val future = actor ? ListLogTriggers
    Await.result(future, timeout.duration).asInstanceOf[Set[LogTrigger]]
  }
}

class TriggersService extends Actor {

  val logger = LoggerFactory.getLogger(getClass)

  var log_triggers = Set[LogTrigger]()
  var proc_triggers = Set[ProcTrigger]()
  var host_triggers = Set[HostTrigger]()

  def handle_log_data(data: LogDataModel) = {
    log_triggers.foreach(trigger => {
      val previous_status = trigger.status
      val status = trigger.evaluate(data)
      if (status) {
        trigger.notify(trigger.error_subject, trigger.error_message)
      } else if (previous_status && !status) {
        trigger.notify(trigger.back_to_normal_subject, trigger.back_to_normal_message)
      }
    })
  }

  def handle_proc_data(data: ProcessDataModel) = {
    proc_triggers.foreach(trigger => {
      val previous_status = trigger.status
      val status = trigger.evaluate(data)
      if (status) {
        trigger.notify(trigger.error_subject, trigger.error_message)
      } else if (previous_status && !status) {
        trigger.notify(trigger.back_to_normal_subject, trigger.back_to_normal_message)
      }
    })
  }

  def handle_host_data(data: HostsDataModel) = {
    host_triggers.foreach(trigger => {
      if (trigger.key == data.key) {
        val previous_status = trigger.status
        if (trigger.evaluate(data)) {
          trigger.notify(trigger.error_subject, trigger.error_message)
        } else if (previous_status) {
          trigger.notify(trigger.back_to_normal_subject, trigger.back_to_normal_message)
        }
      }
    })
  }

  def remove_host_trigger(identifier: String): Boolean = {
    logger.info("Trying to remove host trigger [{}]", identifier)
    host_triggers.find(_.identifier == identifier) match {
      case Some(trigger) =>
        host_triggers -= trigger
        true
      case _ => false
    }
  }

  def add_host_trigger(trigger: HostTrigger): Boolean = {
    logger.info("Trying to add new host trigger [{}]", trigger.identifier)
    host_triggers.find(_.identifier == trigger.identifier) match {
      case Some(trigger) => false
      case _ => {
        // check to make sure the key exists
        HostCache.keys.find(_ == trigger.key) match {
          case Some(key) =>
            host_triggers += trigger
            true
          case _ =>
            false
        }
      }
    }
  }

  def remove_proc_trigger(identifier: String): Boolean = {
    logger.info("Trying to remove proc trigger [%s]", identifier)
    proc_triggers.find(_.identifier == identifier) match {
      case Some(trigger) =>
        proc_triggers -= trigger
        true
      case _ => false
    }
  }

  def add_proc_trigger(trigger: ProcTrigger): Boolean = {
    logger.info("Trying to add new process trigger [%s]", trigger.identifier)
    proc_triggers.find(_.identifier == trigger.identifier) match {
      case Some(trigger) => false
      case _ =>
        proc_triggers += trigger
        true
    }
  }

  def remove_log_trigger(identifier: String): Boolean = {
    logger.info("Trying to remove log trigger [%s]", identifier)
    log_triggers.find(_.identifier == identifier) match {
      case Some(trigger) =>
        log_triggers -= trigger
        true
      case _ => false
    }
  }

  def add_log_trigger(trigger: LogTrigger): Boolean = {
    logger.info("Trying to add new log trigger [%s]", trigger.identifier)
    log_triggers.find(_.identifier == trigger.identifier) match {
      case Some(trigger) => false
      case _ =>
        log_triggers += trigger
        true
    }
  }

  def receive = {
    case ListHostTriggers => sender ! host_triggers
    case ListProcTriggers => sender ! proc_triggers
    case ListLogTriggers => sender ! log_triggers

    case AddHostTrigger(trigger) => sender ! add_host_trigger(trigger)
    case RemoveHostTrigger(identifier) => sender ! remove_host_trigger(identifier)

    case AddProcTrigger(trigger) => sender ! add_proc_trigger(trigger)
    case RemoveProcTrigger(identifier) => sender ! remove_proc_trigger(identifier)

    case AddLogTrigger(trigger) => sender ! add_log_trigger(trigger)
    case RemoveLogTrigger(identifier) => sender ! remove_log_trigger(identifier)

    case data: HostsDataModel => handle_host_data(data)
    case data: ProcessDataModel => handle_proc_data(data)
    case data: LogDataModel => handle_log_data(data)

    case _ =>
  }

}
