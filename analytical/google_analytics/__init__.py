"""
====================================
Google Analytics -- traffic analysis
====================================

`Google Analytics`_ is the well-known web analytics service from
Google.  The product is aimed more at marketers than webmasters or
technologists, supporting integration with AdWords and other e-commence
features.

.. _`Google Analytics`: http://www.google.com/analytics/


.. google-analytics-installation:

Installation
============

You only need to do perform these steps if you are not using the
generic :ttag:`analytical.*` tags.  If you are, skip to
:ref:`google-analytics-configuration`.

In order to use the template tag, you need to add
:mod:`analytical.google_analytics` to the installed applications list in
the project :file:`settings.py` file::

    INSTALLED_APPS = [
        ...
        'analytical.google_analytics',
        ...
    ]

The Google Analytics tracking code is inserted into templates using a
template tag.  Load the :mod:`google_analytics` template tag library and
insert the :ttag:`google_analytics` tag.  Because every page that you
want to track must have the tag, it is useful to add it to your base
template.  Insert the tag at the bottom of the HTML head::

    {% load google_analytics %}
    <html>
    <head>
    ...
    {% google_analytics %}
    </head>
    ...


.. _google-analytics-configuration:

Configuration
=============

Before you can use the Google Analytics integration, you must first set
your website property ID.  You can also add custom segments for Google
Analytics to track.


.. _google-analytics-property-id:

Setting the property ID
-----------------------

Every website you track with Google Analytics gets its own property ID,
and the :ttag:`google_analytics` tag will include it in the rendered
Javascript code.  You can find the web property ID on the overview page
of your account.  Set :const:`GOOGLE_ANALYTICS_PROPERTY_ID` in the
project :file:`settings.py` file::

    GOOGLE_ANALYTICS_PROPERTY_ID = 'UA-XXXXXX-X'

If you do not set a property ID, the tracking code will not be rendered.


.. _google-analytics-internal-ips:

Internal IP addresses
---------------------

Usually you do not want to track clicks from your development or
internal IP addresses.  By default, if the tags detect that the client
comes from any address in the :const:`INTERNAL_IPS` setting, the
tracking code is commented out.  See :const:`ANALYTICAL_INTERNAL_IPS`
for important information about detecting the visitor IP address.


.. _google-analytics-custom-variables:

Custom variables
----------------

As described in the Google Analytics `custom variables`_ documentation
page, you can define custom segments.  Using template context variables
``google_analytics_var1`` through ``google_analytics_var5``, you can let
the :ttag:`google_analytics` tag pass custom variables to Google
Analytics automatically.  You can set the context variables in your view
when your render a template containing the tracking code::

    context = RequestContext({'google_analytics_var1': ('gender', 'female'),
                              'google_analytics_var2': ('visit', '1', SCOPE_SESSION)})
    return some_template.render(context)

The value of the context variable is a tuple *(name, value, [scope])*.
The scope parameter is one of the
:const:`analytical.google_analytics.SCOPE_*` constants:

=================  ======  =============================================
Constant           Value   Description
=================  ======  =============================================
``SCOPE_VISITOR``    1     Distinguishes categories of visitors across
                           multiple sessions.
``SCOPE_SESSION``    2     Ddistinguishes different visitor experiences
                           across sessions.
``SCOPE_PAGE``       3     Defines page-level activity.
=================  ======  =============================================

The default scope is :const:`~analytical.google_analytics.SCOPE_PAGE`.

You may want to set custom variables in a context processor that you add
to the :data:`TEMPLATE_CONTEXT_PROCESSORS` list in :file:`settings.py`::

    def google_analytics_segment_language(request):
        try:
            return {'google_analytics_var3': request.LANGUAGE_CODE}
        except AttributeError:
            return {}

Just remember that if you set the same context variable in the
:class:`~django.template.context.RequestContext` constructor and in a
context processor, the latter clobbers the former.

.. _`custom variables`: http://code.google.com/apis/analytics/docs/tracking/gaTrackingCustomVariables.html

"""

SCOPE_VISITOR = 1
SCOPE_SESSION = 2
SCOPE_PAGE = 3

google_analytics_service = {
    'head_bottom': 'analytical.google_analytics.templatetags.google_analytics'
            '.GoogleAnalyticsNode',
}