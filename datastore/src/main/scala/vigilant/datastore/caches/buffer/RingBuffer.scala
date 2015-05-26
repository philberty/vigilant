package vigilant.datastore.caches.buffer

class RingBuffer[T](val size: Int)(implicit manifest : Manifest[T]) {
  private var _head = 0
  private var _tail = 0
  private var _length = 0
  private var _empty = true
  private val _buffer = new Array[T](size)

  def head: T = _buffer(_head)

  def tail: T = _buffer(_tail)

  private def isBufferFilled: Boolean = _length >= size

  /**
   * Order the data in a buffer and return it
   * @return returns ordered array oldest to fresh'est
   */
  def array: Array[T] = {
    val len = if (isBufferFilled) size else _length
    val clone = new Array[T](len)
    var offset = _tail
    for (i <- 0 until len) {
      clone(i) = _buffer(offset)
      offset = offset + 1
      if (offset >= size) {
        offset = 0
      }
    }
    clone
  }

  /**
   * Reads weird but needs to stop side-effects on indexes
   * @param data data to push to ring
   */
  def push(data: T) = {
    // if not empty move head forward
    if (!_empty) {
      _head += 1
      if (_head >= size) {
        _head = 0
      }
    }

    // to overwrite cell move tail forward
    if (isBufferFilled) {
      _tail = _tail + 1
      if (_tail >= size) {
        _tail = 0
      }
    }

    _empty = false
    _buffer(_head) = data

    _length = _length + 1
    if (_length >= Int.MaxValue) {
      _length = size
    }
  }

}
