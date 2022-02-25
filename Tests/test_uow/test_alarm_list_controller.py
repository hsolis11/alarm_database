from services import alarm_list_controller
from interface import AbstractAlarmsDB, AlarmDetails


class FakeRepo(AbstractAlarmsDB):
    def get_detail_list(self, vendor=None, model=None, module=None, alarm_id=None):
        return [AlarmDetails(1, '1001', 'fake_title', 'fake_message', 'fake_cause',
                            'fake_response', 1, 'semes', 1, 'lozix', 1, 'sc')]


def test_all():
    data = {'vendor': 1, 'model': 'all', 'module': 'all', 'alarm_id': ''}
    alarms = alarm_list_controller(FakeRepo(), data)
    assert alarms == [AlarmDetails(1, '1001', 'fake_title', 'fake_message', 'fake_cause',
                            'fake_response', 1, 'semes', 1, 'lozix', 1, 'sc')]

