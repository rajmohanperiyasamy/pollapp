function ajaxFunction()
{
	var xmlHttp;
	try{
		// Firefox, Opera 8.0+, Safari
		xmlHttp=new XMLHttpRequest();
	}
	catch (e){
		// Internet Explorer
	  	try{
	    	xmlHttp=new ActiveXObject("Msxml2.XMLHTTP");
	    }
		catch (e){
		    try{
		    	xmlHttp=new ActiveXObject("Microsoft.XMLHTTP");
		    }
		    catch (e){
		    	alert("Your browser does not support AJAX!");
		    	return false;
		    }
		}
	}
	return xmlHttp;
}

var httplogin = ajaxFunction();
function isLogin(objdiv){
	httplogin.onreadystatechange=function()
	    {
    	if(httplogin.readyState==4){
    		var data = httplogin.responseText;
    		if(data=='1'){
    			objdiv.style.display='';
    		}else{
    			alert("Please login! ");
    		}
    	}
    }
    var url = "/article/logincheck/";
	httplogin.open("GET",url,true);
	httplogin.send(null);
}


function trim(str){
	if(!str || typeof str != 'string')
		return '';
	return str.replace(/^[\s]+/,'').replace(/[\s]+$/,'').replace(/[\s]{2,}/,' ');
}

// comapre dates # true=s>e  #false=s<e   #dateformat=dd/mm/yyyy
function comparedate(S,E){
	S = S.replace(/(\d+).(\d+).(\d+)/, '$3/$2/$1');
	S = S.replace(/^(\d\d\/)/, '20$1');
	SD = new Date(S);
	E = E.replace(/(\d+).(\d+).(\d+)/, '$3/$2/$1')
	E = E.replace(/^(\d\d\/)/, '20$1')
	ED = new Date(E);
	if(SD>ED)
		return false;
	else
		return true;		
}

var xmlHttpcaptcha=ajaxFunction();
function getcaptcha(imgObj,hashObj){
	xmlHttpcaptcha.onreadystatechange=function()
    {
    	if(xmlHttpcaptcha.readyState==4){
    		var data = xmlHttpcaptcha.responseText;
    		detail = data.split(",");
    		hashObj.value=detail[0];
    		imgObj.src='/site_media/images/captcha/'+detail[1];
    	}
    }
    var imgf = imgObj.src; 
    var img = imgf.split("/site_media/images/captcha/");
    var url = "/getcaptcha/?img="+img[1];
	xmlHttpcaptcha.open("GET",url,true);
	xmlHttpcaptcha.send(null);
}
