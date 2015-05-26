package vigilant.datastore.models

case class HostsDataModel(key: String,
                          hostname: String,
                          timestamp: String,
                          usage: Float,
                          process: Int,
                          cores: Int,
                          memoryTotal: Long,
                          memoryUsed: Long,
                          platform: String,
                          machine: String,
                          version: String,
                          diskTotal: Long,
                          diskFree: Long,
                          cpuStats: Seq[Float],
                          ts: String)

case class LogDataModel(key: String,
                        host: String,
                        message: String,
                        ts: String)

case class ProcessDataModel(key: String,
                            host: String,
                            pid: Int,
                            usage: Float,
                            ts: String)
