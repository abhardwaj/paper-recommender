// try to first load the data from localStorage 
/*
var id = localStorage.getItem('login_id')
var en = localStorage.getItem('entities')
var se = localStorage.getItem('sessions')
var re = localStorage.getItem('recommended')
var st = localStorage.getItem('starred')
var co = localStorage.getItem('codes')
*/
// contact the server if required
//if(id == null || en == null || se == null || re == null || st == null || co == null){
    console.log('contacting server')
    $.ajax({
        type: 'GET',
        async: false,
        url: '/data', 
        success: function(res) {
        id = JSON.stringify(res.login_id)
        en = JSON.stringify(res.entities)
        se = JSON.stringify(res.sessions)
        re = JSON.stringify(res.recs)
        st  = JSON.stringify(res.starred)
        op  = JSON.stringify(res.own_papers)
        co  = res.codes
        localStorage.clear()
        localStorage.setItem('login_id', id)
        localStorage.setItem('entities', en)
        localStorage.setItem('sessions', se)
        localStorage.setItem('recommended', re)
        localStorage.setItem('starred', st)
        localStorage.setItem('codes', co)
        localStorage.setItem('own_papers', op)

        }
    });

//}



var login_id = JSON.parse(id)
var entities = JSON.parse(en)
var sessions = JSON.parse(se)
var recommended_all = JSON.parse(re)
var starred = JSON.parse(st)
var codes = JSON.parse(co)
var own_papers = JSON.parse(op)
var recommended = recommended_all.splice(0,20)

// codes without video preview
var codeBlackList = [
  "KOP","PHN","NDL","LDJ","PQS","PLP","PLL","CYU","LRA","PQV","NNG","PMF","PSS","PSR","NEK","PKY",
  "PKS","PFS","PLJ","TRN","PBR","YQT","PJC","PKZ","PDS","PFR","SRJ","PHF","TUU","TZC","AZG","CZS",
  "PQE","GYU","GDG","NMX","PAK","YHY","PQQ","LLC","NPP","TXL","CZS","TLQ","GFL","TAU","NKQ","PTS",
  "PKL","GXS","SIA","PTU","PAE","PRH","PGG","LBR","PQZ","PTN","PRT","NGR","PEH","PGV","TGN","PSJ",
  "PDT","PMY","NGN","PQC","PPM","PCB","SRC","PDM","PSP","GZX","PKJ","PBM","PHR","SDC","CMU","LPA",
  "PRN","GHQ","TEC","PMR","PCD","NJT","AXZ","PEB","LSU","PMM","PMV","SGC","CMU","NHL","KSP","PKV",
  "YYP","NFM","PTT","NCK","PQG","KCL"
];

function detect_mobile() { 
 if(navigator.userAgent.match(/Android/i)
 || navigator.userAgent.match(/webOS/i)
 || navigator.userAgent.match(/iPhone/i)
 || navigator.userAgent.match(/iPad/i)
 || navigator.userAgent.match(/iPod/i)
 || navigator.userAgent.match(/BlackBerry/i)
 || navigator.userAgent.match(/Windows Phone/i)
 ){
    return true;
  } else {
    return false;
  }
}



jQuery.fn.highlight = function(pat) {
 function innerHighlight(node, pat) {
  var skip = 0;
  if (node.nodeType == 3) {
   var pos = node.data.toUpperCase().indexOf(pat);
   if (pos >= 0) {
    var spannode = document.createElement('span');
    spannode.className = 'text-highlight';
    var middlebit = node.splitText(pos);
    var endbit = middlebit.splitText(pat.length);
    var middleclone = middlebit.cloneNode(true);
    spannode.appendChild(middleclone);
    middlebit.parentNode.replaceChild(spannode, middlebit);
    skip = 1;
   }
  }
  else if (node.nodeType == 1 && node.childNodes && !/(script|style)/i.test(node.tagName)) {
   for (var i = 0; i < node.childNodes.length; ++i) {
    i += innerHighlight(node.childNodes[i], pat);
   }
  }
  return skip;
 }
 return this.each(function() {
  innerHighlight(this, pat.toUpperCase());
 });
};

jQuery.fn.removeHighlight = function() {
 return this.find("span.text-highlight").each(function() {
  this.parentNode.firstChild.nodeName;
  with (this.parentNode) {
   replaceChild(this.firstChild, this);
   normalize();
  }
 }).end();
};



function get_params() {
    var vars = [], hash;
    var hashes = window.location.href.slice(
    window.location.href.indexOf('?') + 1).split('&');
    for (var i = 0; i < hashes.length; i++) {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}





Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};



function exists(recs, id){
    for(var r in recs){
        if(recs[r].id == id)
            return true
    }
    return false
}


