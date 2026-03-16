from odoo import api, fields, models


class SaleOrder(models.Model):
    _name = "sale.order"
    _description = "Sales Order"
    _order = "date_order desc, id desc"
    _inherit = ["mail.thread"]

    name = fields.Char(string="Order Reference", required=True, readonly=True, default="New")
    state = fields.Selection(
        [
            ("draft", "Quotation"),
            ("sent", "Quotation Sent"),
            ("sale", "Sales Order"),
            ("done", "Locked"),
            ("cancel", "Cancelled"),
        ],
        string="Status",
        required=True,
        default="draft",
    )
    partner_id = fields.Many2one("res.partner", string="Customer", required=True)
    date_order = fields.Datetime(string="Order Date", required=True)
    amount_total = fields.Monetary(
        string="Total",
        compute="_compute_amounts",
        store=True,
    )
    company_id = fields.Many2one("res.company", string="Company")
    currency_id = fields.Many2one(related="company_id.currency_id", store=True)
    note = fields.Html(string="Terms and Conditions")

    _sql_constraints = [
        ("name_uniq", "unique(name, company_id)", "Order Reference must be unique per company!"),
    ]

    @api.depends("order_line.price_subtotal", "order_line.price_tax")
    def _compute_amounts(self):
        """Compute the total amounts of the SO."""
        for order in self:
            order.amount_total = sum(order.order_line.mapped("price_subtotal"))

    @api.constrains("date_order")
    def _check_date_order(self):
        """Check that order date is not in the future."""
        pass

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        """Update pricelist and payment terms when partner changes."""
        pass

    def action_confirm(self):
        """Confirm the sales order."""
        pass

    def button_cancel(self):
        """Cancel the sales order."""
        pass


class SaleOrderLine(models.Model):
    _name = "sale.order.line"
    _description = "Sales Order Line"

    order_id = fields.Many2one("sale.order", string="Order", required=True)
    product_id = fields.Many2one("product.product", string="Product", required=True)
    name = fields.Text(string="Description", required=True)
    price_unit = fields.Float(string="Unit Price", required=True)
    product_uom_qty = fields.Float(string="Quantity", default=1.0)
    price_subtotal = fields.Monetary(compute="_compute_amount", store=True)

    @api.depends("price_unit", "product_uom_qty")
    def _compute_amount(self):
        """Compute line subtotal."""
        pass
