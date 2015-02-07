var bids=new Array();
var aids=new Array();
var eids=new Array();
var nids=new Array();
var dids=new Array();
var gids=new Array();
var vids=new Array();
var module=['/business/','/events/','/article/','/news/','/videos/','/gallery/','/deal/']
var category=new Array();
var cat='';
var category_name='';
	
function details_pages(bids){
	var pathname = window.location.pathname;
	org_path=pathname;
	var click = true;
	reports_data(pathname,bids,category,org_path,click);
	}



function module_listing(bids,category){
	var pathname = window.location.pathname;
	org_path=pathname;
	var click = false;
	reports_data(pathname,bids,category,org_path,click);
}

function home_stats(bids,eids,aids,vids,gids,dids,nids){
    var pathname = window.location.pathname;
	org_path=pathname;
	var click=false;
	reports_data(module[0],bids,category,org_path,click);
    reports_data(module[1],eids,category,org_path,click);
    reports_data(module[2],aids,category,org_path,click);
    reports_data(module[3],nids,category,org_path,click);
    reports_data(module[4],vids,category,org_path,click);
    reports_data(module[5],gids,category,org_path,click);
    reports_data(module[6],dids,category,org_path,click);

}