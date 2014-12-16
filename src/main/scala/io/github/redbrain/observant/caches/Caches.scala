package io.github.redbrain.observant.caches

import io.github.redbrain.observant.models._

object HostCache extends MapCache[HostsDataModel] {}

object LogCache extends MapCache[LogDataModel] {}

object ProcCache extends MapCache[ProcessDataModel] {}
