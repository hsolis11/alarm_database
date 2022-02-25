from database.connect import BaseConnection
from interface import Vendor, AbstractVendorsRepository, EqpModel, AbstractEqpModelsRepository, EqpModule, AbstractEqpModulesRepository


class Vendors(BaseConnection, AbstractVendorsRepository):

    def get_list(self):
        sql = "SELECT * FROM vendors"

        with self.conn as conn:
            vendors = []
            c = conn.cursor()
            c.execute(sql)
            data = c.fetchall()
            if data:
                for vendor in data:
                    vendors.append(Vendor(*vendor))  # this needs to be sorted
        return vendors


class EqpModels(BaseConnection, AbstractEqpModelsRepository):

    def get_list(self, vendor=None):
        if vendor:
            sql = "SELECT * FROM eqp_models WHERE vendor = ?"
            values = (vendor,)
        else:
            sql = "SELECT * FROM eqp_models"
            values = None
        with self.conn as conn:
            models = []
            c = conn.cursor()
            if values:
                c.execute(sql, values)
            else:
                c.execute(sql)
            data = c.fetchall()
            if data:
                for model in data:
                    models.append(EqpModel(model[0], model[1]))  # this needs to be sorted
        return models


class EqpModules(BaseConnection, AbstractEqpModulesRepository):

    def get_list(self, model=None):
        if model:
            sql = "SELECT * FROM eqp_modules WHERE eqp_model = ?"
            values = (model,)
        else:
            sql = "SELECT * FROM eqp_modules"
            values = None

        with self.conn as conn:
            modules = []
            c = conn.cursor()
            if values:
                c.execute(sql, values)
            else:
                c.execute(sql)
            data = c.fetchall()
            if data:
                for module in data:
                    modules.append(EqpModule(module[0], module[1]))  # this needs to be sorted
        return modules
