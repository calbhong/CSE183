// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};


// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {

    // This is the Vue data.
    app.data = {
        // Complete as you see fit.
        add_mode: false,
        add_post_text: "",
        author_name: "",
        email: "",
        rows: [],        
    };

    app.enumerate = (a) => {
        // This adds an _idx field to each element of the array.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.complete = (posts) => {
        posts.map((post)=>{
            post.rating = 0;
            post.likes = "";
            post.dislikes ="";
        })
    };

    app.add_post = function () {
        //TODO;
        axios.post(add_post_url,
            {
                post_text: app.vue.add_post_text,
                
            }).then(function (response) {
            app.vue.rows.push({
                id: response.data.id,
                post_text: app.vue.add_post_text,
                author_name: response.data.name,
                email: response.data.email
            });
            app.reset_form();
            app.set_add_status(false);
            app.enumerate(app.vue.rows);
        });
    };

    app.reset_form = function (){
        app.vue.add_post_text = "";
    }

    app.delete_post = function (row_idx,auth_id){
        //TODO;
        let id = app.vue.rows[row_idx].id;
        axios.get(delete_post_url, {params: {id:id, auth_id:auth_id}}).then(function (response) {
            for(let i = 0; i < app.vue.rows.length; i++){
                if(app.vue.rows[i].id == id){
                    app.vue.rows.splice(i,1);
                    app.enumerate(app.vue.rows);
                    break;
                }
            }
        });
    }

    app.set_add_status = function (new_status) {
        app.vue.add_post_text = "";
        app.vue.add_mode = new_status;
    };
    
    app.set_rating = function (post_idx, rating) {
        let post = app.vue.rows[post_idx];
        post.rating = rating;
        axios.post(set_rating_url, {
            "rating_post_id": post.id, 
            "rating_value": post.rating,
        })
    };

    // This contains all the methods.
    app.methods = {
        // Complete as you see fit.
        add_post: app.add_post,
        set_add_status: app.set_add_status,
        delete_post: app.delete_post,
        set_rating: app.set_rating,
    };

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    app.init = () => {
        // Put here any initialization code.
        // Typically this is a server GET call to load the data.
        axios.get(load_posts_url).then(function (response){
            let rows = response.data.rows;
            app.enumerate(rows);
            app.complete(rows);
            app.vue.rows = rows;
        }).then(()=> {
            for (let post of app.vue.rows){
                axios.get(get_rating_url, {params: {"post_id": post.id}})
                    .then((result)=>{
                        post.rating = result.data.rating;
                        post.likes = post.rating;
                        post.dislikes = post.rating;
                    });
            }
        });
    };

    // Call to the initializer.
    app.init();
};

// This takes the (empty) app object, and initializes it,
// putting all the code i
init(app);
