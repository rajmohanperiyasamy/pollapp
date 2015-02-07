//Caution this file is shared by home.html , albumdetails.html & classifieds.html

stepcarousel.setup({
	galleryid: 'galleryc', //id of carousel DIV
	beltclass: 'belt', //class of inner "belt" DIV containing all the panel DIVs
	panelclass: 'panel', //class of panel DIVs each holding content
	panelbehavior: {speed:500, wraparound:true, persist:false},
	defaultbuttons: {enable: false, moveby: 1, leftnav: ['arrowl.gif', -10, 100], rightnav: ['arrowr.gif', -10, 100]},
	statusvars: ['reportA', 'reportB', 'reportC'],
	contenttype: ['inline'] //content setting ['inline'] or ['external', 'path_to_external_file']
})
