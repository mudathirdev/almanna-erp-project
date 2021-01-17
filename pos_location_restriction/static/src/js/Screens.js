/**
    These two functions are used for distance calculation
*/
function getDistanceInMeters(lat1, lon1, lat2, lon2) {
    var R = 6371; // Radius of the earth in km
    var dLat = deg2rad(lat2-lat1);  // deg2rad below
    var dLon = deg2rad(lon2-lon1);
    var a =
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
    Math.sin(dLon/2) * Math.sin(dLon/2)
    ;
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    var d = R * c * 1000; // Distance in meters
    return d;
}

function deg2rad(deg) {
    return deg * (Math.PI/180)
}


odoo.define('pos_location_restriction.screens', function (require) {
    "use strict";

    var core = require('web.core');
    var _t = core._t;
    var PosBaseWidget = require('point_of_sale.BaseWidget');
    var screens = require('point_of_sale.screens');
    var gui = require('point_of_sale.gui');
    var chrome = require('point_of_sale.chrome');
    var pos = require('point_of_sale.models');
    var QWeb = core.qweb;

    // When you click payment this code checks location of partner and location of POS
    screens.ActionpadWidget.include({
        detectLocation: function() {
            var self = this;
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function returnPosition(position) {
                    self.latitude = position.coords.latitude;
                    self.longitude = position.coords.longitude;
                });
            } else {
                console.log("Cannot get location information!");
            }
        },
        renderElement: function () {
            var self = this;
            this.detectLocation();
            this._super();
            this.$('.pay').unbind();
            this.$('.pay').click(function (e) {
                var client = self.pos.get_order().get_client();
                if (client) {
                    if (self.latitude && self.longitude){
                        var lat1 = client.partner_latitude;
                        var lon1 = client.partner_longitude;
                        var lat2 = self.latitude;
                        var lon2 = self.longitude;
                        var distance_in_meters = getDistanceInMeters(lat1, lon1 , lat2, lon2);
                        if (distance_in_meters > self.pos.config.max_distance_to_sell){
                            self.gui.show_popup('alert', {
                                'title': _t('Warning'),
                                'body': _t('You cannot sell because you are far from customer')
                            });
                        }else{
                            self.pos.gui.show_screen('payment');
                        }
                    }
                }
            });
        }
    });

});
