from django import template
register = template.Library()

def do_ifmodulo(parser, token, negate):
  bits = list(token.split_contents())
  if not len(bits) in [3, 4]:
    raise template.TemplateSyntaxError, "%r takes two or three arguments" % bits[0]
  
  end_tag = 'end' + bits[0]
  nodelist_true = parser.parse(('else', end_tag))
  token = parser.next_token()
  if token.contents == 'else':
    nodelist_false = parser.parse((end_tag,))
    parser.delete_first_token()
  else:
    nodelist_false = template.NodeList()
  if len(bits) == 3:
    bits.extend([None])
  return IfModuloNode(bits[1], bits[2], bits[3], nodelist_true, nodelist_false, negate)
  
def ifmodulo(parser, token):
  return do_ifmodulo(parser, token, False)
  
def ifnotmodulo(parser, token):
  return do_ifmodulo(parser, token, True)
  
register.tag('ifmodulo', ifmodulo)
register.tag('ifnotmodulo', ifnotmodulo)

class IfModuloNode(template.Node):
  def __init__(self, var1, var2, var3, nodelist_true, nodelist_false, negate):
    self.var1, self.var2, self.var3 = var1, var2, var3
    self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
    self.negate = negate
    
  def __repr__(self):
    return "<IfModuloNode>"

  def render(self, context):
    try:
      val1 = template.resolve_variable(self.var1, context)
    except template.VariableDoesNotExist:
      val1 = None
    try:
      val2 = template.resolve_variable(self.var2, context)
    except template.VariableDoesNotExist:
      val2 = None
    if self.var3 <> None:
      try:
        val3 = template.resolve_variable(self.var3, context)
      except template.VariableDoesNotExist:
        val3 = None
    else:
      val3 = None
    
    if val3 == None:
      if (not self.negate and val1 % val2) or (self.negate and not val1 % val2):
        return self.nodelist_true.render(context)
      else:
        return self.nodelist_false.render(context)
    else:
      if (not self.negate and val1 % val2 == val3) or (self.negate and val1 % val2 <> val3):
        return self.nodelist_true.render(context)
      else:
        return self.nodelist_false.render(context)
      