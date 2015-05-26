package vigilant.datastore.caches

import vigilant.datastore.caches.buffer.Cache
import vigilant.datastore.models.HostsDataModel
import vigilant.datastore.services.configuration.ConfigurationService

object HostCache extends Cache[HostsDataModel](ConfigurationService.cache_threshold) { }
