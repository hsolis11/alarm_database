from database.connect import BaseConnection
from interface import AbstractAlarmsDB, AlarmDetails


class Alarms(BaseConnection, AbstractAlarmsDB):

    def get_detail_list(self, vendor: int = None, model: int = None, module: int = None, alarm_id: str = None):
        sql = """SELECT alarms.id,
                    alarm_id,
                    title,
                    message,
                    cause,
                    response,
                    vendors.id AS idvendor,
                    vendors.vendor,
                    eqp_models.id AS idmodel,
                    model,
                    eqp_modules.id AS idmodule,
                    module
                FROM alarms
                INNER JOIN eqp_modules
                    ON alarms.eqp_module = eqp_modules.id
                INNER JOIN eqp_models
                    ON eqp_modules.eqp_model = eqp_models.id
                INNER JOIN vendors
                    ON vendors.id = eqp_models.vendor"""
        values = []

        if vendor and not model and not module:
            sql += """ WHERE eqp_models.vendor = ? """
            values.append(vendor)

        elif vendor and model and not module:
            sql += """ WHERE eqp_models.vendor = ?
                     AND eqp_models.id = ? """
            values = values + [vendor, model]

        elif vendor and module and not model:
            sql += """ WHERE eqp_models.vendor = ?
                      AND eqp_modules.id = ? """
            values = values + [vendor, module]

        if alarm_id and not vendor and not model and not module:
            sql += " WHERE alarm_id = ?"
            values.append(alarm_id)

        elif alarm_id:
            sql += " AND alarm_id = ?"
            values.append(alarm_id)

        with self.conn as conn:
            alarms_details = []
            c = conn.cursor()
            c.execute(sql, values)
            alarms_data = c.fetchall()
            if alarms_data:
                for alarm in alarms_data:
                    alarms_details.append(AlarmDetails(*alarm))  # this needs to be sorted
        print(alarms_details)
        return alarms_details



if __name__ == '__main__':
    print(Alarms().get_detail_list(vendor=1, alarm_id='1234'))
    print(Alarms().get_detail_list(vendor=1, module=1))