function bind_events(){
    $("#headlink-right .mobile-nav").on('click',
        function(event){
          event.stopPropagation();
          $("#headlink-right a").toggleClass("toggle-nav");
        });
    $("#back-top a").click(function(){
      window.scrollTo(0,0);
    });

    $('.collapsible').off('click')
    $('.collapsible').on('click',
        function(event){
            event.stopPropagation();
            var target = $(this).attr("data")
            //console.log(target)
            $('#'+ target).toggle();
            if($('#'+target).is(':visible')){
                //$(this).find('.arrow').html('▾');
                $(this).find('.arrow').removeClass("arrow-right").addClass("arrow-down");
            }else{
                //$(this).find('.arrow').html('▸');
                $(this).find('.arrow').removeClass("arrow-down").addClass("arrow-right");
            }
        });

    $('.session-collapsible').off('click')
    $('.session-collapsible').on('click',
        function(event){
            enable_loading("opening a session...");
            event.stopPropagation();
            var s = $(this).parents('div.session:first')
            s.find('.paper-container').toggle();
            if(s.find('.paper-container').is(':visible')){
                s.find('.arrow').removeClass("arrow-right").addClass("arrow-down");
            }else{
                s.find('.arrow').removeClass("arrow-down").addClass("arrow-right");
            }
            disable_loading();
        });

    $('input:text').addClass('default-search-text')
    $('input:text').each(function(){
        if($(this).attr("title") == null || $(this).attr("title") == ''){
            $(this).attr("title", 'Enter paper titles, authors, or keywords')
        }
    });

  
    $(".default-search-text").focus(
        function() {
        if ($(this).val() == $(this).attr("title")) {
            $(this).removeClass("default-search-text-active");
            $(this).val("");
        }
    });



    
    $(".default-search-text").blur(
        function() {
        if ($(this).val() == "") {
            $(this).addClass("default-search-text-active");
            $(this).val($(this).attr("title"));
        }
    });

    $('input:text').each(function(){
        if( $(this).val() == '' || $(this).val() == $(this).attr("title")){
            $(this).blur()
        }else{
            $(this).focus()
        }
    });

    $("#refresh_recommendations").off('click')
    $("#refresh_recommendations").on('click', function(event){
        event.stopImmediatePropagation();
        populate_recs(recommended);
    })
    
    if(detect_mobile()){
        /*

        var needs_scroll_update = false;
        $(document).scroll(function(){
            if(needs_scroll_update) {
                setTimeout(function() {
                    $("body").css("height", "+=1").css("height", "-=1");
                }, 0);
            }
        });
        $("input:text").live("focus", function(e) {
            needs_scroll_update = true;
        });

        $("input:text").live("blur", function(e) {
            needs_scroll_update = false;
        });

        */

        $('#search_papers').keyup(function(event){
            var str = $(this).val()
            if(str==""){
                reset_all_papers()
                $('#show_papers').show();
            }else{
                $('#show_papers').hide();
            }
            
        });


        $('#search_session').keyup(function(event){
            var str = $(this).val()
            if(str==""){
                reset_sessions()
            }
        });

        $('#search_sessions_btn').off('click')
        $('#search_sessions_btn').on('click', function(event){
                var str = $('#search_session').val()
                delay('simple_search_session("'+str+'");', 0);
            });


        $('#search_papers_btn').off('click')
        $('#search_papers_btn').on('click', function(event){
            var str = $('#search_papers').val()
            delay('simple_search_papers("'+str+'");', 0);
        });

        
    }else{
        $('#search_session').keyup(function(event){
            var str = $(this).val()
            delay('search_session("'+str+'");', 300);
        });


        $('#search_papers').keyup(function(event){
            var str = $(this).val()
            if(str==""){
                $('#show_papers').show();
            }else{
                $('#show_papers').hide();
            }
            delay('search_papers("'+str+'");', 300);
        });
        

        $('#search_sessions_btn').off('click')
        $('#search_sessions_btn').on('click', function(event){
                var str = $('#search_session').val()
                delay('search_session("'+str+'");', 0);
            });


        $('#search_papers_btn').off('click')
        $('#search_papers_btn').on('click', function(event){
            var str = $('#search_papers').val()
            delay('search_papers("'+str+'");', 0);
        });
        

    }
    
   

    

    $('#show_likes').on('click', function(){
        if($("#likes tr:visible").length > 2){
                $("#likes tr:gt(1)").hide()
                $("#show_likes").html('Show All')
        }else{
                $("#likes tr").show()
                $("#show_likes").html('Show Less')
        }
        update_likes_count();         
    });
    

    $('#show_recs').on('click', function(){
        var n = $('#recs tr:visible').length
        if((n+5) < $("#recs tr").length){
            $('#recs tr:lt('+(n+5)+')').show()               
        }else{
            $("#recs tr").show()
            $("#show_recs").hide()
        }
        update_recs_count();         
    });
    

    $('#show_papers').on('click', function(){
        var n = $('#all_papers tr:visible').length
        if((n+25) < $("#all_papers tr").length){
            $('#all_papers tr:lt('+(n+25)+')').show()               
        }else{
            $("#all_papers tr").show()
            $("#show_papers").hide()
        }
        update_papers_count();         
    });
}



