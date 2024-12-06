# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext
_ = gettext.gettext

wx.Main = 6000

###########################################################################
## Class MainWindow
###########################################################################

class MainWindow ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.Main, title = _(u"Conway's game of life"), pos = wx.DefaultPosition, size = wx.Size( 813,585 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        self.m_menubar4 = wx.MenuBar( 0 )
        self.m_file_menu = wx.Menu()
        self.m_file_load = wx.MenuItem( self.m_file_menu, wx.ID_ANY, _(u"Open\tCtrl+O"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_file_menu.Append( self.m_file_load )

        self.m_file_save = wx.MenuItem( self.m_file_menu, wx.ID_ANY, _(u"Save\tCtrl+S"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_file_menu.Append( self.m_file_save )

        self.m_file_menu.AppendSeparator()

        self.m_file_settings = wx.MenuItem( self.m_file_menu, wx.ID_ANY, _(u"Settings\tCtrl+A"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_file_menu.Append( self.m_file_settings )

        self.m_file_menu.AppendSeparator()

        self.m_file_quit = wx.MenuItem( self.m_file_menu, wx.ID_ANY, _(u"Quit\tCtrl+Q"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_file_menu.Append( self.m_file_quit )

        self.m_menubar4.Append( self.m_file_menu, _(u"File") )

        self.m_sim_menu = wx.Menu()
        self.m_sim_run = wx.MenuItem( self.m_sim_menu, wx.ID_ANY, _(u"Run\tCtrl+R"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_sim_menu.Append( self.m_sim_run )

        self.m_sim_pause = wx.MenuItem( self.m_sim_menu, wx.ID_ANY, _(u"Pause\tCtrl+P"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_sim_menu.Append( self.m_sim_pause )
        self.m_sim_pause.Enable( False )

        self.m_sim_step = wx.MenuItem( self.m_sim_menu, wx.ID_ANY, _(u"Single Step\tCtrl+N"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_sim_menu.Append( self.m_sim_step )

        self.m_sim_back = wx.MenuItem( self.m_sim_menu, wx.ID_ANY, _(u"Backwars Step\tCtrl+B"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_sim_menu.Append( self.m_sim_back )

        self.m_sim_random_fill = wx.MenuItem( self.m_sim_menu, wx.ID_ANY, _(u"Random Fill\tCtrl+F"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_sim_menu.Append( self.m_sim_random_fill )

        self.m_sim_continue = wx.MenuItem( self.m_sim_menu, wx.ID_ANY, _(u"Continue\tCtrl+C"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_sim_menu.Append( self.m_sim_continue )
        self.m_sim_continue.Enable( False )

        self.m_sim_menu.AppendSeparator()

        self.m_sim_faster = wx.MenuItem( self.m_sim_menu, wx.ID_ANY, _(u"Faster\tCtrl++"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_sim_menu.Append( self.m_sim_faster )

        self.m_sim_slower = wx.MenuItem( self.m_sim_menu, wx.ID_ANY, _(u"Slower\tCtrl+-"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_sim_menu.Append( self.m_sim_slower )

        self.m_menubar4.Append( self.m_sim_menu, _(u"Simulation") )

        self.m_zoom_menu = wx.Menu()
        self.m_zoom_auto = wx.MenuItem( self.m_zoom_menu, wx.ID_ANY, _(u"Auto\tCtrl+Z"), wx.EmptyString, wx.ITEM_CHECK )
        self.m_zoom_menu.Append( self.m_zoom_auto )
        self.m_zoom_auto.Check( True )

        self.m_zoom_in = wx.MenuItem( self.m_zoom_menu, wx.ID_ANY, _(u"In\tCtrl+>"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_zoom_menu.Append( self.m_zoom_in )

        self.m_zoom_out = wx.MenuItem( self.m_zoom_menu, wx.ID_ANY, _(u"Out\tCtrl+<"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_zoom_menu.Append( self.m_zoom_out )

        self.m_menubar4.Append( self.m_zoom_menu, _(u"Zoom") )

        self.SetMenuBar( self.m_menubar4 )

        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        self.m_grid = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
        self.m_grid.SetScrollRate( 5, 5 )
        bSizer2.Add( self.m_grid, 1, wx.EXPAND |wx.ALL, 5 )


        self.SetSizer( bSizer2 )
        self.Layout()
        self.m_statusBar1 = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )

        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind( wx.EVT_MENU, self.OnOpen, id = self.m_file_load.GetId() )
        self.Bind( wx.EVT_MENU, self.OnSave, id = self.m_file_save.GetId() )
        self.Bind( wx.EVT_MENU, self.OnSettings, id = self.m_file_settings.GetId() )
        self.Bind( wx.EVT_MENU, self.OnClose, id = self.m_file_quit.GetId() )
        self.Bind( wx.EVT_MENU, self.RunSim, id = self.m_sim_run.GetId() )
        self.Bind( wx.EVT_MENU, self.PauseSim, id = self.m_sim_pause.GetId() )
        self.Bind( wx.EVT_MENU, self.TakeSingleStep, id = self.m_sim_step.GetId() )
        self.Bind( wx.EVT_MENU, self.StepBack, id = self.m_sim_back.GetId() )
        self.Bind( wx.EVT_MENU, self.RandomFill, id = self.m_sim_random_fill.GetId() )
        self.Bind( wx.EVT_MENU, self.OnContinue, id = self.m_sim_continue.GetId() )
        self.Bind( wx.EVT_MENU, self.OnFaster, id = self.m_sim_faster.GetId() )
        self.Bind( wx.EVT_MENU, self.OnSlower, id = self.m_sim_slower.GetId() )
        self.Bind( wx.EVT_MENU, self.ToggleZoomAuto, id = self.m_zoom_auto.GetId() )
        self.Bind( wx.EVT_MENU, self.ZoomIn, id = self.m_zoom_in.GetId() )
        self.Bind( wx.EVT_MENU, self.ZoomOut, id = self.m_zoom_out.GetId() )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def OnOpen( self, event ):
        event.Skip()

    def OnSave( self, event ):
        event.Skip()

    def OnSettings( self, event ):
        event.Skip()

    def OnClose( self, event ):
        event.Skip()

    def RunSim( self, event ):
        event.Skip()

    def PauseSim( self, event ):
        event.Skip()

    def TakeSingleStep( self, event ):
        event.Skip()

    def StepBack( self, event ):
        event.Skip()

    def RandomFill( self, event ):
        event.Skip()

    def OnContinue( self, event ):
        event.Skip()

    def OnFaster( self, event ):
        event.Skip()

    def OnSlower( self, event ):
        event.Skip()

    def ToggleZoomAuto( self, event ):
        event.Skip()

    def ZoomIn( self, event ):
        event.Skip()

    def ZoomOut( self, event ):
        event.Skip()


###########################################################################
## Class SettingsDialog
###########################################################################

class SettingsDialog ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer1.SetFlexibleDirection( wx.BOTH )
        fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, _(u"Fill Width"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )

        fgSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )

        self.m_textCtrl_width = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer1.Add( self.m_textCtrl_width, 0, wx.ALL, 5 )

        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, _(u"Fill Height"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )

        fgSizer1.Add( self.m_staticText2, 0, wx.ALL, 5 )

        self.m_textCtrl_height = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer1.Add( self.m_textCtrl_height, 0, wx.ALL, 5 )

        self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, _(u"Fill Factor"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )

        fgSizer1.Add( self.m_staticText3, 0, wx.ALL, 5 )

        self.m_textCtrl_fill = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer1.Add( self.m_textCtrl_fill, 0, wx.ALL, 5 )

        self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, _(u"Stagnation Window"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText6.Wrap( -1 )

        fgSizer1.Add( self.m_staticText6, 0, wx.ALL, 5 )

        self.m_textCtrl_stagnation = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer1.Add( self.m_textCtrl_stagnation, 0, wx.ALL, 5 )

        self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, _(u"Similarity threshold"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )

        fgSizer1.Add( self.m_staticText7, 0, wx.ALL, 5 )

        self.m_textCtrl_similarity = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer1.Add( self.m_textCtrl_similarity, 0, wx.ALL, 5 )

        self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )

        fgSizer1.Add( self.m_staticText5, 0, wx.ALL, 5 )

        self.m_setting_save = wx.Button( self, wx.ID_ANY, _(u"Save"), wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer1.Add( self.m_setting_save, 0, wx.ALL, 5 )


        self.SetSizer( fgSizer1 )
        self.Layout()
        fgSizer1.Fit( self )

        self.Centre( wx.BOTH )

        # Connect Events
        self.m_setting_save.Bind( wx.EVT_BUTTON, self.OnSave )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def OnSave( self, event ):
        event.Skip()


###########################################################################
## Class AlertDialog
###########################################################################

class AlertDialog ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        fgSizer2 = wx.FlexGridSizer( 0, 1, 0, 0 )
        fgSizer2.SetFlexibleDirection( wx.VERTICAL )
        fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_text_alert = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_text_alert.Wrap( -1 )

        fgSizer2.Add( self.m_text_alert, 0, wx.ALL, 5 )

        self.m_button_ok = wx.Button( self, wx.ID_ANY, _(u"Ok"), wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer2.Add( self.m_button_ok, 0, wx.ALL, 5 )


        self.SetSizer( fgSizer2 )
        self.Layout()
        fgSizer2.Fit( self )

        self.Centre( wx.BOTH )

        # Connect Events
        self.m_button_ok.Bind( wx.EVT_BUTTON, self.OnClose )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def OnClose( self, event ):
        event.Skip()


