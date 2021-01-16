odoo.define('pos_location_restriction.models', function (require) {
    "use strict";

    var models = require('point_of_sale.models');
    models.load_fields('res.partner', ['partner_latitude', 'partner_longitude']);


});
