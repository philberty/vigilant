package vigilant.datastore.controllers

import org.scalatra.atmosphere.JsonMessage
import vigilant.datastore.caches.{HostCache, LogCache, ProcCache}
import vigilant.datastore.models._
import vigilant.datastore.monitors.StatsMonitor.AtmosphereStatsMonitor
import vigilant.datastore.services.triggers.TriggersService
import vigilant.datastore.services.triggers.host.HostUsageThresholdTrigger
import vigilant.datastore.services.triggers.proc.ProcUsageThresholdTrigger
import scala.concurrent.ExecutionContext.Implicits.global
import org.scalatra.swagger.{Swagger, SwaggerSupport}

class StatsController(implicit val swagger: Swagger) extends VigilantStack with SwaggerSupport {

  protected val applicationDescription = "The Real-Time Stats API."

  // --- --- --- ---

  get("/") {
    redirect("/lib/swagger-ui/dist/index.html")
  }

  get("/state", operation(
    apiOperation[StateDataPayload]("getState")
      summary "Get node graph of cluster state")) {
    var nodes = List[Node]()
    var edges = List[Edge]()

    val root = Node(0, 3, "DataStore", "root", "box")
    nodes = nodes :+ root

    var nodeIndex = 1
    HostCache.keys.foreach(k => {
      HostCache.headForKey(k) match {
        case None =>
        case Some(data) =>
          val host = Node(nodeIndex, 2, k, online_status_for_timestamp(data.ts), "box")
          nodes = nodes :+ host
          edges = edges :+ Edge(root.id, host.id, 200, 4, "line")
          nodeIndex += 1

          ProcCache.process_keys_on_host(k).foreach(p => {
            val procNode = Node(nodeIndex, 1, p, online_status_for_timestamp(data.ts), "box")
            nodes = nodes :+ procNode
            nodeIndex += 1
            edges = edges :+ Edge(host.id, procNode.id, 200, 1, "dash-line")
          })
      }
    })

    StateDataPayload(nodes, edges)
  }

  // --- --- --- ---

  get("/hosts/state", operation(
    apiOperation[HostsState]("getHostsState")
      summary "Get quick state of all hosts in data store")) {
    var state = Set[HostDataSnap]()
    HostCache.headForAllKeys.foreach(data => {
      state += HostDataSnap(data.key, is_timestamp_alive(data.ts), data)
    })
    HostsState(state)
  }

  get("/hosts/state/:key", operation(
    apiOperation[HostState]("getHostState")
      summary "Get process state of specified host in data store"
      parameters
        pathParam[String]("key").description("Host key"))) {
    val key = params("key")
    val procs = ProcCache.process_head_for_host(key)
    var state = Set[HostProcState]()
    procs.foreach(p => {
      state += HostProcState(p, is_timestamp_alive(p.ts))
    })
    HostState(state)
  }

  // --- --- --- ---

  get("/hosts/keys", operation(
    apiOperation[Keys]("getHostKeys")
      summary "Get all host keys in datastore")) {
    Keys(HostCache.keys)
  }

  get("/proc/keys", operation(
    apiOperation[Keys]("getProcKeys")
      summary "Get all process keys in datastore")) {
    Keys(ProcCache.keys)
  }

  get("/logs/keys", operation(
    apiOperation[Keys]("getLogKeys")
      summary "Get all log keys in datastore")) {
    Keys(LogCache.keys)
  }

  // --- --- --- ---

  get("/hosts/liveness/:key", operation(
    apiOperation[Liveness]("getHostLiveness")
      summary "Get liveness state of specified host"
      parameters
        pathParam[String]("key").description("Host key"))) {
    val key = params("key")
    HostCache.headForKey(key) match {
      case None => Liveness(alive = false)
      case Some(data) => Liveness(is_timestamp_alive(data.ts))
    }
  }

  get("/proc/liveness/:key", operation(
    apiOperation[Liveness]("getProcessLiveness")
      summary "Get liveness state of specified process"
      parameters
        pathParam[String]("key").description("Process key"))) {
    val key = params("key")
    ProcCache.headForKey(key) match {
      case None => Liveness(alive = false)
      case Some(data) => Liveness(is_timestamp_alive(data.ts))
    }
  }

  get("/logs/liveness/:key", operation(
    apiOperation[Liveness]("getLogLiveness")
      summary "Get liveness state of specified log"
      parameters
        pathParam[String]("key").description("Log key"))) {
    val key = params("key")
    LogCache.headForKey(key) match {
      case None => Liveness(alive = false)
      case Some(data) => Liveness(is_timestamp_alive(data.ts))
    }
  }

  // --- --- --- ---

  get("/hosts/procs/:key", operation(
    apiOperation[HostProcList]("getHostProcessKeys")
      summary "Get process keys of processes running on specified host"
      parameters
        pathParam[String]("key").description("Host key"))) {
    val key = params("key")
    HostProcList(key, ProcCache.process_keys_on_host(key).toArray)
  }

  // --- --- --- ---

  get("/hosts/rest/:key", operation(
    apiOperation[HostDataPayload]("getHostBuffer")
      summary "Get current state buffer for specified host"
      parameters
        pathParam[String]("key").description("Host key"))) {
    val key = params("key")
    HostDataPayload(key, HostCache.bufferForKey(key))
  }

  get("/hosts/head/:key", operation(
    apiOperation[HostDataSnap]("getHostHead")
      summary "Get latest host state in buffer"
      parameters
        pathParam[String]("key").description("Host key"))) {
    val key = params("key")
    HostCache.headForKey(key) match {
      case None => notFound()
      case Some(data) =>
        val alive = is_timestamp_alive(data.ts)
        HostDataSnap(key, alive, data)
    }
  }

