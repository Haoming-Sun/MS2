function displayOrders(data){
    //empty old data
    $("#order_container").empty()

    //insert all new data
    $.each(data['orders'], function(i, datum){
        let station_id = $("<span class='words'>"+datum['station_id']+"</span>")
        let duration = $("<span class='words'>"+datum['duration']+"</span>")
        let is_buy_order = $("<span class='words'>"+datum['is_buy_order']+"</span>")
        let price = $("<span class='words'>"+datum['price']+"</span>")
        let volume_remain = $("<span class='words'>"+datum['volume_remain']+"</span>")
        let volume_total = $("<span class='words'>"+datum['volume_total']+"</span>")
        let last_modified = $("<span class='words'>"+datum['last_modified']+"</span>")

        let new_row= $("<div></div>")
        new_row.append(station_id)
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
    let url = ""
    $.each(data['links'], function(i, datum) {
        if (datum['rel']=="item detail"){
            $("#item_name").attr("href", datum['href'])
        }
        if (datum['rel']=='sort'){
            url = datum['href']
        }
    })
    console.log(data)
    $("#item_name").append(data['type_name'])
    $("#item_id").append(data['type_id'])

    $("#station_id").attr('href', url+'?offset='+data['offset']+"&limit="+data['limit']+"&sorted=ASC&sorted_by=station_id")
    $("#duration").attr('href', url+'?offset='+data['offset']+"&limit="+data['limit']+"&sorted=ASC&sorted_by=duration")
    $("#is_buy_order").attr('href', url+'?offset='+data['offset']+"&limit="+data['limit']+"&sorted=ASC&sorted_by=is_buy_order")
    $("#price").attr('href', url+'?offset='+data['offset']+"&limit="+data['limit']+"&sorted=ASC&sorted_by=price")
    $("#volume_remain").attr('href', url+'?offset='+data['offset']+"&limit="+data['limit']+"&sorted=ASC&sorted_by=volume_remain")
    $("#volume_total").attr('href', url+'?offset='+data['offset']+"&limit="+data['limit']+"&sorted=ASC&sorted_by=volume_total")
    $("#last_modified").attr('href', url+'?offset='+data['offset']+"&limit="+data['limit']+"&sorted=ASC&sorted_by=last_modified")

    let sort_index = data['sort_index']
    let sort_flag = data['sort_flag']

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