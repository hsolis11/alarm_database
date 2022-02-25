import database as db
from interface import AbstractAlarmsDB


def alarm_list_controller(database: AbstractAlarmsDB, data: dict) -> list:
    alarms = []
    vendor = data['vendor']
    model = data['model'] if data['model'] == 'all' else int(data['model'])
    module = data['module'] if data['module'] == 'all' else int(data['module'])
    alarm_id = data['alarm_id']

    if isinstance(vendor, int) and model == 'all' and module == 'all':
        alarms = database.get_detail_list(vendor=vendor, alarm_id=alarm_id)

    elif isinstance(vendor, int) and model != 'all' and module == 'all':
        alarms = database.get_detail_list(vendor=vendor, model=model, alarm_id=alarm_id)

    elif isinstance(vendor, int) and isinstance(model, int) and isinstance(module, int):
        alarms = database.get_detail_list(vendor=vendor, module=module, alarm_id=alarm_id)

    return alarms

# class ProcessAlarmCard:
#     def __init__(self):
#         self.card: Alarm
#         self.manager = Manager()
#         self.putsql = "INSERT INTO alarms(eqp_module, alarm_id, alarm_title, alarm_message, alarm_cause, alarm_response) VALUES(%s, %s, %s, %s, %s, %s)"
#         self.values: tuple
#
#     def processForm(self, form):
#         self.card = Alarm(form.alarm_id.data, form.title.data, form.message.data, form.cause.data, form.response.data)
#         self.values = tuple(form.module.data) + self.card.getTuple()
#
#     def put_alarm_card(self):
#         if self.card:
#             self.manager.putAlarmCard(self.putsql, self.values)
#             return True


if __name__ == "__main__":
    controller = AlarmsListController(db.Alarms())
    controller.fill(vendor=1, model='all', module='all', alarm_id='')
    controller.print_all()