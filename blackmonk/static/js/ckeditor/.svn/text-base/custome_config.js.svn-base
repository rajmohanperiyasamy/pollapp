CKEDITOR.editorConfig = function( config )
{
	config.toolbarCanCollapse = false;
	config.disableNativeSpellChecker = false;
	config.font_defaultLabel = 'Arial';
	config.forcePasteAsPlainText = true;
	config.fontSize_defaultLabel = '12px';
	config.fontSize_sizes = '8/8px;9/9px;10/10px;11/11px;12/12px;14/14px;16/16px;18/18px;20/20px;22/22px;';
	config.format_tags = 'p;h2;h3;h4';
	config.toolbar_Basic = [ [ 'Bold', 'Italic','Underline','Strike','Link', 'Unlink','NumberedList', 'BulletedList','Outdent', 'Indent' ] ];
	config.toolbar_Full = [
						{ name: 'document', items : [ 'Source','-'] },
                        { name: 'clipboard', items : ['Undo','Redo' ,'-'] },
                        { name: 'editing', items : [ 'Find','-'] },
                        { name: 'paragraph', items : [ 'NumberedList','BulletedList','-','Outdent','Indent','Blockquote','- ','JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'] },
						{ name: 'basicstyles', items : [ 'Bold','Italic','Underline','Strike','-','RemoveFormat','-' ] },
                        { name: 'links', items : [ 'Link','Unlink','-'] },
                        { name: 'insert', items : [ 'Image','HorizontalRule','-'] },
                        { name: 'styles', items : [ 'Format','FontSize'] },
						{ name: 'tools', items : [ 'Maximize' ]}
					];
	config.toolbar_Basic_Image = [ [ 'Bold', 'Italic','Underline','Strike','Link', 'Unlink','NumberedList', 'BulletedList','Outdent', 'Indent' ],{ name: 'insert', items : [ 'Image','HorizontalRule'] } ];
	config.removePlugins = 'tabletools,contextmenu,resize';
};

CKEDITOR.on( 'dialogDefinition', function( ev )
	{
		ev.data.definition.resizable = CKEDITOR.DIALOG_RESIZE_NONE;
		

		var dialogName = ev.data.name;
		var dialogDefinition = ev.data.definition;
		
		
		if ( dialogName == 'link' )
		{
			var targetTab = dialogDefinition.getContents('target');
			
			var targetField = targetTab.get('linkTargetType');
			
			targetField['items'].splice(0, 3);
			targetField['items'].splice(3, 1);
			targetField['items'].splice(1, 1);
			
			var targetField = targetTab.get( 'linkTargetType' );
			
			var infoTab = dialogDefinition.getContents( 'info' );
			
			infoTab.remove( 'linkType' );
			infoTab.remove( 'browse' );
			infoTab.remove( 'protocol' );
			
			var urlField = infoTab.get( 'url' );
			urlField['default'] = 'www.example.com';
			
			dialogDefinition.height =50;
			dialogDefinition.removeContents( 'advanced' );
			dialogDefinition.removeContents( 'upload' );
			dialogDefinition.onFocus = function()
			{
				var urlField = this.getContentElement( 'info', 'url' );
				urlField.select();
			};
		}
		if ( dialogName == 'image' )
		{
			dialogDefinition.width =350;
			dialogDefinition.removeContents( 'advanced' );
			dialogDefinition.removeContents( 'Link' );
			dialogDefinition.height =305;
		}
		if ( dialogName == 'find' )
		{
		
			dialogDefinition.width =415;
			dialogDefinition.height =90;
		}
	});