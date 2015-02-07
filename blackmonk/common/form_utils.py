from django import forms
from django.utils.safestring import mark_safe

class HorizCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def __init__(self, css_class=None, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.css_class = css_class

    def render(self, *args, **kwargs): 
        output = super(HorizCheckboxSelectMultiple, self).render(*args,**kwargs)
        return mark_safe(output.replace(u'<ul>', u'').replace(u'</ul>', u'').replace(u'<li>', u'<span class="%s">' % self.css_class).replace(u'</li>', u'</span>').replace(u'<input', u'<span class="cform-checkbox-container"><input').replace(u' /> ', u' /><span class="cform-checkbox-element"></span></span>'))#

class HorizDivCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def __init__(self, css_class=None, **kwargs):
        super(self.__class__, self).__init__(**kwargs)
        self.css_class = css_class

    def render(self, *args, **kwargs): 
        output = super(HorizDivCheckboxSelectMultiple, self).render(*args,**kwargs)
        return mark_safe(output.replace(u'<ul>', u'').replace(u'</ul>', u'').replace(u'<li>', u'<div class="%s">' % self.css_class).replace(u'</li>', u'</div>').replace(u' <label>', u' <label class="checkbox inline fW-nRmL">'))#


class HorizRadioRenderer(forms.RadioSelect.renderer):
    """ this overrides widget method to put radio buttons horizontally
        instead of vertically.
    """
    def render(self):
            """Outputs radios"""
            return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))