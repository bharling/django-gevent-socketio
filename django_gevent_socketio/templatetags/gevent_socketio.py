from django import template
register = template.Library()
from django.contrib.staticfiles.storage import staticfiles_storage

@register.simple_tag
def socketio_js(include_flash=True):
    script_path = staticfiles_storage.url('js/socket.io.js')
    swf_script = ""
    if include_flash:
        swf_path = staticfiles_storage.url('flashsocket/WebSocketMain.swf')
        swf_script = '<script type="text/javascript">WEB_SOCKET_SWF_LOCATION="%s";</script>' % ( swf_path )
    return '<script type="text/javascript" src="%s"></script>\n%s' % ( script_path, swf_script )