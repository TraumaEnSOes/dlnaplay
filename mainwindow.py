import gi
import subprocess

import gssdp

gi.require_version( 'Gtk', '3.0' )
from gi.repository import Gtk
from gi.repository import GObject

class MainWindow( object ):
  @staticmethod
  def connect( widget, signals ):
    for k, v in signals.items( ):
      widget.connect( k, v )

    return widget;

  @staticmethod
  def getAndConnect( builder, id, signals ):
    return MainWindow.connect( builder.get_object( id ), signals )

  def __init__( self ):
    super( MainWindow, self ).__init__( )

    builder = Gtk.Builder( ).new_from_file( 'main.glade' )

    self.__window = MainWindow.getAndConnect( builder, 'MainWindow', {
      'destroy': Gtk.main_quit,
      'delete-event': self.__onClose
    } )
    self.__server = MainWindow.getAndConnect( builder, 'Server', {

    } )
    self.__refresh = MainWindow.getAndConnect( builder, 'Refresh', {
      'clicked': self.__onRefresh
    } )
    self.__media = MainWindow.getAndConnect( builder, 'Media', {
    } )
    self.__order = MainWindow.getAndConnect( builder, 'Order', {

    } )
    self.__down = MainWindow.getAndConnect( builder, 'Down', {

    } )
    self.__play = MainWindow.getAndConnect( builder, 'Play', {
      'clicked': self.__onPlay
    } )

    self.__closing = False
    self.__window.show_all( )

    gssdp.start( self.__onGSSDP )

  def __onPlay( self, button ):
    pass
    #Popen( [ self.__order.get_active_text( ) ], shell = True, stdin = None, stdout = None, stderr = None, close_fds = True )

  def showAll( self ):
    self.__window.show_all( )

  def __onGSSDP( self, msn, locations ):
    if self.__closing:
      return

    if locations == None:
      print( 'PERDIDO', msn )
    else:
      print( 'ENCONTRADO', msn )
      for v in locations:
        print( v )

  def __onClose( self, NotUsed1, NotUsed2 ):
    self.__closing = True
    gssdp.stop( )
    return False

  def __onRefresh( self, NotUsed ):
    gssdp.stop( );
    GObject.timeout_add( 500, gssdp.start( self.onGSSDP ) )
