package io.github.redbrain.observant.servlets

import org.scalatest.FunSuiteLike
import org.scalatra.test.scalatest._

class DataStoreStateServletTest extends ScalatraSuite with FunSuiteLike {

  addServlet(classOf[DataStoreStateServlet], "/*")

  test("Getting state object for datastore") {
    get("/") {
      status should equal (200)
    }
  }

}
