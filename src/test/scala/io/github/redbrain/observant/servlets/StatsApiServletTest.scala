package io.github.redbrain.observant.servlets

import org.scalatest.FunSuiteLike
import org.scalatra.test.scalatest._

class StatsApiServletTest extends ScalatraSuite with FunSuiteLike {

  addServlet(classOf[StatsApiServlet], "/*")

  test("Getting list of host keys") {
    get("/host/keys") {
      status should equal (200)
    }
  }

  test("Getting list of process keys") {
    get("/proc/keys") {
      status should equal (200)
    }
  }

  test("Getting list of log session keys") {
    get("/logs/keys") {
      status should equal (200)
    }
  }
}
