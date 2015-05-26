package vigilant.datastore.caches

import vigilant.datastore.caches.buffer.Cache
import vigilant.datastore.models.LogDataModel
import vigilant.datastore.services.configuration.ConfigurationService

object LogCache extends Cache[LogDataModel](ConfigurationService.cache_threshold) { }