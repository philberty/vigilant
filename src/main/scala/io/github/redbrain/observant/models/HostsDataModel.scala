package io.github.redbrain.observant.models

/**
 * Created by redbrain on 24/11/2014.
 */
class HostsDataModel(val hostname:String,
                     val timestamp:String,
                     val usage:Float,
                     val process:Int,
                     val cores:Int,
                     val memoryTotal:Int,
                     val memoryUsed:Int,
                     val platform:String,
                     val machine:String,
                     val version:String,
                     val diskTotal:Int,
                     val diskFree:Int) {
}