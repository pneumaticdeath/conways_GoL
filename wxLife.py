#!/usr/bin/env python3

import life
import math
import os
import random
import time
import wx
import wxLifeUI


class MainWindow(wxLifeUI.MainWindow):
    _zoom_factor = 1.1
    _speed_factor = 1.5
    _shift_factor = 0.1

    def __init__(self, parent):
        wxLifeUI.MainWindow.__init__(self, parent)
        self._board_size = (20, 20)
        self._fill_factor = 40
        self._delay_time_ms = 100
        self._history_limit = -1
        self._single_step = False
        self._stagnated = False
        self._stagnation = 0
        self._stagnation_window = 10
        self._similarity_threshold = 0.95
        self._last_step_time = 0
        self._background = wx.Brush('black')
        self._paused_brush = wx.Brush(wx.Colour(31, 31, 255))
        self._running_brush = wx.Brush('green')
        self._stagnated_brush = wx.Brush('red')
        self._edit_brush = wx.Brush('yellow')
        self._directory = 'examples'
        self._filename = ''
        self._save_format = life.FMT_LIFE
        self._timer = wx.Timer()
        self.initializeGame(set())
        self.m_grid.Bind(wx.EVT_LEFT_DOWN, self.OnLeftClick)
        self.m_grid.Bind(wx.EVT_PAINT, self.OnPaint)
        self._timer.Bind(wx.EVT_TIMER, self.OnTimer)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.m_grid.Bind(wx.EVT_KEY_DOWN, self.OnKeypress)

    def initializeGame(self, cells):
        self.clearStagnation()
        self._game = life.Life(cells, self._history_limit)
        self.resetDisplayBox()

    def resetDisplayBox(self):
        self._box_min_x, self._box_min_y, self._box_max_x, self._box_max_y = self._game.getBoundingBox()
        if self._box_min_x is None:
            self._box_min_x = 0
            self._box_min_y = 0
            self._box_max_x = self._board_size[0] - 1
            self._box_max_y = self._board_size[1] - 1
        self.Refresh()

    def getBrush(self):
        if self.m_sim_edit.IsChecked():
            return self._edit_brush
        elif self._stagnated:
            return self._stagnated_brush
        elif self.m_sim_play_pause.IsChecked():
            return self._running_brush
        else:
            return self._paused_brush

    def getHistoryLimit(self):
        return self._history_limit

    def setHistoryLimit(self, limit):
        self._history_limit = limit
        self._game.setHistoryLimit(limit)

    def RandomFill(self, event):
        self.clearStagnation()
        self._filename = ''
        newCells = set()
        for y in range(self._board_size[1]):
            for x in range(self._board_size[0]):
                if random.uniform(0, 100) < self._fill_factor:
                    newCells.add((x, y))
        self.initializeGame(newCells)

    def OnClear(self, event):
        self._filename = ''
        self._game.clear()
        self.Refresh()
        event.Skip()

    def OnPlayPause(self, event):
        if self.m_sim_play_pause.IsChecked():
            self.RunSim()
        else:
            self.PauseSim()

    def RunSim(self):
        self.editMode(False)
        if self._stagnated:
            self.clearStagnation()
        self._timer.Start(int(self._delay_time_ms))
        self.m_sim_play_pause.Check(True)
        self.Refresh()

    def PauseSim(self):
        self._timer.Stop()
        self.m_sim_play_pause.Check(False)
        self.Refresh()

    def OnTimer(self, event):
        self.takeStep()

    def TakeSingleStep(self, event=None):
        self.PauseSim()
        self.takeStep()

    def takeStep(self):
        time_before = time.time()
        self._game.step()
        time_after = time.time()
        self._last_step_time = time_after - time_before
        if self.m_zoom_auto.IsChecked():
            self.AutoZoom()
        self.checkStagnation()
        self.Refresh()

    def StepBack(self, event=None):
        self.PauseSim()
        self.clearStagnation()
        if not self._game.backwardsStep():
            self.setStatus('Can\'t go back any further')
        self.Refresh()

    def checkStagnation(self):
        stagnating = False
        curr_cells = self._game.getLiveCells()
        if not self._stagnated and self.m_sim_stagnation.IsChecked():
            if len(curr_cells) == len(self._game.getHistory()[-1]):
                stagnating = True
                self.setStatus('Stagnating on population at generation {}'.format(self._game.getGeneration()))
            for historical_cells in self._game.getHistory()[-self._stagnation_window:]:
                if curr_cells == historical_cells:
                    stagnating = True
                    self._stagnated = True
                    self.setStatus('Stagnated on loop at generation {}'.format(self._game.getGeneration()))
                    break
                elif len(curr_cells.intersection(historical_cells)) > len(curr_cells) * self._similarity_threshold:
                    stagnating = True
                    self.setStatus('Stagnating on similarity at generation {}'.format(self._game.getGeneration()))
                    # break
            if stagnating:
                self._stagnation += 1
                if self._stagnation >= self._stagnation_window:
                    self._stagnated = True
                    self.setStatus('Stagnated at generation {}'.format(self._game.getGeneration() - self._stagnation))
            else:
                self._stagnation = 0

        if self._stagnated:
            self.PauseSim()

    def clearStagnation(self):
        self._stagnated = False
        self._stagnation = 0

    def OnFaster(self, event):
        self._delay_time_ms = max(self._delay_time_ms / self._speed_factor, 1)
        if self._timer.IsRunning():
            self._timer.Start(int(self._delay_time_ms))

    def OnSlower(self, event):
        self._delay_time_ms = self._delay_time_ms * self._speed_factor
        if self._timer.IsRunning():
            self._timer.Start(int(self._delay_time_ms))

    def AutoZoom(self):
        min_x, min_y, max_x, max_y = self._game.getBoundingBox()

        if min_x is None:
            return

        if min_x < self._box_min_x:
            self._box_min_x = min_x
        if min_y < self._box_min_y:
            self._box_min_y = min_y
        if max_x > self._box_max_x:
            self._box_max_x = max_x
        if max_y > self._box_max_y:
            self._box_max_y = max_y

    def OnOpen(self, event):
        self.PauseSim()
        self.clearStagnation()
        fod = wx.FileDialog(self, "Choose a Life file",
                            self._directory, '', '*', wx.FD_OPEN)
        if fod.ShowModal() == wx.ID_OK:
            self._filename = fod.GetFilename()
            self._directory = fod.GetDirectory()
            self._game.load(os.path.join(self._directory, self._filename))
            self.resetDisplayBox()
        fod.Destroy()

    def OnSave(self, event):
        self.PauseSim()
        ext = ''
        if self._save_format == life.FMT_CELLS:
            ext = '.cells'
        elif self._save_format == life.FMT_RLE:
            ext = '.rle'
        elif self._save_format == life.FMT_LIFE:
            ext = '.life'
        save_dialog = wx.FileDialog(self, "Save state", self._directory, '',
                                    f'*{ext}', wx.FD_SAVE)
        if save_dialog.ShowModal() == wx.ID_OK:
            save_filename = save_dialog.GetFilename()
            self._directory = save_dialog.GetDirectory()
            self._game.save(os.path.join(self._directory, save_filename), self._save_format)
        save_dialog.Destroy()

    def OnLeftClick(self, event):
        if self.m_sim_edit.IsChecked():
            print(f'Scale {self._scale} BoxMid ({self._box_mid_x}, {self._box_mid_y}) DispMid ({self._display_mid_x}, {self._display_mid_y})')
            x_rel_to_center = (event.x - self._display_mid_x)
            y_rel_to_center = (event.y - self._display_mid_y)
            print(f'Rel to center ({x_rel_to_center}, {y_rel_to_center})')
            cell_x = math.floor(self._box_mid_x + x_rel_to_center / self._scale + 0.5)
            cell_y = math.floor(self._box_mid_y + y_rel_to_center / self._scale + 0.5)
            print('Cell ({}, {})'.format(cell_x, cell_y))
            cell = (cell_x, cell_y)
            cells = self._game.getLiveCells()
            if cell in cells:
                cells.remove(cell)
            else:
                cells.add(cell)
        else:
            print('Click while not in edit mode')
        self.Refresh()
        event.Skip()

    def OnPaint(self, event):
        dc = wx.PaintDC(self.m_grid)
        dc.SetBackground(self._background)
        dc.SetBrush(self.getBrush())
        dc.SetPen(wx.Pen(self.getBrush().GetColour()))
        dc.Clear()
        disp_size = dc.GetSize()
        disp_width = disp_size.GetWidth()
        disp_height = disp_size.GetHeight()
        box_width = self._box_max_x - self._box_min_x + 1
        box_height = self._box_max_y - self._box_min_y + 1
        self._scale = min(disp_width / (box_width + 1), disp_height / (box_height + 1))

        self._box_mid_x = (self._box_max_x + self._box_min_x) / 2
        self._box_mid_y = (self._box_max_y + self._box_min_y) / 2

        self._display_mid_x = disp_width / 2
        self._display_mid_y = disp_height / 2

        if self._filename:
            self.SetTitle('"{}"  Generation: {}   Cells: {}  Last step time: {} ms  Cell size {:.3f} px'
                          .format(self._filename,
                                  self._game.getGeneration(),
                                  len(self._game.getLiveCells()),
                                  int(self._last_step_time * 1000 + 0.5),
                                  self._scale))
        else:
            self.SetTitle('Generation: {}   Cells: {}  Last step time {} ms  Cell size {:.3f} px'
                          .format(self._game.getGeneration(),
                                  len(self._game.getLiveCells()),
                                  int(self._last_step_time * 1000 + 0.5),
                                  self._scale))
        pixels = {}
        for cell_x, cell_y in self._game.getLiveCells():
            x = math.floor(self._display_mid_x + self._scale * (cell_x - self._box_mid_x + 0.5))
            y = math.floor(self._display_mid_y + self._scale * (cell_y - self._box_mid_y + 0.5))

            if self._scale <= 2:
                if (x, y) in pixels:
                    pixels[(x, y)] += 1
                else:
                    pixels[(x, y)] = 1
            else:
                point = wx.Point(math.floor(x - self._scale / 2 + 0.5), math.floor(y - self._scale / 2 + 0.5))
                dc.DrawCircle(point, max(1, int(self._scale * 0.45)))

        if self._scale <= 2:
            max_dens = max([d for d in pixels.values()])
            bg_color = dc.GetBackground().GetColour()
            brush_color = self.getBrush().GetColour()
            for pos, d in pixels.items():
                new_color = wx.Colour(int(bg_color.GetRed() * (max_dens - d) / max_dens + brush_color.GetRed() * d / max_dens),
                                      int(bg_color.GetGreen() * (max_dens - d) / max_dens + brush_color.GetGreen() * d / max_dens),
                                      int(bg_color.GetBlue() * (max_dens - d) / max_dens + brush_color.GetBlue() * d / max_dens))
                new_brush = wx.Brush(new_color)
                dc.SetBrush(new_brush)
                dc.DrawCircle(pos[0], pos[1], 1)

    def _scaleRange(self, min_v, max_v, factor):
        mid = (max_v + min_v) / 2.0
        new_min = math.floor(mid - (mid - min_v) * factor)
        new_max = math.ceil(mid + (max_v - mid) * factor)

        if new_min == min_v:
            new_min -= 1 if factor > 1 else -1

        if new_max == max_v:
            new_max += 1 if factor > 1 else -1

        if new_min <= new_max:
            return new_min, new_max
        else:
            return min_v, max_v

    def zoom(self, factor):
        self._box_min_x, self._box_max_x = self._scaleRange(self._box_min_x, self._box_max_x, factor)
        self._box_min_y, self._box_max_y = self._scaleRange(self._box_min_y, self._box_max_y, factor)
        self.Refresh()

    def ZoomIn(self, event=None):
        self.m_zoom_auto.Check(False)
        self.zoom(1 / self._zoom_factor)

    def ZoomOut(self, event=None):
        self.m_zoom_auto.Check(False)
        self.zoom(self._zoom_factor)

    def ToggleZoomAuto(self, event):
        if self.m_zoom_auto.IsChecked():
            self.AutoZoom()
            self.Refresh()

    def OnReframe(self, event):
        event.Skip()
        self.resetDisplayBox()

    def ToggleStagnation(self, event):
        # The checked flag has already been toggled at this point
        if not self.m_sim_stagnation.IsChecked():
            self.clearStagnation()
            self.Refresh()

    def ToggleEditMode(self, event):
        if self.m_sim_edit.IsChecked():
            self.PauseSim()
            self.setStatus('Edit Mode')
        else:
            self.setStatus('Leaving Edit Mode')
        self.Refresh()

    def editMode(self, mode):
        if mode != self.m_sim_edit.IsChecked():
            self.m_sim_edit.Check(mode)
            if mode:
                self.PauseSim()
                self.setStatus('Edit Mode')
            else:
                self.setStatus('Leaving Edit Mode')
            self.Refresh()

    def OnClose(self, event):
        self._timer.Stop()
        self.Destroy()

    def OnKeypress(self, event):
        keycode = event.GetKeyCode()
        if keycode == wx.WXK_RETURN or keycode == wx.WXK_MEDIA_NEXT_TRACK:
            self.TakeSingleStep(event)
        elif keycode == wx.WXK_MEDIA_PLAY_PAUSE:
            if self.m_sim_play_pause.IsChecked():
                self.PauseSim()
            else:
                self.RunSim()
        elif keycode == wx.WXK_MEDIA_PREV_TRACK:
            self.StepBack(event)
        elif keycode == wx.WXK_LEFT:
            self._box_min_x, self._box_max_x = self.shift(self._box_min_x, self._box_max_x, -self._shift_factor)
        elif keycode == wx.WXK_RIGHT:
            self._box_min_x, self._box_max_x = self.shift(self._box_min_x, self._box_max_x, self._shift_factor)
        elif keycode == wx.WXK_UP:
            self._box_min_y, self._box_max_y = self.shift(self._box_min_y, self._box_max_y, -self._shift_factor)
        elif keycode == wx.WXK_DOWN:
            self._box_min_y, self._box_max_y = self.shift(self._box_min_y, self._box_max_y, self._shift_factor)
        self.Refresh()
        event.Skip()

    def shift(self, min_v, max_v, factor):
        spread = max_v - min_v
        amount = max(1, int(spread * abs(factor)))
        if factor > 0:
            return min_v + amount, max_v + amount
        elif factor < 0:
            return min_v - amount, max_v - amount

    def OnSettings(self, event):
        wasRunning = self.m_sim_play_pause.IsChecked()
        if self.m_sim_play_pause.IsChecked():
            self.PauseSim()

        dialog = SettingDialog(self)
        if dialog.ShowModal() == wx.ID_OK:
            self.setStatus("Saving settings")

        if wasRunning:
            self.RunSim()

    def setStatus(self, text):
        self.GetStatusBar().SetStatusText(text)
        print(text)


