package io.github.redbrain.observant.backends

import io.github.redbrain.observant.aggregator.StatsObserver
import io.github.redbrain.observant.models.{HostsDataModel, ProcessDataModel, LogDataModel}

class AsyncBackendDispatchQueue extends StatsObserver {



  override def observedHostStat(data: HostsDataModel): Unit = {

  }

  override def observedProcStats(data: ProcessDataModel): Unit = {

  }

  override def observedLogStat(data: LogDataModel): Unit = {

  }
}
