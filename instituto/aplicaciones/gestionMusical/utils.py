from io import StringIO
from django.http import HttpResponse
from django.template.loader import get_template
from datetime import datetime
from xhtml2pdf import pisa
from django.template import Context

def render_to_pdf( template_src, context_dict):
    now = datetime.now()
    filename = now.strftime('%Y-%m-%d') + '.pdf'
    template = get_template(template_src)
    context = context_dict
    html  = template.render(context)
    result = StringIO()

    pdf = pisa.pisaDocument(StringIO(html.encode("UTF-8")),result, path=path)

    if not pdf.err:
      response = HttpResponse(result.getvalue(), mimetype='application/pdf')
      response['Content-Disposition'] = 'attachment; filename="'+filename+'"'
      return response
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

def get_full_path_x(request):
    full_path = ('http', ('', 's')[request.is_secure()], '://',
    request.META['HTTP_HOST'], request.path)
    return ''.join(full_path) 