var delay = (function(){
  var timer = 0;
  return function(callback, ms){
    clearTimeout (timer);
    timer = setTimeout(callback, ms);
  };
})();




function search_session(str){
    if(str==""){
        reset_sessions()
        return
    }
    var regex_str = ''
    var words = str.split(' ')
    for (var i=0;i<words.length; i++){
        regex_str += '(?=.*\\b'+words[i]+'.*\\b)'
    }
    var s =  new RegExp(regex_str , 'i')
    $('.session-timeslot').each(function(){
        $(this).prev().hide()
    });

      
    $('.session').each(function(){
        $(this).removeHighlight()
        if(s.test($(this).text())){
            $(this).show()   
            var p = $(this).attr("data")
            $("#"+p).show()
            $(this).highlight(str);
            //$(this).text().indexOf(str)        
        }else{
            $(this).hide()
            var p = $(this).attr("data")
            $("#"+p).hide()

        }

    });

    $('.session:visible').each(function(){
        $(this).parent().prev().show()
        
    });
    update_sessions_count(); 
    
}


function simple_search_session(str){
    
    $('.session-timeslot').each(function(){
        $(this).prev().hide()
    });

       
    $('.session').each(function(){
        if($(this).text().toLowerCase().indexOf(str.toLowerCase())!=-1){
            $(this).show()            
        }else{
            $(this).hide()
        }

    });

    $('.session:visible').each(function(){
        $(this).parent().prev().show()
        $('.session .paper').show()
    });
    update_sessions_count(); 
    
}

function search_papers(str){
    if(str==""){
        reset_all_papers()
        return
    }
    var regex_str = ''
    var words = str.split(' ')
    for (var i=0;i<words.length; i++){
        regex_str += '(?=.*\\b'+words[i]+'.*\\b)'
    }
    var s =  new RegExp(regex_str , 'i')
    
    //console.log(s)
       
    $('#all_papers .paper').each(function(){
        if(s.test($(this).text())){
            $(this).show()
            
        }else{
            $(this).hide()
        }

    });
    
    
    update_papers_visible_count(); 
}


function simple_search_papers(str){
   
       
    $('#all_papers .paper').each(function(){
        if($(this).text().toLowerCase().indexOf(str.toLowerCase())!= -1){
            $(this).show()
            
        }else{
            $(this).hide()
        }

    });
    

   

    update_papers_visible_count(); 
}




function refresh_recommendations(){
    populate_recs(recommended)
    update_recs(recommended)
}








