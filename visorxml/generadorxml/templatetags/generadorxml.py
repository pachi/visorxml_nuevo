#!/usr/bin/env python
#encoding:utf-8
#
# Copyright (c) 2015 Ministerio de Fomento
#                    Instituto de Ciencias de la Construcción Eduardo Torroja (IETcc-CSIC)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import base64

from django import template

from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def escalasvg(letra, value = None):
    """Devuelve imagen de la escala y su calificación como SVG inline"""

    SVGTEXT = """<svg xmlns='http://www.w3.org/2000/svg' width="185" height="120">
<g id="layer1" stroke="none">
<path d="m 184,{ypos:d} -57,0 -11,7 11,7 57,0 z" fill="#black" />
<text x="180" y="{ypostxt:d}" id="calif" style="font-size:11px;font-weight:bold;text-align:end;text-anchor:end;fill:white;font-family:Arial">
{value}{calif}</text>

<path d="m 0,0 67,0 7,7 -7,7 -67,0 z" fill="#00a651" />
<path d="m 0,17 74,0 7,7 -7,7 -74,0 z" fill="#4cb847" />
<path d="m 0,34 81,0 7,7 -7,7 -81,0 z" fill="#bfd630" />
<path d="m 0,51 88,0 7,7 -7,7 -88,0 z" fill="#fff100" />
<path d="m 0,68 95,0 7,7 -7,7 -95,0 z" fill="#feb811" />
<path d="m 0,85 102,0 7,7 -7,7 -102,0 z" fill="#f36f23" />
<path d="m 0,102 109,0 7,7 -7,7 -109,0 z" fill="#ee1c25" />

<text x="55" y="11" style="font-size:12px;font-weight:bold;fill:white;font-family:Arial">A</text>
<text x="62" y="28" style="font-size:12px;font-weight:bold;fill:white;font-family:Arial">B</text>
<text x="69" y="45" style="font-size:12px;font-weight:bold;fill:white;font-family:Arial">C</text>
<text x="76" y="62" style="font-size:12px;font-weight:bold;fill:white;font-family:Arial">D</text>
<text x="83" y="79" style="font-size:12px;font-weight:bold;fill:white;font-family:Arial">E</text>
<text x="90" y="96" style="font-size:12px;font-weight:bold;fill:white;font-family:Arial">F</text>
<text x="97" y="113" style="font-size:12px;font-weight:bold;fill:white;font-family:Arial">G</text>
</g>
</svg>"""

    SVGERROR = """<svg xmlns='http://www.w3.org/2000/svg' width="175" height="120">
<g id="layer1" stroke="none">
<path d="m 2 2 173 0 0 118 -173 0 z" stroke="gray" fill="none" />
<path d="m 2 2 173 118 M 0 118 l 178 -118" stroke="gray" fill="none" />
<text x="85" y="60" id="calif" style="font-size:12px;font-weight:bold;text-align:center;text-anchor:middle;fill:black;font-family:Arial">Sin valor para calificación</text>
</g>
</svg>
"""
    try:

        ypos = 17 * {
            'A': 0,
            'B': 1,
            'C': 2,
            'D': 3,
            'E': 4,
            'F': 5,
            'G': 6
        }[letra]
        svgdata = SVGTEXT.format(ypos=ypos,
                                 ypostxt=ypos + 11,
                                 calif=letra,
                                 value=value or ""
                                 )
    except:
        svgdata = SVGERROR

    encoded_string = base64.b64encode(svgdata.encode('utf-8'))
    return "data:image/svg+xml;charset=utf-8;base64,{}".format(encoded_string.decode())

ALERTINT = 9999999999
ALERT = ALERTINT / 100
ALERT_SPAN = mark_safe("<span class='alert'>-</span>")

@register.filter(is_safe=True)
def asnum(value):
    "Devuelve un valor numérico con dos decimales"
    if ((not value) and (value != 0)):
        return ''
    try:
        val = float(value)
        res = '{:0.2f}'.format(val).replace('.', ',') if val < ALERT else ALERT_SPAN
    except:
        res = ALERT_SPAN
    return res


TIPOS_RESIDENCIALES = "ViviendaUnifamiliar|BloqueDeViviendaCompleto|ViviendaIndividualEnBloque".split("|")
@register.simple_tag(takes_context=True)
def get_uso(context):
    try:
        report = context['report']
        tipo = report.data.IdentificacionEdificio.TipoDeEdificio
        context["es_vivienda"] = tipo in TIPOS_RESIDENCIALES
        context["es_local"] = tipo == "LocalUsoTerciario"
        context["es_bloque"] = "Bloque" in tipo
        context["es_bloque_cpl"] =  "BloqueDeViviendaCompleto" == tipo

    except:
        pass

    return ""

@register.simple_tag(takes_context=True)
def get_alcance(context):
    try:
        report = context['report']
        context["es_nuevo"] = "Nuevo" in report.data.IdentificacionEdificio.AlcanceInformacionXML 
    except:
        pass

    return ""

