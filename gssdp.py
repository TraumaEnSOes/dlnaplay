import gi
gi.require_version( 'GSSDP', '1.0' )
from gi.repository import GSSDP

__callback = None
__network = None
__msgType = None
__client = None
__browser = None

def start( cb, network = '0.0.0.0', msgtype = 'ssdp:all' ):
  global __client, __browser, __callback
  # Si ya hay un descubrimiento en marcha, no hacemos nada.
  if __client != None:
    if cb == __callback:
      return
    else:
      raise( 'Ya hay un descubrimiento en marcha' )
  
  __callback = cb
  __client = GSSDP.Client.new( )
  __client.set_network( network )

  __browser = GSSDP.ResourceBrowser.new( __client, msgtype )
  __browser.connect( 'resource-available', __available )
  __browser.connect( 'resource-unavailable', __unavailable )
  __browser.set_active( True )

def stop( ):
  global __client, __browser

  if __client == None:
    return

  __browser.set_active( False )
  __browser = None
  __client = None

def started( ):
  return not ( __client == None )

def __available( notUsed, msn, locations ):
  __callback( msn, locations )

def __unavailable( notUsed, msn ):
  __callback( msn, None )
