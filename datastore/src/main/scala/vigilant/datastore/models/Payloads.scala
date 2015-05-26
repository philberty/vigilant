package vigilant.datastore.models

case class Liveness(alive: Boolean)

case class LogDataPayload(key: String, payload: Array[LogDataModel])
case class ProcessDataPayload(key: String, payload: Array[ProcessDataModel])
case class HostDataSnap(key: String, alive: Boolean, payload: HostsDataModel)
case class HostDataPayload(key: String, payload: Array[HostsDataModel])
case class HostProcList(host: String, procs: Array[String])

case class Node(id: Int, value: Int, label: String, group: String, shape: String)
case class Edge(from: Int, to: Int, length: Int, width: Int, style: String)
case class StateDataPayload(nodes: List[Node], edges: List[Edge])

case class Keys(keys: Set[String])
case class HostState(state: Set[HostProcState])
case class HostsState(hosts: Set[HostDataSnap])

case class Response(ok: Boolean)

case class TriggerSnapshot(name: String, key: String, info: String, status: Boolean)
case class TriggerList(triggers: Set[TriggerSnapshot])

case class HostUsageTrigger(identifier: String, key: String, threshold: Float, sms: Sms, email: Email)
case class ProcUsageTrigger(identifier: String, key: String, threshold: Float, sms: Sms, email: Email)

case class HostProcState(data: ProcessDataModel, alive: Boolean)