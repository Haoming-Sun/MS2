function expand_cate(group_id){
    console.log(group_id)
    let curr = $("#"+group_id)
    if (curr.attr('expand') == '1'){
        $("#show_"+group_id).empty()
        curr.attr('expand','0')
        let text = curr.text().slice(0,-1)+'→'
        let img = $("<img class='icon'>")
        img.attr('src','https://evemarketer.com/static/img/market_groups/'+curr.attr('icon_id')+'.png')
        img.attr('onerror',"this.onerror=null; this.src='https://evemarketer.com/static/img/market_groups/0.png'")
        curr.empty()
        curr.append(img)
        curr.append(text)
    }
    else{
        curr.attr('expand','1')
        let text = curr.text().slice(0,-1)+'↓'
        let img = $("<img class='icon'>")
        img.attr('src','https://evemarketer.com/static/img/market_groups/'+curr.attr('icon_id')+'.png')
        img.attr('onerror',"this.onerror=null; this.src='https://evemarketer.com/static/img/market_groups/0.png'")
        curr.empty()
        curr.append(img)
        curr.append(text)
        var data={'parent':curr.attr('id')}
        let next_level = String(parseInt(curr.attr('level'))+1)
        $.ajax({
            type: "POST",
            url: host_url + "/api/marketorders",
            dataType : "json",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(data),
            success: function (response) {
                if (response['is_item'] == '0'){
                    $.each(response['data'], function(i, datum) {
                        let img = $("<img class='icon'>")
                        img.attr('src','https://evemarketer.com/static/img/market_groups/'+datum['icon_id']+'.png')
                        img.attr('onerror',"this.onerror=null; this.src='https://evemarketer.com/static/img/market_groups/0.png'")
                        let new_cate = $("<div class='category' id="+datum['market_group_id']+"></div>")
                        new_cate.attr('level',next_level)
                        new_cate.attr('icon_id',datum['icon_id'])
                        new_cate.attr('group_name',datum['market_group_name'])
                        new_cate.attr('expand','0')
                        new_cate.attr('onclick',"expand_cate("+datum['market_group_id']+")")
                        new_cate.attr('style', "background: rgba(150,150,255,"+String(1-0.2*parseInt(next_level))+"); ")
                        new_cate.append(img)
                        new_cate.append(datum['market_group_name']+"→")
                        $("#show_"+group_id).append(new_cate)
                        $("#show_"+group_id).append("<div class='cate_show' id=show_"+datum['market_group_id']+"></div>")
                    })

                }
                else{
                    $.each(response['data'], function(i, datum) {
                        let new_cate = $("<a class='category' id="+datum['type_name']+">"+datum['type_name']+"</a> <br>")
                        new_cate.attr('level',next_level)
                        new_cate.attr('href',curr_url+"/marketorders/"+datum['type_id'])
                        new_cate.attr('style',"background: rgba(255,255,255,1);")
                        $("#show_"+group_id).append(new_cate)
                    })
                }

            },
            error: function(request, status, error){
                console.log("Error");
                console.log(request)
                console.log(status)
                console.log(error)
            }
        })
    }
}

function verify(name){
    $.ajax({
        type: "GET",
        url: host_url+"/api/item/"+name,
        success: function (response) {
            window.location.href = curr_url+"/marketorders/"+name
        },
        error: function(request, status, error){
            console.log("Error");
            $('#search_note').empty()
            $('#search_note').append("<span style='color: red; margin-left: 25px'>Wrong item name!</span>")
            $('#search_input').val('')
        }
    })
}

$(document).ready(function(){
    //when the page loads, display all the names
    $("#search_input").focus()
    $("#search_input").autocomplete({
        source: name_diction
    })
    $('#search_input').keyup(function (event){
        if (event.which == 13) {
            $("#search_button").trigger('click')
        }
    })
    $("#search_button").click(function (event) {
        var name = $("#search_input").val().trim()
        console.log(name)
        verify(name)
    });

    $.each(data['data'], function(i, datum) {
        let img = $("<img class='icon'>")
        img.attr('src','https://evemarketer.com/static/img/market_groups/'+datum['icon_id']+'.png')
        img.attr('onerror',"this.onerror=null; this.src='https://evemarketer.com/static/img/market_groups/0.png'")
        let new_cate = $("<div class='category' id="+datum['market_group_id']+"></div>")
        new_cate.attr('level','0')
        new_cate.attr('icon_id',datum['icon_id'])
        new_cate.attr('group_name',datum['market_group_name'])
        new_cate.attr('expand','0')
        new_cate.attr('onclick',"expand_cate("+datum['market_group_id']+")")
        new_cate.append(img)
        new_cate.append(datum['market_group_name']+"→")
        $("#cate_container").append(new_cate)
        $("#cate_container").append("<div class='cate_show' id=show_"+datum['market_group_id']+"></div>")
    })
})