function updateStreams() {
    $.ajax({
        type: 'GET',
        url: 'https://mc1.my-colony.com/api.php?pf=5&g=1',
        dataType: 'json',
        success: function (data) {
            var show_streams = "Live-streaming now :";
            for (i in data) {
                //console.log(data);
                //console.log(i);
                show_streams += '<br><span style="color: rgb(0, 255, 0);">&bull;</span> <a target="_blank" href="https://mc1.my-colony.com/colonies/'+data[i]['charter']+'" >'+data[i]['colony']+' ('+data[i]['user']+')</a>';
            }
            if (show_streams == 'Live-streaming now :') {
                document.getElementById("curr_streaming").innerHTML = '';
            } else {
            document.getElementById("curr_streaming").innerHTML = show_streams+"<hr>";
            }
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) { 
        document.getElementById("curr_streaming").innerHTML = "Status: " + textStatus+"<br>Error: " + errorThrown+"<hr>";
        }
    });
}

function fn60sec() {
    // runs every 60 sec and runs on init.
    //console.log('updating streams');
    updateStreams();
}

$( document ).ready(function() {
    fn60sec();
    setInterval(fn60sec, 60*1000);
});
