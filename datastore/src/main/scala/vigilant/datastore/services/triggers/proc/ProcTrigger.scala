package vigilant.datastore.services.triggers.proc

import vigilant.datastore.models.ProcessDataModel

trait ProcTrigger {
  def status: Boolean
  def identifier: String
  def key: String
  def info: String
  def evaluate(data: ProcessDataModel): Boolean
  def notify(subject: String, body: String)
  def error_subject: String
  def error_message: String
  def back_to_normal_subject: String
  def back_to_normal_message: String
}