class SettingDialog(wxLifeUI.SettingsDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self._board_size = (None, None)
        self._fill_factor = None
        if type(parent) is MainWindow:
            self.SetBoardSize(parent._board_size)
            self.SetFillFactor(parent._fill_factor)
            self.SetStagnationWindow(parent._stagnation_window)
            self.SetSimilarityThreshold(parent._similarity_threshold)
            self.SetHistoryLimit(parent.getHistoryLimit())
            save_format = "RLE"
            if parent._save_format == life.FMT_LIFE:
                save_format = "Life"
            elif parent._save_format == life.FMT_CELLS:
                save_format = "Cells"
            self.SetSaveFormat(save_format)

    def SetBoardSize(self, size):
        self._board_size = size
        self.m_textCtrl_width.SetValue(str(size[0]))
        self.m_textCtrl_height.SetValue(str(size[1]))

    def GetBoardSize(self):
        return self._board_size

    def SetFillFactor(self, factor):
        self._fill_factor = factor
        self.m_textCtrl_fill.SetValue(str(factor))

    def GetFillFactor(self):
        return self._fill_factor

    def SetStagnationWindow(self, window):
        self._stagnation_window = window
        self.m_textCtrl_stagnation.SetValue(str(window))

    def GetStagnationWindow(self):
        return self._stagnation_window

    def SetSimilarityThreshold(self, threshold):
        self._similarity_threshold = threshold
        self.m_textCtrl_similarity.SetValue(str(threshold))

    def GetSimilarityThreshold(self):
        return self._similarity_threshold

    def SetHistoryLimit(self, limit):
        self._history_limit = limit
        self.m_textCtrl_history.SetValue(str(limit))

    def GetHistoryLimit(self):
        return self._history_limit

    def SetSaveFormat(self, format):
        num = self.m_combo_saveformat.GetCount()
        found = False
        for f in range(num):
            if format == self.m_combo_saveformat.GetString(f):
                self.m_combo_saveformat.SetSelection(f)
                found = True
                break
        if not found:
            raise ValueError(f'Unknown format {format}')

    def GetSaveFormat(self):
        selected = self.m_combo_saveformat.GetSelection()
        if selected == wx.NOT_FOUND:
            return "UNKNOWN"
        else:
            return self.m_combo_saveformat.GetString(selected)

    def OnSave(self, event):
        event.Skip()
        try:
            width = int(self.m_textCtrl_width.GetValue())
            height = int(self.m_textCtrl_height.GetValue())
            fill = int(self.m_textCtrl_fill.GetValue())
            window = int(self.m_textCtrl_stagnation.GetValue())
            threshold = float(self.m_textCtrl_similarity.GetValue())
            history = int(self.m_textCtrl_history.GetValue())
            format = self.GetSaveFormat()

        except Exception:
            self.setStatus('Unable to parse values, please use numbers')

        if width <= 0:
            self.setStatus('Width must be a positive number')
        elif height <= 0:
            self.setStatus('Height must be a positive number')
        elif fill <= 0 or fill > 100:
            self.setStatus('Fill must be between 1-100')
        elif window < 0:
            self.setStatus('Stagnation window cannot be negative')
        elif threshold < 0 or threshold > 1:
            self.setStatus('Similarity threshold must be between 0 and 1')
        elif format not in ['Life', 'RLE', 'Cells']:
            self.setStatus('Please choose a save format')
        else:
            self._board_size = (width, height)
            self._fill_factor = fill
            self._stagnation_window = window
            self._similarity_threshold = threshold
            self._history_limit = history

            if type(self.GetParent()) is MainWindow:
                self.GetParent()._board_size = self.GetBoardSize()
                self.GetParent()._fill_factor = self.GetFillFactor()
                self.GetParent()._stagnation_window = self.GetStagnationWindow()
                self.GetParent()._similarity_threshold = self.GetSimilarityThreshold()
                self.GetParent().setHistoryLimit(self.GetHistoryLimit())

                fmtId = wx.NOT_FOUND
                if format == 'RLE':
                    fmtId = life.FMT_RLE
                elif format == 'Life':
                    fmtId = life.FMT_LIFE
                else:
                    fmtId = life.FMT_CELLS
                self.GetParent()._save_format = fmtId
            self.EndModal(wx.ID_OK)

    def setStatus(self, text):
        alert = AlertDialog(self, text)
        alert.ShowModal()


class AlertDialog(wxLifeUI.AlertDialog):
    def __init__(self, parent, text):
        super().__init__(parent)
        self.m_text_alert.SetLabel(text)
        self.Fit()

    def OnClose(self, event):
        self.EndModal(wx.ID_OK)
        self.Destroy()


app = wx.App(False)
mainWindow = MainWindow(None)
app.SetTopWindow(mainWindow)
mainWindow.Show()
app.MainLoop()
