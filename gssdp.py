import functools
import gi
gi.require_version( 'GSSDP', '1.0' )
from gi.repository import GSSDP

class Discover( object ):
  __slots__ = '__network', '__msgtype', '__client', '__browser', '__callback'

  def __init__( self, cb, network = '0.0.0.0', msgtype = 'ssdp:all' ):
    super( Discover, self ).__init__( )

    self.__callback = cb
    self.__network = network
    self.__msgtype = msgtype
    self.__client = GSSDP.Client.new( )

    self.__client.set_network( network )
    self.__browser = GSSDP.ResourceBrowser.new( self.__client, msgtype )

    self.__browser.connect( 'resource-available', functools.partial( Discover.__available, self ) )
    self.__browser.connect( 'resource-unavailable', functools.partial( Discover.__unavailable, self ) )

  def __available( self, browser, msn, locations ):
    self.__callback( self, msn, locations )

  def __unavailable( self, browser, msn ):
    self.__callback( self, msn, None )

  def start( self ):
    self.__browser.set_active( True )

  def stop( self ):
    self.__browser.set_active( False )
