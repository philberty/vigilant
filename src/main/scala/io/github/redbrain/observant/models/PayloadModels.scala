package io.github.redbrain.observant.models

case class HostsDataModel(key:String,
                          hostname:String,
                          timestamp:String,
                          usage:Float,
                          process:Int,
                          cores:Int,
                          memoryTotal:Long,
                          memoryUsed:Long,
                          platform:String,
                          machine:String,
                          version:String,
                          diskTotal:Long,
                          diskFree:Long,
                          cpuStats:List[Float],
                          ts:java.util.Date)

case class LogDataModel(key:String,
                        host:String,
                        message:String,
                        ts:java.util.Date)

case class ProcessDataModel(key:String,
                            host:String,
                            pid:Int,
                            path:String,
                            cwd:String,
                            cmdline:List[String],
                            status:String,
                            username:String,
                            threads:Int,
                            nfds:Int,
                            fds:List[String],
                            usage:Float,
                            memory:Float,
                            connections:List[String],
                            ts:java.util.Date)
