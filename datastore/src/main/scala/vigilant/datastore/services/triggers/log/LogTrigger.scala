package vigilant.datastore.services.triggers.log

import vigilant.datastore.models.LogDataModel

trait LogTrigger {
  def status: Boolean
  def identifier: String
  def key: String
  def info: String
  def evaluate(data: LogDataModel): Boolean
  def notify(subject: String, body: String)
  def error_subject: String
  def error_message: String
  def back_to_normal_subject: String
  def back_to_normal_message: String
}
