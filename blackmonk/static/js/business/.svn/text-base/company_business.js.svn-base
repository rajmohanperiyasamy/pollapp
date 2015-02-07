
	function add_coupons(bid,url){
			var data = "<input type='hidden' name='bid' value='"+bid+"' />";
			data +=    "<input type='hidden' name='title' value='"+$('#id_c_title').val()+"' />";
			data +=    "<input type='hidden' name='description' value='"+$('#id_c_description').val()+"' />";
			data +=    "<input type='hidden' name='end_date' value='"+$('#id_end_date').val()+"' />";
			$('#loadingGal').show();
			$.ajaxFileUpload({
				url:url,
				secureuri:false,
				fileElementId:'id_c_photo',
				dataType: 'html',
				data: data,
				success: function (data, status){
					$('#coupons_list').html(data);
					$('#loadingGal').hide();
				},
				error: function (data, status, e){
					alert(e);
				}
			});
	}
	function delete_coupons(bid,cid,url){
		$(document).ready(function(){
			$.ajax({
				type: "GET",
				url:url,
				data:"bid="+bid+"&cid="+cid,
				success: function(html_from_server){
					$('#coupons_list').html(html_from_server);
				}
			});	
		});
	}
	function edit_coupons(cid){
		$('#coupon_list_display'+cid).hide();
		$('#coupon_list_edit'+cid).show();
		$('#expirydate'+cid).datepicker();
	}
	function update_coupons(bid,cid,url){
			var data = "bid="+bid+"&cid="+cid
			data += '&title='+$('#title'+cid).val();
			data += '&description='+$('#description'+cid).val();
			data += '&end_date='+$('#expirydate'+cid).val();
			$('#loadingGal').show();
			$.ajax({
				dataType: "POST",
				url:url,
				dataType:'json',
				data:data,
				success: function(Rdata){
					$('#loadingGal').hide();
					$('#coupon_list_edit'+cid).fadeOut(300)
					var hl = '<h4>'+Rdata.title+'</h4><p class="description">'+Rdata.description+'</p><span class="exp">Expiry date: '+Rdata.end_date+'</span>';
					$('#coupon_list_display'+cid).html(hl);
					$('#coupon_list_display'+cid).fadeIn(300)
				}
			});
	}
	
	
	
	
	function add_product(bid,url){
			var data = "<input type='hidden' name='bid' value='"+bid+"' />";
			data +=    "<input type='hidden' name='title' value='"+$('#id_p_title').val()+"' />";
			data +=    "<input type='hidden' name='description' value='"+$('#id_p_description').val()+"' />";
			data +=    "<input type='hidden' name='price' value='"+$('#id_p_price').val()+"' />";
			$.ajaxFileUpload({
				url:url,
				secureuri:false,
				fileElementId:'id_p_photo',
				dataType: 'html',
				data: data,
				success: function (data, status){
					$('#products_list').html(data);
				},
				error: function (data, status, e){
					alert(e);
				}
			});
	}
	function delete_product(bid,pid,url){
		$(document).ready(function(){
			$.ajax({
				type: "GET",
				url:url,
				data:"bid="+bid+"&pid="+pid,
				success: function(html_from_server){
					$('#products_list').html(html_from_server);
				}
			});	
		});
	}
	function edit_product(pid){
		$('#product_list_display'+pid).hide();
		$('#product_list_edit'+pid).show();
		$('#expirydate'+pid).datepicker();
	}
	function update_product(bid,pid,url){
			var data = "bid="+bid+"&pid="+pid
			data += '&title='+$('#title_p_'+pid).val();
			data += '&description='+$('#description_p_'+pid).val();
			data += '&price='+$('#price_p_'+pid).val();
			$.ajax({
				dataType: "POST",
				url:url,
				dataType:'json',
				data:data,
				success: function(Rdata){
					$('#product_list_edit'+pid).fadeOut(300)
					var hl = '<h4>'+Rdata.title
					if(Rdata.price){
						hl += '<span class="price">$'+ Rdata.price +'</span>'
					}
					hl += '</h4><p class="description">'+Rdata.description+'</p>';
					$('#product_list_display'+pid).html(hl);
					$('#product_list_display'+pid).fadeIn(300)
				}
			});
	}
	

