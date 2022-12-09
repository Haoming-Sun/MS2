$(document).ready(function(){
    $("#item_name").append(data['type_name'])
    $("#item_id").append(data['type_id'])
    $("#mass").append(data['mass'])
    $("#volume").append(data['volume'])
    $("#description").append(data['description'])
    console.log(data['description'])
    // $.each(data['links'], function(i, datum) {
    //     if (datum['rel']=="market order"){
    //         $("#show_orders").attr("href", datum['href'])
    //     }
    // })
    var url = window.location.href
    var arr = url.split("/")
    var curr_url = arr[0] + "//" + arr[2]
    $("#show_orders").attr("href",curr_url+"/composite/marketorders/"+data['type_id'])
})