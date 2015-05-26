import org.scalatra.sbt._
import sbt.Keys._
import sbt._

object VigilantBuild extends Build {
  val Organization = "io.github.redbrain"
  val Name = "vigilant"
  val Version = "0.2.0-SNAPSHOT"
  val ScalaVersion = "2.11.6"
  val ScalatraVersion = "2.3.0"

  lazy val project = Project (
    "vigilant",
    file("."),
    settings = ScalatraPlugin.scalatraSettings ++ Seq(
      organization := Organization,
      name := Name,
      version := Version,
      scalaVersion := ScalaVersion,

      resolvers += "Sonatype OSS Snapshots" at "http://oss.sonatype.org/content/repositories/snapshots/",
      resolvers += "Akka Repo" at "http://repo.akka.io/repository",
      resolvers += "Typesafe repository" at "http://repo.typesafe.com/typesafe/releases/",

      conflictWarning ~= { _.copy(failOnConflict = false) },

      libraryDependencies ++= Seq(
        // Scalatra
        "org.scalatra" %% "scalatra" % ScalatraVersion,
        "org.scalatra" %% "scalatra-atmosphere" % ScalatraVersion,
        "org.scalatra" %% "scalatra-json" % ScalatraVersion,
        "org.scalatra" %% "scalatra-auth" % ScalatraVersion,
        "org.scalatra" %% "scalatra-swagger"  % ScalatraVersion,
        "org.scalatra" %% "scalatra-specs2" % ScalatraVersion % "test",
        "org.scalatra" %% "scalatra-scalatest" % ScalatraVersion % "test",

	      // Json
        "org.json4s" %% "json4s-jackson" % "3.2.9",
        "org.json4s" %% "json4s-native" % "3.2.9",
        "com.typesafe.play" %% "play-json" % "2.3.0",

	      // database
        "org.sorm-framework" % "sorm" % "0.3.18",
        "com.h2database" % "h2" % "1.4.187",

	      // notifications
        "com.twilio.sdk" % "twilio-java-sdk" % "4.0.1",
        "javax.mail" % "mail" % "1.4.1",
        "javax.activation" % "activation" % "1.1.1",

	      // Akka
        "ch.qos.logback" % "logback-classic" % "1.0.13",
        "com.typesafe.akka" %% "akka-actor" % "2.3.4",
        "net.databinder.dispatch" %% "dispatch-core" % "0.11.1",

	      // Jetty
        "org.eclipse.jetty" % "jetty-webapp" % "8.1.8.v20121106" % "container",
        "org.eclipse.jetty" % "jetty-websocket" % "8.1.8.v20121106" % "container;provided",
        "org.eclipse.jetty.orbit" % "javax.servlet" % "3.0.0.v201112011016" % "container;provided;test"
      )
    )
  )
}
