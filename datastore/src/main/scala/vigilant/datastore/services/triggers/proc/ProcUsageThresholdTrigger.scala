package vigilant.datastore.services.triggers.proc

import vigilant.datastore.models.{ProcessDataModel, Email, Sms}
import vigilant.datastore.services.triggers.Trigger


class ProcUsageThresholdTrigger(sms_notification: Sms, email_notification: Email, identifier: String,
                                val key: String, val threshold: Float)
  extends Trigger(identifier, sms_notification, email_notification) with ProcTrigger {

  private var _status = false
  override def status: Boolean = _status
  override def info: String = ""

  override def error_subject: String =
    "VIGILANT - Process Usage Exceeded" + "[" + key + "]"

  override def error_message: String =
    "Process usage exceeded [" + key + ":" + threshold + "]"

  override def back_to_normal_subject: String = "VIGILANT - Process Usage back to normal"

  override def back_to_normal_message: String = "Process Usage back to normal"

  override def evaluate(data: ProcessDataModel): Boolean = {
    if (data.key == key) {
      _status = data.usage >= threshold
      return _status
    }
    false
  }

}
