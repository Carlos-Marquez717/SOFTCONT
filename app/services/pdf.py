import logging
from io import BytesIO

from django.template.loader import get_template
from xhtml2pdf import pisa


def render_template_to_pdf_bytes(template_src, context=None, page_size=(842, 595)):
    context = context or {}
    template = get_template(template_src)
    html = template.render(context)
    result = BytesIO()

    pisa_status = pisa.CreatePDF(
        BytesIO(html.encode("UTF-8")),
        dest=result,
        page_size=page_size,
    )

    if pisa_status.err:
        logging.error("Error generating PDF from template %s: %s", template_src, pisa_status.err)
        return None

    return result.getvalue()
