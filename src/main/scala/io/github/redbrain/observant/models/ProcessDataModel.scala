package io.github.redbrain.observant.models

/**
 * Created by redbrain on 02/12/2014.
 */
class ProcessDataModel(val host:String,
                       val pid:Int,
                       val path:String,
                       val cwd:String,
                       val cmdline:List[String],
                       val status:String,
                       val username:String,
                       val threads:Int,
                       val nfds:Int,
                       val fds:List[String],
                       val usage:Float,
                       val memory:Float,
                       val connections:List[String])
{}
