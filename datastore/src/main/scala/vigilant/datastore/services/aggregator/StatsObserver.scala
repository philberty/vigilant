package vigilant.datastore.services.aggregator

import vigilant.datastore.models.{LogDataModel, ProcessDataModel, HostsDataModel}

trait StatsObserver {
  def observedHostStat(data: HostsDataModel)
  def observedProcStats(data: ProcessDataModel)
  def observedLogStat(data: LogDataModel)
}
