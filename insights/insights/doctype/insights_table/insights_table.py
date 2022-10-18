# Copyright (c) 2022, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class InsightsTable(Document):
    def on_update(self):
        if not self.columns:
            self.update_columns()

    @frappe.whitelist()
    def sync_table(self):
        source = frappe.get_doc("Insights Data Source", self.data_source)
        source.sync_tables([self.table])

    @frappe.whitelist()
    def update_visiblity(self, hidden):
        self.hidden = hidden
        self.save()

    @frappe.whitelist()
    def get_preview(self):
        data_source = frappe.get_doc("Insights Data Source", self.data_source)
        return data_source.get_table_preview(self.table)

    def get_columns(self):
        if not self.columns:
            self.update_columns()
        return self.columns

    def update_columns(self):
        data_source = frappe.get_doc("Insights Data Source", self.data_source)
        if columns := data_source.get_table_columns(self):
            self.columns = []
            for column in columns:
                self.append(
                    "columns",
                    {
                        "column": column.get("column"),
                        "label": column.get("label"),
                        "type": column.get("type"),
                    },
                )