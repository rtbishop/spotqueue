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
        $.getJSON(initial_data_url,function (data) {
                self.vue.current_user = data.current_user;
                self.vue.logged_in = data.logged_in;
                console.log(data.logged_in);
                console.log(self.vue.logged_in);
            })
    };

//    self.get_songs = function(){
//      $.getJSON(get_songs_url,function (data) {
//              console.log(data);
//          });
//    };

    self.search_songs = function(query) {
        console.log(query);
        $.getJSON(search_songs_url,
            { query: query },
            function (data) {
                self.vue.search_results = data.songs;
            }
         );
    };

    self.add_to_queue = function(song_uri) {
        console.log("clicked: "+song_uri);
        $.getJSON(add_to_queue_url,
            { song_uri: song_uri },
            function (data) {
                console.log("add to queue: "+data);
            }
        );
        setTimeout(function(){
            location.reload(1);
        }, 800);
    };

    self.get_playlists = function() {
        $.getJSON(get_playlists_url,
            function (data) {
                self.vue.user_playlists = data.user_playlists;
            }
         );
    };

    self.get_tracks_from_playlist = function(playlist_id) {
        $.getJSON(get_tracks_url,
            { playlist_id: playlist_id },
            function (data) {
                console.log(data.tracks_in_playlist);
                self.vue.tracks_in_playlist = data.tracks_in_playlist;
            }
         );
    };

    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            current_user: null,
            logged_in: true,
            //queue: [],
            search: '',
            search_results: [],
            user_playlists: [],
            tracks_in_playlist: [],
        },
        methods: {
            search_songs: self.search_songs,
            add_to_queue: self.add_to_queue,
            get_playlists: self.get_playlists,
            get_tracks_from_playlist: self.get_tracks_from_playlist,
        }

    });

    //self.get_songs();
    self.get_initial_data();
    self.get_playlists();
    $("#vue-div").show();
    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
