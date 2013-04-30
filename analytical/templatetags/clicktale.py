"""
Clickmap template tags and filters.
"""

from __future__ import absolute_import

import re

from django.template import Library, Node, TemplateSyntaxError
from django.utils import simplejson

from analytical.utils import get_identity, is_internal_ip, disable_html, get_required_setting


CLICKTALE_PROJECT_ID_RE = re.compile(r'^\d+$')
TRACKING_CODE = """
    <!-- ClickTale Bottom part -->
      <div id="ClickTaleDiv" style="display: none;"></div>
      <script type="text/javascript">
          if(document.location.protocol!='https:')
              document.write(unescape("%3Cscript%20src='http://s.clicktale.net/WRe0.js'%20type='text/javascript'%3E%3C/script%3E"));
      </script>
      <script type="text/javascript">
          if(typeof ClickTale=='function') ClickTale(%(project_id),%(recording_ratio),"www08");
      </script>
      <!-- ClickTale end of Bottom part -->
"""

register = Library()


@register.tag
def clicktale(parser, token):
    """
    Clicktale tracker template tag.

    Renders Javascript code to track page visits.  You must supply
    your clicktale project ID (as a string) in the ``CLICKTALE_PROJECT_ID``
    setting.
    """
    bits = token.split_contents()
    if len(bits) > 1:
        raise TemplateSyntaxError("'%s' takes no arguments" % bits[0])
    return ClicktaleNode()


class ClicktaleNode(Node):
    def __init__(self):
        self.tracker_id = get_required_setting('CLICKTALE_PROJECT_ID',
                CLICKTALE_PROJECT_ID_RE,
                "must be a (string containing) a number")
        self.recording_ratio = get_required_setting('CLICKTALE_RECORDING_RATIO',
                CLICKTALE_PROJECT_ID_RE,
                "must be a (string containing) a number")
        self

    def render(self, context):
        html = TRACKING_CODE % {'portal_id': self.portal_id,
                'domain': self.domain}
        if is_internal_ip(context, 'CLICKTALE'):
            html = disable_html(html, 'Clicktale')
        return html


def contribute_to_analytical(add_node):
    ClicktaleNode()  # ensure properly configured
    add_node('body_bottom', ClicktaleNode)