  delete("/hosts/:key", operation(
    apiOperation[Response]("deleteHost")
      summary "Delete specified host cache"
      parameters
        pathParam[String]("key").description("Host key"))) {
    val key = params("key")
    HostCache.deleteKey(key)
    Response(ok = true)
  }

  // --- --- --- ---

  get("/proc/rest/:key", operation(
    apiOperation[ProcessDataPayload]("getProcessBuffer")
      summary "Get current state buffer for specified host"
      parameters
        pathParam[String]("key").description("Process key"))) {
    val key = params("key")
    ProcessDataPayload(key, ProcCache.bufferForKey(key))
  }

  delete("/proc/:key", operation(
    apiOperation[Response]("deleteProcess")
      summary "Delete process cache for specified key"
      parameters
        pathParam[String]("key").description("Process key"))) {
    val key = params("key")
    ProcCache.deleteKey(key)
    Response(ok = true)
  }

  // --- --- --- ---

  get("/logs/rest/:key", operation(
    apiOperation[LogDataPayload]("getLogBuffer")
      summary "Get current state buffer for specified Log"
      parameters
        pathParam[String]("key").description("Log key"))) {
    val key = params("key")
    LogDataPayload(key, LogCache.bufferForKey(key))
  }

  delete("/logs/:key", operation(
    apiOperation[Response]("deleteLog")
      summary "Delete specified log cache"
      parameters
        pathParam[String]("key").description("Log key"))) {
    val key = params("key")
    LogCache.deleteKey(key)
    Response(ok = true)
  }

  // --- --- --- ---

  get("/hosts/triggers", operation(
    apiOperation[TriggerList]("listHostTriggers")
      summary "List host triggers")) {
    val triggers = TriggersService.host_triggers_list
    var payload = Set[TriggerSnapshot]()
    triggers.foreach(trigger => {
      payload += TriggerSnapshot(trigger.identifier, trigger.key, trigger.info, trigger.status)
    })
    TriggerList(payload)
  }

  get("/hosts/triggers/:key", operation(
    apiOperation[TriggerList]("listHostTriggers")
      summary "List host triggers"
      parameters
        pathParam[String]("key").description("Host key"))) {
    val key = params("key")
    val triggers = TriggersService.host_triggers_list
    var payload = Set[TriggerSnapshot]()
    triggers.foreach(trigger => {
      if (trigger.key == key) {
        payload += TriggerSnapshot(trigger.identifier, trigger.key, trigger.info, trigger.status)
      }
    })
    TriggerList(payload)
  }

  delete("/hosts/triggers/:identifier", operation(
    apiOperation[Response]("deleteHostTrigger")
      summary "Delete specified trigger"
      parameters
      pathParam[String]("identifier").description("Trigger identifier"))) {
    val identifier = params("identifier")
    Response(ok = TriggersService.remove_host_trigger(identifier))
  }

  post("/hosts/usage_trigger", operation(
    apiOperation[Response]("addHostUsageTrigger")
      summary "Add a new host usage trigger"
      parameters
        bodyParam[HostUsageTrigger]("body").description("New host usage trigger"))) {
    val body = parsedBody.extract[HostUsageTrigger]
    val trigger = new HostUsageThresholdTrigger(
      body.sms,
      body.email,
      body.identifier,
      body.key,
      body.threshold)
    Response(ok = TriggersService.add_host_trigger(trigger))
  }

  // --- --- --- ---

  get("/proc/triggers", operation(
    apiOperation[TriggerList]("listProcTriggers")
      summary "List host triggers")) {
    val triggers = TriggersService.proc_triggers_list
    var payload = Set[TriggerSnapshot]()
    triggers.foreach(trigger => {
      payload += TriggerSnapshot(trigger.identifier, trigger.key, trigger.info, trigger.status)
    })
    TriggerList(payload)
  }

  delete("/proc/triggers/:identifier", operation(
    apiOperation[Response]("deleteProcTrigger")
      summary "Delete specified trigger"
      parameters
        pathParam[String]("identifier").description("Trigger identifier"))) {
    val identifier = params("identifier")
    Response(ok = TriggersService.remove_proc_trigger(identifier))
  }

  post("/proc/usage_trigger", operation(
    apiOperation[Response]("addProcUsageTrigger")
      summary "Add a new process usage trigger"
      parameters
      bodyParam[ProcUsageTrigger]("body").description("New process usage trigger"))) {
    val body = parsedBody.extract[ProcUsageTrigger]
    val trigger = new ProcUsageThresholdTrigger(
      body.sms,
      body.email,
      body.identifier,
      body.key,
      body.threshold)
    Response(ok = TriggersService.add_proc_trigger(trigger))
  }

  // --- --- --- ---

  atmosphere("/hosts/sock/:key") {
    new AtmosphereStatsMonitor(params("key"), StatType.HOST) {
      override def observedHostStat(data: HostsDataModel) {
        if (data.key == this.key) send(JsonMessage(encodeJson(data)))
      }
    }
  }

  atmosphere("/proc/sock/:key") {
    new AtmosphereStatsMonitor(params("key"), StatType.PROC) {
      override def observedProcStats(data: ProcessDataModel) {
        if (data.key == this.key) send(JsonMessage(encodeJson(data)))
      }
    }
  }

  atmosphere("/logs/sock/:key") {
    new AtmosphereStatsMonitor(params("key"), StatType.LOG) {
      override def observedLogStat(data: LogDataModel) {
        if (data.key == this.key) send(JsonMessage(encodeJson(data)))
      }
    }
  }

  // --- --- --- ---
}