function remove_special_chars(str){
    if (str == null || str == "null")
      return "";
    var result = str;
    result = result.replace(/¬/g, "-"); 
    result = result.replace(/×/g, "x"); 
    result = result.replace(/–/g, "-"); 
    result = result.replace(/‘/g, "'"); 
    result = result.replace(/’/g, "'"); 
    result = result.replace(/“/g, "\""); 
    result = result.replace(/”/g, "\""); 
    result = result.replace(/\\"/g, "\""); 
    result = result.replace(/â€”/g, "-");
    result = result.replace(/â€"/g, "-");
    result = result.replace(/â€˜/g, "'");
    result = result.replace(/â€œ/g, "\"");
    result = result.replace(/â€/g, "\"");
    result = result.replace(/Ã©/g, "é");
    result = result.replace(/\\u2013/g, "-");
    result = result.replace(/\\u00ac/g, "-");
    result = result.replace(/\\u2014/g, "-");
    result = result.replace(/\\u2018/g, "'");
    result = result.replace(/\\u2019/g, "'");
    result = result.replace(/\\u2022/g, "*");
    result = result.replace(/\\u201c/g, "\"");
    result = result.replace(/\\u201d/g, "\"");
    result = result.replace(/â€™/g, "'");
    result = result.replace(/â€“/g, "-");
    result = result.replace(/™/g, "(TM)"); 
    result = result.replace(/\\\//g, "/"); 
    result = result.replace(/\\/g, ""); 
    result = result.replace(/\\ \\/g, ""); 
    return result;
}




function format_venue(venue){
  if (venue == "paper")
    return "Paper";
  if (venue == "SIG")
    return "SIG Meeting";
  if (venue == "altchi")
    return "alt.chi";
  if (venue == "course")
    return "Course";
  if (venue == "casestudy")
    return "Case Study";
  if (venue == "panel")
    return "Panel";
  return venue;
}





function get_communities(entity){
  if (typeof entity.communities === "undefined" || entity.communities == null || entity.communities == "")
    return "";
  else
    return entity.communities.join(' ');

}

function get_short_session_info_of_paper(id){
  var result = "";
  var session = sessions[entities[id].session];
  var date = "";
  if (session.date == "Monday")
    date = "Mon";
  if (typeof session !== "undefined"){
    result += session.date.substring(0,3) + " " + session.time.substr(0,5) + " | " + session.room + " | " + session.s_title;
  }
  return result;
}

function get_session_info_of_paper(id){
  var result = "";
  var session = sessions[entities[id].session];
  if (typeof session !== "undefined"){
    result += session.date + " | " + session.time + " | " + session.room + " | " + session.s_title;
  }
  return result;
}


function get_paper_subtype(id){
    var subtype = "";
    if (typeof entities[id] !== "undefined" && entities[id].subtype != "")
      subtype = entities[id].subtype;
    else if (id.indexOf("tochi") > -1)
      subtype = "TOCHI";
    else {
      var session = sessions[entities[id].session];
      if (typeof session !== "undefined")
        subtype = format_venue(session.venue);
    }
    return "- " + subtype;
}

function codeExists(code){
  // if the given code has no video preview return false
  if ($.inArray(code, codeBlackList) > -1)
    return false;
  return true;

}

function isMyPaper(id){
  if ($.inArray(id, own_papers) > -1)
    return true;
  return false;
}


function get_paper_html(id){
    if(entities[id] == null)
        return ''
    var communities = get_communities(entities[id]);
    var raw_html = '<tr class="clickable paper ' + id
    if(exists(recommended, id)){
        raw_html += ' recommended'
    }
    if(starred[id] != null){
        raw_html += ' highlight'
    }
    if(entities[id].hm){
        raw_html += ' p_hm'
    }
    if(entities[id].award){
        raw_html += ' p_award'
    }
    if(communities != "")
      raw_html += ' communities'
    raw_html += '">'
      
    raw_html += '<td class="metadata">'   
    if(starred[id] == null){
        raw_html += '<div class="star star-open p_star" data="'+ id + '" onclick="handle_star(event);">'        
    }else{
        raw_html += '<div class="star star-filled p_star" data="'+ id + '" onclick="handle_star(event);">'       
    }
    raw_html += '</div>'
    
    raw_html += '</td>'
    
    raw_html += '<td class="content">'    
    raw_html += '<ul>'

    raw_html += '<li class="paper-title blue"><h3><a href="/paper?id='+id+'">'+remove_special_chars(entities[id].title) +'</a>'
    raw_html += '<span class="paper-subtype">' + get_paper_subtype(id) + '</span>'
    raw_html += '<span class="paper-code">' + codes['code'][id] + '</span>'
    //raw_html += '<span class="paper-session">' + get_short_session_info_of_paper(id) + '</span>'
    if (codeExists(codes['code'][id]))
      raw_html += '<span class="video-url"><a href="http://chischedule.org/2013/'+codes['code'][id]+'" target="_blank"><span class="play-icon"></span></a></span>'
    raw_html += '</h3>'
    raw_html += '</li>'


    raw_html += '<li class="paper-authors">'
    for(author in entities[id].authors){
        if(entities[id].authors[author] != null){
            raw_html += ' ' + entities[id].authors[author].givenName + ' ' + entities[id].authors[author].familyName + '&nbsp;&nbsp;&nbsp;&nbsp;'
        }
    }
    raw_html += '</li>'
      
    raw_html += '<li class="paper-icons"><span class="award-icon"></span><span class="hm-icon"></span>'
    if (isMyPaper(id))
      raw_html += '<span class="own-icon">my paper</span>'
    raw_html += '<span class="rec-icon">recommended</span>'
    if (communities != ""){
      $.each(entities[id].communities, function(i, v){
        raw_html += '<span class="community-icon ' + v + '">' + v + '</span>'
      });
    }
    raw_html += '</li>'
    if (entities[id].c_and_b == "null")
      raw_html += '<li class="paper-cb">'+ remove_special_chars(entities[id].abstract) + '</li>'
    else
      raw_html += '<li class="paper-cb">'+ remove_special_chars(entities[id].c_and_b) + '</li>'
        
    raw_html += '<li class="paper-keywords">' + remove_special_chars(entities[id].keywords) + '</li>'
    raw_html += '</ul>'
    raw_html += '</td>'
    
    raw_html += '</tr>'

    return raw_html
}







function get_session_html(id){
    var communities = get_communities(sessions[id]);
    var communities_class = (communities == "") ? "" : " communities";
    var award=''
    if(sessions[id].award || sessions[id].hm){
        award = 's_awardhm'
    }
    if(sessions[id].award){
        award += ' s_award'
    }
    if(sessions[id].award || sessions[id].hm){
        award += ' s_hm'
    }
    var raw_html = '<div class="session ' + id + ' ' + sessions[id].date + ' t' + sessions[id].time.substr(0,2) + ' '
              + sessions[id].venue + ' ' + sessions[id].personas.substr(0,2) + ' '
              + communities_class + ' ' + communities + ' ' + award + '" data="' + id + '">'
    raw_html += '<table class="session-container session-collapsible" data="' + id + '"><tr class="clickable">'
    
    raw_html += '<td class="metadata">'     
    //raw_html += '<div class="ui-state-default ui-corner-all s_star" data="'+ id + '" onclick="handle_session_star(event);">'
    raw_html += '<div class="star star-open s_star" data="'+ id + '" onclick="handle_session_star(event);">'
    //raw_html += '<span class="ui-icon ui-icon-star"></span>'
    raw_html += '</div>'        
    raw_html += '</td>'
    
    raw_html += '<td class="content">'  
    raw_html += '<ul>'
    raw_html += '<li><h3><span class="arrow arrow-right"></span> <span class="session-title">'+ remove_special_chars(sessions[id].s_title) + '</span>'
    /* 
    raw_html += '<span class="session-code">' + codes['code'][id] + '</span>'
    if (codeExists(codes['code'][id]))
      raw_html += '<span class="video-url"><a href="http://chischedule.org/2013/'+codes['code'][id]+'" target="_blank"><span class="play-icon"></span></a></span>'
    */
    raw_html += '</h3></li>'
    raw_html += '<li class="session-icons"><span class="award-icon"></span><span class="hm-icon"></span><span class="rec-icon">recommended</span>'

    if (communities != ""){
      $.each(sessions[id].communities, function(i, v){
        raw_html += '<span class="community-icon ' + v + '">' + v + '</span>'
      });
    }
    
    raw_html += '</li>';
    raw_html += '<li class="session-info"><span class="session-venue">' + format_venue(sessions[id].venue) + '</span> <span class="session-room">Room: ' + sessions[id].room + '</span></li>'
    raw_html += '</ul>'

    
    raw_html += '<div class="timeline">'
    var size = sessions[id].submissions.length
    var weight = []
    var sum = 0
    for(i=0; i<size; i++){
        if(entities[sessions[id].submissions[i]].subtype == 'Note'){
            weight[i] = 0.5
        }else{
            weight[i] = 1.0
        }
        sum += weight[i]
    }
    
    for(var i=0; i< size; i++){
        var w = 100*(weight[i]/sum)
        raw_html += '<div style="width:' + w + '%;"></div>'
    }
    raw_html += '</div>'
    raw_html += '</td>'
    
    raw_html += '</tr>'
    raw_html += '</table>'
    raw_html += '<table id="' +id +'" class="paper-container" style="display:none; padding-left:20px;">'
    for(var i in sessions[id].submissions){        
        raw_html += get_paper_html(sessions[id].submissions[i]);        
    }
    raw_html += '</table>'
    raw_html += '</div>'
    return raw_html
}



function get_selected_paper_html(id){
    if(entities[id] == null)
      return null
    var communities = get_communities(entities[id]);


    raw_html += '<tbody>'
    var raw_html = '<tr class="paper ' + id
    if(exists(recommended, id)){
        raw_html += ' recommended'
    }
    if(starred[id] != null){
        raw_html += ' highlight'
    }
    if(entities[id].hm){
        raw_html += ' p_hm'
    }
    if(entities[id].award){
        raw_html += ' p_award'
    }
    if(communities != ""){
      raw_html += ' communities';
    }
    raw_html += '">'


    raw_html += '<td class="metadata">'   
    if(starred[id] == null){
        raw_html += '<div class="star star-open p_star" data="'+ id + '" onclick="handle_star(event);">'        
    }else{
        raw_html += '<div class="star star-filled p_star" data="'+ id + '" onclick="handle_star(event);">'       
    }
    raw_html += '</div>'
    
    raw_html += '</td>'
    
    raw_html += '<td class="content">'    
    raw_html += '<ul>'



    raw_html += '<h3>' + remove_special_chars(entities[id].title) 
    raw_html += '<span class="paper-subtype">' + get_paper_subtype(id) + '</span>'
    raw_html += '<span class="paper-code">' + codes['code'][id] + '</span>'
    if (codeExists(codes['code'][id]))
      raw_html += '<span class="video-url"><a href="http://chischedule.org/2013/'+codes['code'][id]+'" target="_blank"><span class="play-icon"></span></a></span>'
    raw_html += '</h3>';

    raw_html += '<li class="paper-authors">'
    for(var author in entities[id].authors){
        if(entities[id].authors[author] != null){
          //console.log(entities[id]);
            //raw_html += entities[id].authors[author].givenName + ' ' + entities[id].authors[author].familyName + '&nbsp;&nbsp;&nbsp;&nbsp;'
            raw_html += '<span class="author"><span class="author-name">' 
                    + entities[id].authors[author].givenName + ' ' + entities[id].authors[author].familyName 
                    + '</span>';
            var affiliation = entities[id].authors[author].primary; 
            if (typeof affiliation !== "undefined" && affiliation != null && typeof affiliation.institution !== "undefined" && affiliation.institution != null && typeof affiliation.country !== "undefined" 
&& affiliation.country != null)
            raw_html += '<span class="author-affiliation">'
                    + affiliation.institution + ', ' + affiliation.country 
                    + '</span>';
            raw_html += '</span>';
        }
    }
    raw_html += '</li>'
    
    raw_html += '<li class="paper-icons"><span class="award-icon"></span><span class="hm-icon"></span>'
    if (isMyPaper(id))
      raw_html += '<span class="own-icon">my paper</span>'
    raw_html += '<span class="rec-icon">recommended</span>'
    if (communities != ""){
      $.each(entities[id].communities, function(i, v){
        raw_html += '<span class="community-icon ' + v + '">' + v + '</span>'
      });
    }
    raw_html += '</li>'
    raw_html += '<li class="paper-selected-session">' + get_session_info_of_paper(id) + '</li>'
    raw_html += '<hr />'
    raw_html += '<li>' + remove_special_chars(entities[id].abstract) + '</li>'
    raw_html += '<li class="paper-keywords">' + remove_special_chars(entities[id].keywords) + '</li>'
    raw_html += '</ul>'
    raw_html += '</td>'
    raw_html += '</tr>'
    raw_html += '</tbody>'
    raw_html += '</table>'
    return raw_html
}




function place_session(s){
    if(s.hasClass('Monday')){
        if(s.hasClass('t09')){
            $("#Mondayt09").append(s)
            $("#Mondayt09").prev().show()
        }else if(s.hasClass('t11')){
            $("#Mondayt11").append(s)
            $("#Mondayt11").prev().show()
        }else if(s.hasClass('t14')){
            $("#Mondayt14").append(s)
            $("#Mondayt14").prev().show()
        }else if(s.hasClass('t16')){
            $("#Mondayt16").append(s)
            $("#Mondayt16").prev().show()
        }

    }else if(s.hasClass('Tuesday')){
        if(s.hasClass('t09')){
            $("#Tuesdayt09").append(s)
            $("#Tuesdayt09").prev().show()
        }else if(s.hasClass('t11')){
            $("#Tuesdayt11").append(s)
            $("#Tuesdayt11").prev().show()
        }else if(s.hasClass('t14')){
            $("#Tuesdayt14").append(s)
            $("#Tuesdayt14").prev().show()
        }else if(s.hasClass('t16')){
            $("#Tuesdayt16").append(s)
            $("#Tuesdayt16").prev().show()
        }

    }else if(s.hasClass('Wednesday')){
        if(s.hasClass('t09')){
            $("#Wednesdayt09").append(s)
            $("#Wednesdayt09").prev().show()
        }else if(s.hasClass('t11')){
            $("#Wednesdayt11").append(s)
            $("#Wednesdayt11").prev().show()
        }else if(s.hasClass('t14')){
            $("#Wednesdayt14").append(s)
            $("#Wednesdayt14").prev().show()
        }else if(s.hasClass('t16')){
            $("#Wednesdayt16").append(s)
            $("#Wednesdayt16").prev().show()
        }

    }else if(s.hasClass('Thursday')){
        if(s.hasClass('t09')){
            $("#Thursdayt09").append(s)
            $("#Thursdayt09").prev().show()
        }else if(s.hasClass('t11')){
            $("#Thursdayt11").append(s)
            $("#Thursdayt11").prev().show()
        }else if(s.hasClass('t14')){
            $("#Thursdayt14").append(s)
            $("#Thursdayt14").prev().show()
        }else if(s.hasClass('t16')){
            $("#Thursdayt16").append(s)
            $("#Thursdayt16").prev().show()
        }

    }
}


function update_session_view(){
    $( ".session" ).each(function(s_index) {
        var session = $(this)
        $(this).find('.paper-container').find('.star').each(function(p_index){
            if($(this).hasClass('star-filled')){
                session.find('.timeline').children("div").eq(p_index).addClass("filled_yellow");
            }else{
                session.find('.timeline').children("div").eq(p_index).removeClass("filled_yellow");                  
            }
                        

        });

        $(this).find('.paper-container tr').each(function(p_index){
            if($(this).hasClass('recommended')){
                session.addClass('p_recommended')
                session.find('.timeline').children("div").eq(p_index).addClass("filled_blue");
            }else{                
                session.find('.timeline').children("div").eq(p_index).removeClass("filled_blue");
            }               

        });

        
        
        if($(this).find('.paper-container').find('.recommended').length > 0){
            $(this).find('.session-container').find('tr').addClass('recommended')
            session.addClass('s_recommended')
        }else{
            $(this).find('.session-container').find('tr').removeClass('recommended')
            session.removeClass('s_recommended')
        }
       
        if($(this).find('.paper-container').find('.star-filled').length > 0){
              $(this).find('.session-container').find('.star').removeClass('star-open').addClass('star-filled')
              $(this).find('.session-container').find('tr').addClass('highlight')
              session.addClass('s_starred')
        }else{
            $(this).find('.session-container').find('.star').removeClass('star-filled').addClass('star-open')
            $(this).find('.session-container').find('tr').removeClass('highlight')
            session.removeClass('s_starred')
        }
        
    });

    update_sessions_count();
}


function update_recs(){
      $('.paper').removeClass('recommended')
      for(var r in recommended){
            $('.'+recommended[r].id).each(function(){
                $(this).addClass('recommended')
            });
      }

}




function handle_session_star(event){
    enable_alert("updating information..."); 
    event.stopPropagation();
    var obj = $(event.target).parents("td:first").find('.s_star')
    var session_id = obj.attr("data")
    var papers = sessions[session_id]['submissions']
    //console.log(papers)
    if(obj.hasClass('star-filled')){
        $.post('/like/unstar', {'papers': JSON.stringify(papers)}, function(res) {
            for(var paper_id in papers){
                delete starred[papers[paper_id]]
            }
            $('.'+obj.attr('data')).each(function(){
                $(this).find('.p_star').removeClass('star-filled').addClass('star-open')
                $(this).removeClass('highlight')
                $(this).find('.paper').removeClass('highlight')
            })
            recommended = res.recs
            localStorage.setItem('starred', JSON.stringify(starred))
            localStorage.setItem('recommended', JSON.stringify(recommended))
            update_recs()
            update_session_view()
        })
        .done(function(){
            enable_alert("You unliked a session.");
        });
    }else{
        $.post('/like/star', {'papers': JSON.stringify(papers)}, function(res) {
            for(var paper_id in papers){
                starred[papers[paper_id]] = true
            }
            $('.'+obj.attr('data')).each(function(){
                $(this).find('.p_star').removeClass('star-open').addClass('star-filled')
                $(this).find('.paper').addClass('highlight')
            })
            recommended = res.recs
            localStorage.setItem('starred', JSON.stringify(starred))
            localStorage.setItem('recommended', JSON.stringify(recommended))
            update_recs()
            update_session_view()
        })
        .done(function(){
            enable_alert("You liked a session.");
        });
    }
    


}



function handle_star(event){ 
    enable_alert("updating information..."); 
    var obj = $(event.target).parents("td:first").find('.p_star')
    var paper_id = obj.attr("data")
    if(obj.hasClass('star-filled')){
        $.post('/like/unstar', {'papers': JSON.stringify([paper_id])}, function(res) {
          if(res.res[paper_id] == 'unstar'){
            $('.'+obj.attr('data')).each(function(){
                $(this).find('.p_star').removeClass('star-filled').addClass('star-open')
                //$(this).find('.p_star').removeClass('ui-state-active')
                $(this).removeClass('highlight')
            })

            delete starred[paper_id]
            populate_likes(starred)
            recommended = res.recs
            localStorage.setItem('starred', JSON.stringify(starred))
            localStorage.setItem('recommended', JSON.stringify(recommended))
            if($("#recs tr").length == 0){
                populate_recs(recommended)
            }        
            
            update_recs()
            update_session_view()
          }
        })
        .done(function(){
            enable_alert("You unliked a paper.");
        });
    }else{
        $.post('/like/star', {'papers': JSON.stringify([paper_id])}, function(res) {
          if(res.res[paper_id] == 'star'){
            $('.'+obj.attr('data')).each(function(){
                $(this).find('.p_star').removeClass('star-open').addClass('star-filled')
                $(this).addClass('highlight')
            })
            starred[paper_id] = true
            populate_likes(starred)
            recommended = res.recs
            localStorage.setItem('starred', JSON.stringify(starred))
            localStorage.setItem('recommended', JSON.stringify(recommended))
            if($("#recs tr").length == 0){
                populate_recs(recommended)
            }
            
            update_recs()
            update_session_view()
            
          }
        })
        .done(function(){
            enable_alert("You liked a paper.");
        });



    }
}



function load_paper(){
    var params = get_params()
    var paper_id = params['id']
    //console.log(paper_id)
    var selected_paper_html = get_selected_paper_html(paper_id)
    $('#selected_paper').find('.form').html(selected_paper_html)
    $('#similar_papers').html('')
    $.post('recs', {'papers': JSON.stringify([paper_id])}, 
    function(res){    
        var raw_html = '' 
        var recs_len = 20
        if(res.length < recs_len){
            recs_len = res.length
        }         
        for(var i = 0; i< recs_len; i++){
            raw_html += get_paper_html(res[i].id)            
        } 
        $('#similar_papers').html(raw_html) 
        
    });

    
} 

function update_papers_count(){
    setTimeout('update_papers_count_async();', 0)
}

function update_papers_count_async(){
    $("#papers_toggle .count").text("(" + $("#all_papers tr").length + ")");  
}

function update_papers_visible_count(){
    setTimeout('update_papers_visible_count_async();', 0)
}

function update_papers_visible_count_async(){
    $("#papers_toggle .count").text("(" + $("#all_papers tr:visible").length + ")");  
}

function update_recs_count(){
    setTimeout('update_recs_count_async();', 0)
}

function update_recs_count_async(){
    $("#recs_toggle .count").text("(" + $("#recs tr:visible").length + ")");  
}

function update_likes_count(){
    setTimeout('update_likes_count_async();', 0)
}

function update_likes_count_async(){
    $("#likes_toggle .count").text("(" + $("#likes tr").length + ")");  
}

function update_sessions_count(){
    setTimeout('update_sessions_count_async();', 0)
}

function update_sessions_count_async(){
    if ($("#program .session").length == $("#program .session:visible").length)
      $("#search-results .count").text("all");
    else
      $("#search-results .count").text($("#program .session:visible").length);  
}



function reset_all_papers(){
    $("#all_papers tr").show()
    $("#all_papers tr:gt(24)").hide()  

    if($("#all_papers tr:visible").length == $("#all_papers tr").length){
        $('#show_papers').hide();
    }else{
        $('#show_papers').show();
    }         
    update_papers_count();
}


function reset_sessions(){
    $('.session').show()
    $('.session').removeHighlight()
    $('.session-timeslot').each(function(){
        $(this).prev().hide()
    });  

    $('.session:visible').each(function(){
        $(this).parent().prev().show()
        
    });
    update_sessions_count(); 
}


function populate_papers(){
    var raw_html = ''       
    for(var e in entities){
        raw_html += get_paper_html(e)
    }
    $("#all_papers").html(raw_html)
    $("#all_papers tr:gt(24)").hide()  

    if($("#all_papers tr:visible").length == $("#all_papers tr").length){
        $('#show_papers').hide();
    }else{
        $('#show_papers').show();
    }         
    update_papers_count();
}


function populate_recs(){  
    var raw_html = ''   
    for(var r in recommended){
        raw_html += get_paper_html(recommended[r].id)
    }
    $("#recs").html(raw_html)

    $("#recs tr:gt(4)").hide()  

    if($("#recs tr:visible").length == $("#recs tr").length){
        $('#show_recs').hide();
    }else{
        $('#show_recs').show();
    }         
      
   update_recs_count(); 
}



function populate_likes(){  
    var raw_html = ''
    var liked_papers = Object.keys(starred)    
    for(var i = liked_papers.length; i>=0 ; i--){
       raw_html += get_paper_html(liked_papers[i])
    }
    $("#likes").html(raw_html)
    if($("#likes tr").length <= 2){
        $('#show_likes').hide();
    }else{
         $('#show_likes').show()
        if($('#show_likes').html() == 'Show All'){
            $("#likes tr:gt(1)").hide()           
        }
    }  
  update_likes_count();
}


function populate_sessions(){
    $(".session-timeslot").html("")
    $('.session-timeslot').each(function(){
        $(this).prev().hide()
    }); 
    for(var s in sessions){
        var raw_html = get_session_html(s)
        var row = $(raw_html)
        place_session(row)
    }
    update_session_view()
}







function setup_filters(){
    $('.filter').off('click')
    $('.filter').on('click', function(){       
        //enable_loading("applying filter...");

        var attr = $(this).attr("type")
        $('.'+attr).removeClass('active')

        $(this).addClass('active')

        var day_classes = '.'+$('.day.active').attr("title")
        var time_classes = '.'+$('.time.active').attr("title")
        var personas_classes = '.'+$('.persona.active').attr("title")
        var venues_classes = '.'+$('.venue.active').attr("title")
        var communities_classes = '.'+$('.community.active').attr("title")
        var papers_classes = '.'+$('.p_session.active').attr("title")
        /*
        console.log(day_classes)
        console.log(time_classes)
        console.log(venues_classes)
        console.log(personas_classes)
        console.log(papers_classes)
        */

        var select_class = $('.session')
        if(day_classes != '.all'){
            select_class = select_class.filter(day_classes)
        }
        
        if(time_classes!='.all'){               
            select_class = select_class.filter(time_classes)                
        }

        if(personas_classes!='.all'){               
            select_class = select_class.filter(personas_classes)                
        }

        if(venues_classes!='.all'){             
            select_class = select_class.filter(venues_classes)              
        }
        if(communities_classes!='.all'){             
            select_class = select_class.filter(communities_classes)              
        }

        if(papers_classes!='.all'){             
            select_class = select_class.filter(papers_classes)              
        }
       $('.session').hide();
       $('.session-timeslot').each(function(){
            $(this).prev().hide()
        });

       select_class.show();
       select_class.each(function(){
            $(this).parent().prev().show()
        });

       update_sessions_count(); 
    });
}



function enable_loading(msg){
  $("body .modal .message").text(msg);
  $("body").addClass("loading");
}



function disable_loading(){
  $("body").removeClass("loading");
}



function enable_alert(msg){
  $("body .alert .message").text(msg);
  $("body").addClass("notice");
  setTimeout(function(){
    $("body").removeClass("notice");
  }, 2000);
}
