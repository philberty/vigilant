package io.github.redbrain.observant.caches

import io.github.redbrain.observant.models._

object HostCache extends StatsDataCache[HostsDataModel] {}

object LogCache extends StatsDataCache[LogDataModel] {}

object ProcCache extends StatsDataCache[ProcessDataModel] {}
