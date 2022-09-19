
    function populars(array_list, container) {
        let linkto = "";
        if (array_list[1] == "{{ session['id_user'] }}") {
            linkto = "/account";
        } else {
            linkto = "/profile/" + array_list[1];
        }

        $(container).append(`
                <section onclick="location.href='/post/`+ array_list[0] + `';">
                    <p>` + array_list[2] + `</p>
                    <div>
                        <i class="fa fa-heart"> `+ array_list[4] + `</i>
                        <i class="fa fa-message"> `+ array_list[5] + `</i>
                        <i class="fa fa-eye"> `+ array_list[6] + `</i>
                    </div>
                    <em>`+ array_list[7] + `</em>
                    <a href="`+ linkto + `">@` + array_list[3] + `</a></section>`);
    }

   
    // onclick="$(this).parent().children('section').toggle()"

    function show_popular_posts(){
        //POPULAR POSTS
        $.post("/popular_posts", { request: '1' }, function (data) {
            //MOST RECENT POSTS
            $('.newest').html(`<h1 onclick="$(this).parent().children('section').toggle();$(this).children('i').toggleClass('fa-xmark fa-plus');">Recent posts: <i class="fa fa-xmark"></i></h1>`);
            data.recent.forEach(function (arr) { populars(arr, '.newest') });
            //MOST VISITED POSTS
            $('.visited').html(`<h1 onclick="$(this).parent().children('section').toggle();$(this).children('i').toggleClass('fa-plus fa-xmark');">Most visited posts: <i class="fa fa-plus"></i></h1>`);
            data.visits.forEach(function (arr) { populars(arr, '.visited') });
            //MOST COMMENTED POSTS
            $('.commented').html(`<h1 onclick="$(this).parent().children('section').toggle();$(this).children('i').toggleClass('fa-plus fa-xmark');">Most commented posts: <i class="fa fa-plus"></i></h1>`);
            data.comments.forEach(function (arr) { populars(arr, '.commented') });
            //MOST LIKED POSTS
            $('.liked').html(`<h1 onclick="$(this).parent().children('section').toggle();$(this).children('i').toggleClass('fa-plus fa-xmark');">Most liked posts: <i class="fa fa-plus"></i></h1>`);
            data.likes.forEach(function (arr) { populars(arr, '.liked') });

            $('.visited h1, .commented h1, .liked h1').parent().children('section').toggle()
           

        });
    }

    $('.visited h1, .commented h1, .liked h1').click(function(){
    setTimeout(function(){
        console.log($('.newest h1').text())
        $(this).parent().children('section').toggle();
        $(this).children('i').toggleClass('fa-plus fa-xmark');
    },2000)
    
   })