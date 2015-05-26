package vigilant.datastore.caches.buffer

class Cache[T](private val _size: Int)(implicit manifest : Manifest[T]) {
  var _cache = Map[String, RingBuffer[T]]()

  def keys: Set[String] = _cache.keySet

  def deleteKey(key: String) = _cache -= key

  def headForKey(key: String): Option[T] = {
    _cache.get(key) match {
      case None => None
      case Some(buffer) => Some(buffer.head)
    }
  }

  def bufferForKey(key: String): Array[T] = {
    _cache.get(key) match {
      case None => Array()
      case Some(data) => data.array
    }
  }

  def headForAllKeys: Array[T] = {
    var heads = List[T]()
    _cache.keys.foreach(k => {
      headForKey(k) match {
        case None =>
        case Some(data) => {
          heads ::= data
        }
      }
    })
    heads.toArray
  }

  def pushDataForKey(key: String, data: T) = {
    _cache.get(key) match {
      case None => {
        val ring = new RingBuffer[T](_size)
        ring.push(data)
        _cache += key -> ring
      }
      case Some(buffer) => buffer.push(data)
    }
  }
}
