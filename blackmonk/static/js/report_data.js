function reports_data(pathname,bids,cat,org_path,click)
{
var array_data='';
var module=[];
var search='';
var path=org_path;

search = $("#id_track_search").val();
    if(search==1)
    {
    senddata += "&search="+ search;
    }
    array_data='bids='+bids;
    array_data += '&cat='+cat;
    array_data += "&pathname="+pathname;
    array_data += "&search="+search;
    array_data += "&org_path="+org_path;
    array_data += "&clicks="+click;
    $.ajax({
            type: "GET",
            url: "/reports/",
            data: array_data,
            success: function(response){
            if(response==1)
            {
            return true;
            }
            else
            {
            return false;
            }
            }
    });
    
}