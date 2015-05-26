package vigilant.datastore.services.triggers.log

import vigilant.datastore.models.{LogDataModel, Email, Sms}
import vigilant.datastore.services.triggers.Trigger

class LogRegexTrigger(sms_notification: Sms, email_notification: Email, identifier: String,
                      val key: String, val regex: String)
  extends Trigger(identifier, sms_notification, email_notification) with LogTrigger {

  private var _status = false
  override def status: Boolean = _status
  override def info: String = ""

  override def error_subject: String = ""

  override def error_message: String = ""

  override def back_to_normal_subject: String = ""

  override def back_to_normal_message: String = ""

  override def evaluate(data: LogDataModel): Boolean = {
    // TODO

    _status = false
    _status
  }

}
