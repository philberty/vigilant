package vigilant.datastore.caches

import org.scalatest.FunSuiteLike
import org.scalatra.test.scalatest.ScalatraSuite
import vigilant.datastore.caches.buffer.RingBuffer

class RingBufferTest extends ScalatraSuite with FunSuiteLike {

  test("That pushing data works") {
    val mockBuffer = new RingBuffer[Int](5)

    mockBuffer.push(1)

    assert(mockBuffer.head == 1)
    assert(mockBuffer.tail == 1)

    val buffer = mockBuffer.array
    assert(buffer(0) == 1)
    assert(buffer.length == 1)
  }

  test("That pushing multiple pieces of data queues correctly") {
    val mockBuffer = new RingBuffer[Int](5)

    mockBuffer.push(1)
    mockBuffer.push(2)

    val buffer = mockBuffer.array
    assert(buffer(0) == 1)
    assert(buffer(1) == 2)
    assert(buffer.length == 2)
    assert(mockBuffer.head == 2)
    assert(mockBuffer.tail == 1)
  }

  test("That pushing data greater than the size of the cache the buffer is a ring") {
    val mockBuffer = new RingBuffer[Int](5)
    mockBuffer.push(0)
    mockBuffer.push(1)
    mockBuffer.push(2)
    mockBuffer.push(3)
    mockBuffer.push(4)

    assert(mockBuffer.head == 4)
    assert(mockBuffer.tail == 0)
    var buf = mockBuffer.array
    assert(buf(0) == 0)
    assert(buf(1) == 1)
    assert(buf(2) == 2)
    assert(buf(3) == 3)
    assert(buf(4) == 4)
    assert(buf.length == 5)

    mockBuffer.push(5)

    assert(mockBuffer.head == 5)
    assert(mockBuffer.tail == 1)
    buf = mockBuffer.array
    assert(buf(0) == 1)
    assert(buf(1) == 2)
    assert(buf(2) == 3)
    assert(buf(3) == 4)
    assert(buf(4) == 5)
    assert(buf.length == 5)

    mockBuffer.push(6)

    assert(mockBuffer.head == 6)
    assert(mockBuffer.tail == 2)
    buf = mockBuffer.array
    assert(buf(0) == 2)
    assert(buf(1) == 3)
    assert(buf(2) == 4)
    assert(buf(3) == 5)
    assert(buf(4) == 6)
    assert(buf.length == 5)

    mockBuffer.push(7)
    mockBuffer.push(8)
    mockBuffer.push(9)

    assert(mockBuffer.head == 9)
    assert(mockBuffer.tail == 5)
    buf = mockBuffer.array
    assert(buf(0) == 5)
    assert(buf(1) == 6)
    assert(buf(2) == 7)
    assert(buf(3) == 8)
    assert(buf(4) == 9)
    assert(buf.length == 5)
  }

}