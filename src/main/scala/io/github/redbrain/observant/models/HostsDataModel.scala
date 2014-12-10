package io.github.redbrain.observant.models

/**
 * Created by redbrain on 24/11/2014.
 */
class HostsDataModel(val hostname:String,
                     val timestamp:String,
                     val usage:Float,
                     val process:Int,
                     val cores:Int,
                     val memoryTotal:Long,
                     val memoryUsed:Long,
                     val platform:String,
                     val machine:String,
                     val version:String,
                     val diskTotal:Long,
                     val diskFree:Long,
                     val cpuStats:List[Float],
                     val ts:java.util.Date)
{}
