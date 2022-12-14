function displayOrders(data){
    //empty old data
    $("#order_container").empty()

    //insert all new data
    $.each(data['orders'], function(i, datum){
        let location_container = $("<span class = 'location'></span>")
        let location_r = $("<a class='words' style='width: auto'>"+datum['region']+"/</a>")
        location_r.attr("href", curr_url+"/composite/marketorders/"+data['type_id']+"/by_range/"+datum['region_id'])
        let location_c = $("<a class='words' style='width: auto'>"+datum['cons']+"/</a>")
        location_c.attr("href", curr_url+"/composite/marketorders/"+data['type_id']+"/by_range/"+datum['cons_id'])
        let location_s = $("<a class='words' style='width: auto'>"+datum['system']+"/</a>")
        location_s.attr("href", curr_url+"/composite/marketorders/"+data['type_id']+"/by_range/"+datum['system_id'])
        let location_st = $("<a class='station'>"+datum['station_name']+"</a>")
        location_st.attr("href", curr_url+"/composite/marketorders/"+data['type_id']+"/"+datum['station_id'])
        let duration = $("<span class='words'>"+datum['duration']+"</span>")
        let is_buy_order = $("<span class='words'>"+datum['is_buy_order']+"</span>")
        let price = $("<span class='words'>"+datum['price']+"</span>")
        let volume_remain = $("<span class='words'>"+datum['volume_remain']+"</span>")
        let volume_total = $("<span class='words'>"+datum['volume_total']+"</span>")
        let last_modified = $("<span class='words'>"+datum['last_modified']+"</span>")

        let new_row= $("<div></div>")
        location_container.append(location_r)
        // location_container.append(location_c)
        location_container.append(location_s)
        location_container.append(location_st)

        new_row.append(location_container)
        new_row.append(duration)
        new_row.append(is_buy_order)
        new_row.append(price)
        new_row.append(volume_remain )
        new_row.append(volume_total)
        new_row.append(last_modified)

        $("#order_container").append(new_row)
        $("#order_container").append($("<hr>"))
    })
}

$(document).ready(function(){
    //when the page loads, display all the names
    $.each(data['links'], function(i, datum) {
        if (datum['rel']=="item detail"){
            $("#item_name").attr("href", datum['href'])
        }
    })
    console.log(data)
    $("#item_name").append(data['type_name'])
    $("#item_id").append(data['type_id'])
    console.log(url)
    $("#station_id").attr('href', url+'?offset='+data['offset']+"&limit="+data['limit']+"&sorted=ASC&sorted_by=station_id")
    $("#duration").attr('href', url+'?offset='+data['offset']+"&limit="+data['limit']+"&sorted=ASC&sorted_by=duration")
    $("#is_buy_order").attr('href', url+'?offset='+data['offset']+"&limit="+data['limit']+"&sorted=ASC&sorted_by=is_buy_order")
    $("#price").attr('href', url+'?offset='+data['offset']+"&limit="+data['limit']+"&sorted=ASC&sorted_by=price")
    $("#volume_remain").attr('href', url+'?offset='+data['offset']+"&limit="+data['limit']+"&sorted=ASC&sorted_by=volume_remain")
    $("#volume_total").attr('href', url+'?offset='+data['offset']+"&limit="+data['limit']+"&sorted=ASC&sorted_by=volume_total")
    $("#last_modified").attr('href', url+'?offset='+data['offset']+"&limit="+data['limit']+"&sorted=ASC&sorted_by=last_modified")

    let sort_index = data['sort_index']
    let sort_flag = data['sort_flag']

    let limit = data['limit']
    let offset = data['offset']
    let next = data['next']
    console.log(parseInt(limit)+parseInt(offset))

    if (offset!=0){
        $("#page").append("<a class='previous' id='previous'>previous</a>")
        $("#previous").attr('href', url+'?offset='+String(parseInt(data['offset'])-parseInt(data['limit']))+"&limit="+data['limit']+"&sorted=ASC&sorted_by=is_buy_order")
    }

    if (next!=0){
        $("#page").append("<a class='next' id='next'>next</a>")
        $("#next").attr('href', url+'?offset='+String(parseInt(data['offset'])+parseInt(data['limit']))+"&limit="+data['limit']+"&sorted=ASC&sorted_by=is_buy_order")
    }

    if (sort_index != ''){
        if (sort_flag==1){
            $("#"+sort_index).append('↑')
            $("#"+sort_index).attr('href', url+'?offset='+data['offset']+"&limit="+data['limit']+"&sorted=DESC&sorted_by="+sort_index)
        }
        else{
            $("#"+sort_index).append('↓')
        }
    }



    displayOrders(data)

})