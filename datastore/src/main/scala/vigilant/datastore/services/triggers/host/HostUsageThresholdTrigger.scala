package vigilant.datastore.services.triggers.host

import vigilant.datastore.models.{Sms, Email, HostsDataModel}
import vigilant.datastore.services.triggers.Trigger

class HostUsageThresholdTrigger(sms_notification: Sms, email_notification: Email, identifier: String,
                                val key: String, val threshold: Float)
  extends Trigger(identifier, sms_notification, email_notification) with HostTrigger {

  private var _status = false
  override def status: Boolean = _status
  override def info: String = key + ".host.usage >= " + threshold + "%"

  override def error_subject: String =
    "VIGILANT - Host Usage Exceeded" + "[" + key + "]"

  override def error_message: String =
    "Host usage exceeded [" + key + ":" + threshold + "]"

  override def back_to_normal_subject: String = "VIGILANT - Host Usage back to normal"

  override def back_to_normal_message: String = "Host Usage back to normal"

  override def evaluate(data: HostsDataModel): Boolean = {
    if (data.usage >= threshold) {
      _status = true
    } else {
      _status = false
    }
    _status
  }

}
