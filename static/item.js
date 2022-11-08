$(document).ready(function(){
    $("#item_name").append(data['type_name'])
    $("#item_id").append(data['type_id'])
    $("#mass").append(data['mass'])
    $("#volume").append(data['volume'])
    $("#description").append(data['description'])
    console.log(data['description'])
    $.each(data['links'], function(i, datum) {
        if (datum['rel']=="market order"){
            $("#show_orders").attr("href", datum['href'])
        }
    })
})