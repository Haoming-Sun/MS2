$(document).ready(function() {
    $("#searchResultBox").empty();
    $("#searchFrom").ajaxForm(function(data) {
        if(data) {
            $("#searchResultBox").empty();
            console.log(data);
            if (data.type=="3"){
                data.solar_system_name=data.name
            }
            else if(data.type=="2"){
                data.constellation_name=data.name
            }
            else if(data.type=="1"){
                data.region_name=data.name
            }
            $("#searchResultBox").html(`
            <div style={{whiteSpace: 'pre-line'}}>
            
             <div class = 'items1'>item name: <span class = 'words1'  id="item_name">${data.name}</span> </div> 
             <div class = 'items1'>item id:  <span class="words1" id="item_id">${data.id}</span> </div>
             <div class = 'itemdetail1'>type: <span class="words1" id="item_type">${data.type}</span></div>
             <div class = 'itemdetail1'>solar_system_name: <span class="words1" id="solar_system_name">${data.solar_system_name}</span></div>
             <div class = 'itemdetail1'>constellation_name: <span class="words1" id="constellation_name">${data.constellation_name}</span></div>
             <div class = 'itemdetail1'>region_name: <span class="words1" id="region_name">${data.region_name}</span></div>
            
             <div class="container-fluid px-lg-12" style="width:200%;margin-left:10px">
             <div class="row mx-lg-n5">
               <div class="col-lg-3 py-3 px-lg-4 station" id="stations_id">stations_id:</div>
               <div class="col-lg-9 py-3 px-lg-5 station" id="stations_name">station_name: </div>
             </div>
             </div>
           </div>
            
           `);

            data.stations.forEach(obj => {
                $("#stations_id").append(`<div class = 'words1' >${obj.station_id}</div>`)
                $("#stations_name").append(` <div class = 'words1' >${obj.station_name}</div>`)
            })
        }
        else{
            $("#searchResultBox").empty()
            $("#searchResultBox").append("<div class='error_note'>No such location!</div>")
        }
    });
})