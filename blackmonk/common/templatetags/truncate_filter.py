from django import template  
register = template.Library()  
    
@register.filter("truncate_chars")  
def truncate_chars(value, max_length):
    
    if value:
        if len(value) > max_length:
            truncd_val = value[:max_length]  
            try:
                if value[max_length+1] != " ":
                    truncd_val = truncd_val[:truncd_val.rfind(" ")]  
                return  truncd_val + "..."  
            except:pass
        return value
    else:
        return ''  