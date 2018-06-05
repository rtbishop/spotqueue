// This is the js for the default/index.html view.

var app = function() {

    var self = {};

    Vue.config.silent = false; // show all warnings

    // Extends an array
    self.extend = function(a, b) {
        for (var i = 0; i < b.length; i++) {
            a.push(b[i]);
        }
    };

    self.get_initial_data = function () {
        // The URL is initial_data_url
        console.log('test');
        $.getJSON(initial_data_url,function (data) {
                console.log(data);
            });
    };

    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
          logged_in: true,
          thing_list: [],
          animal_list: [],
        },
        methods: {
        }

    });

    $("#vue-div").show();
    self.get_initial_data();
    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
