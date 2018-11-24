var url = "http://localhost:3000";
var users = [
    {
        "lat": "46.490036",
        "long": "6.353213",
        "dest": "Genève"
    },
    {
        "lat": "46.453831",
        "long": "6.293492",
        "dest": "Lausanne"
    },
    {
        "lat": "46.206415",
        "long": "6.140399",
        "dest": "Lausanne"
    },
    {
        "lat": "46.272339",
        "long": "6.161429",
        "dest": "Lausanne"
    },
    {
        "lat": "46.272339",
        "long": "6.161429",
        "dest": "Genève"
    }
];
$(document).ready(function(){

    loadUsers();

    $("#add").on('click', function (e) {
        var long = $("#long").val();
        var lat = $("#lat").val();
        var dest = $("#dest").val();
        users.push({"lat": lat, "long": long, "dest": dest});
        loadUsers();
        return false;
    });
    $("#compute").on('click', function(e){
        var arr = users;
        alert(url+"/compute");
        $.ajax(
            {
                url: url+"/compute",
                type: "POST",
                data: JSON.stringify(arr),
                contentType: 'application/json; charset=utf-8',
                dataType: 'jsonp',
                async: true,
                success: function(msg) {
                    console.log(msg);
                },
                failure: function(errMsg) {
                    alert(errMsg);
                }
            }
        );
    });
});

function loadUsers(){
    $("#users").empty();
    $.each(users, function( key, value ) {
        $("#users").append("<li><span>"+key+"</span> lat: "+value.lat+", long: "+value.long+", destination: "+value.dest+"</li>");
    });
}