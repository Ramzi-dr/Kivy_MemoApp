#from logging import error, raiseExceptions, root
#from os import W_OK
#import pathlib
#from typing_extensions import Concatenate
#import PIL

from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
import os
import threading
from kivy.clock import Clock, mainthread
from kivy.core import window
from kivy.core.window import Window
from typing import Text, List
from kivy.app import App
from kivy.lang import builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.layout import Layout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.app import Builder
from kivy.metrics import dp
from kivy.config import Config
#from kivy.app import runTouchApp
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import StringProperty, ObjectProperty, NumericProperty,BooleanProperty
from functools import partial
#from plyer import filechooser
import time
import image_list
#Window.maximize()



class LandingPage(Screen):
    hint_text = StringProperty('Vul je naam hier in')

    def __init__(self, **kwargs):
        super(LandingPage, self).__init__(**kwargs)
        self.gamer_name = ''
        self.sec = 0
        self.on = 0

    def screen_transition(self, *args):
        self.manager.current = 'game'

    def popup_foto_selection(self,*args):
        content = PopupFotoSelect()
        popupSelection = Popup(content=content,title='', separator_height=dp(0), auto_dismiss=False, size_hint=(.6, .5))
        content.ids.start_selection_bt.bind(on_release=popupSelection.dismiss,on_press=ImageChooserPage().file_chooser)
        popupSelection.open()
        
    def popup_foto_new_selection(self,*args):
        content = PopupFotoSelectionEmpltyList()
        popup_new = Popup(content=content,title='', separator_height=dp(0), auto_dismiss=False, size_hint=(.6, .5))
        content.ids.new_selection_bt.bind(on_release=popup_new.dismiss, on_press=ImageChooserPage().file_chooser)
        popup_new.open()

    def startPlay(self):
        return self.ids.start_bt.bind(on_release=self.screen_transition)

    def start_bt(self):
        Octaaf = 'Octaaf De Bolle'
        Kwebbel = 'Kweeeeeebbel'
        self.gamer_name = self.ids.name_input.text
        gamer = self.gamer_name.upper()
        if len(gamer) <= 0:
            self.ids.name_input.hint_text = 'alstublieft uw naam in'
        elif gamer == 'DOURAYD':
            self.ids.up_button.text = f"Hallo {Octaaf}"
            self.manager.get_screen('ImageChooser').gamer_label = 'De Bolle: Ik Will pIpI DoeN'
            self.startPlay()
            self.ids.dridi.text = 'druk op de startknop'
        elif gamer == 'SHAHINEZE':
            self.ids.up_button.text = f'Hallo {Kwebbel}'
            self.manager.get_screen('ImageChooser').gamer_label = 'Kwebbel: jij pRaaT te Veeeel'
            self.startPlay()
            self.ids.dridi.text = 'druk op de startknop'
        else:
            self.ids.up_button.text = f'Hallo {gamer.title()}'
            PopupFotoSelect.hallo_gamer= f'Hallo {gamer.title()}'
            PopupFotoSelectionEmpltyList.gamer= f'Hallo {gamer.title()}'
            self.startPlay()
            self.ids.dridi.text = 'druk op de startknop'
####################################  Fotos selection      ############################

class PopupFotoSelectionEmpltyList(FloatLayout):
    gamer = StringProperty('')

    def __init__(self,**kwargs):
        super(PopupFotoSelectionEmpltyList,self).__init__(**kwargs)

class PopupFotoSelect(FloatLayout):
    hallo_gamer = StringProperty('')

    def __init__(self,**kwargs):
        super(PopupFotoSelect,self).__init__(**kwargs)      

class PopupFotoError(FloatLayout):
    pass
class PopupFotoInList(FloatLayout):
    pass
class PopupFullList(FloatLayout):
    pass
class PopupExitApp(FloatLayout):
    pass
class PopupInfoFotoInList(FloatLayout):
    pass
class PopupYouWin(FloatLayout):
    def play_again(self):
        MatchControl().play_again()
##################################################################################################
################################### GAME PAGE ###################################################

class GamePage(StackLayout):
    current_btn = StringProperty()
    btn_blocked = BooleanProperty(False)
    selection_counter = 0
    memo_images = image_list.image_creator()

    def __init__(self, **kwargs):
        super(GamePage, self).__init__(**kwargs)
        self.counter = 0
        self.on = 0

        for i in range(50):
            self.btn = Button(background_down=self.memo_images[i], border=(1, 1, 1, 1), size_hint=(.1, .2))
            self.ids[f'btn_{str(i)}'] = self.btn
            self.add_widget(self.btn)
        for key in self.ids.keys():
            buttoncallback = partial(self.pressed, key)
            self.ids[key].bind(on_release=buttoncallback)

    def pressed(self, *args):
        self.parent.parent.parent.on_start_timer()
        btn_id = args[0]
        if self.selection_counter == 0 and not self.btn_blocked and GamePage.current_btn != btn_id\
                                       and self.ids[btn_id].background_normal == 'atlas://data/images/defaulttheme/button':
            MatchControl().selection_1(btn_id, self)
            self.selection_counter += 1
            GamePage.current_btn = btn_id
        elif self.selection_counter == 1 and GamePage.current_btn != btn_id\
                and self.ids[btn_id].background_normal == 'atlas://data/images/defaulttheme/button' :
            GamePage.current_btn = btn_id
            MatchControl().selection_2(btn_id, self)
            self.btn_blocked = False
            self.selection_counter -= 1
        else:
            pass


class MatchControl(Screen):
    first_selection_id = StringProperty()
    second_selection_id = StringProperty()
    image1 = StringProperty()
    image2 = StringProperty()
    gamepage_instance = ''
    new_score = 0
    new_level = 1

    def __init__(self, **kwargs):
        super(MatchControl, self).__init__(**kwargs)
        self.selection_counter = int

    def selection_1(self, btn_id, *args):
        args[0].ids[btn_id].background_normal = GamePage().ids[btn_id].background_down
        MatchControl.first_selection_id = btn_id
        MatchControl.image1 = GamePage().ids[btn_id].background_down
        self.selection_counter = 1
        MatchControl.first_selection_id = btn_id
        self.selection_control(args[0])
        GamePage.btn_blocked = True

    def selection_2(self, btn_id, *args):
        args[0].ids[btn_id].background_normal = GamePage().ids[btn_id].background_down
        MatchControl.image2 = GamePage().ids[btn_id].background_down
        MatchControl.second_selection_id = btn_id
        self.selection_counter = 2
        self.selection_control(args[0])

    def selection_control(self, instance, *args):
        MatchControl.gamepage_instance = instance
        if self.selection_counter == 2 and MatchControl.image1 != MatchControl.image2:
            instance.ids[self.first_selection_id].background_normal = 'atlas://data/images/defaulttheme/button'
            instance.ids[self.second_selection_id].background_normal = 'atlas://data/images/defaulttheme/button'
        elif self.selection_counter == 2 and MatchControl.image1 == MatchControl.image2:
            MatchControl.new_score += 1
            if MatchControl.new_score < 10:
                instance.parent.parent.parent.score = f'Score: 0{self.new_score}'
            else:
                instance.parent.parent.parent.score = f'Score: {self.new_score}'
                if self.new_score == 25:
                    self.you_win()

    def you_win(self, *args):
        you_win_instance = PopupYouWin()
        popup_win = Popup(content=you_win_instance, title='', separator_height=dp(0), auto_dismiss=False,
                             size_hint=(.6, .6))
        you_win_instance.ids.play_again.bind(on_press=popup_win.dismiss)
        popup_win.open()

    def play_again(self):
        GamePage.memo_images = image_list.image_creator()
        MatchControl.new_level += 1
        MatchControl.gamepage_instance.parent.parent.parent.level = f'Level: {self.new_level}'
        MatchControl.gamepage_instance.parent.parent.parent.manager.get_screen('game').stop_play()
        MatchControl.gamepage_instance.clear_widgets()
        MatchControl.gamepage_instance.__init__()
        MatchControl.gamepage_instance.parent.parent.parent.manager.current = 'game'


class Scroll(Screen):
    if_timer = False
    score = StringProperty('Score: 00')
    level = StringProperty('level: 01')

    def __init__(self, **kwargs):
        super(Scroll, self).__init__(**kwargs)
        self.pattern = '{0:02d}:{1:02d}:{2:02d}'
        self.timer = [0, 0, 0]
        self.timerString = ''
        self.Clock_run = ''

    def Label_updater(self, time_string):
        self.ids.time_.text = time_string

    def timer_func(self, *args):
        self.timer[2] += 1
        if self.timer[2] >= 60:
            self.timer[2] = 0
            self.timer[1] += 1
        if self.timer[1] >= 60:
            self.timer[0] += 1
            self.timer[1] = 0
        self.timeString = self.pattern.format(self.timer[0], self.timer[1], self.timer[2])
        self.Label_updater(self.timeString)

    def screen_transition(self, *args):
        self.manager.current = 'landing'

    def on_start_timer(self):

        if self.if_timer is False:
            Clock.schedule_interval(self.timer_func, 1)
            self.if_timer = True

    def on_pause_timer(self):
        Clock.unschedule(self.timer_func)
        self.if_timer = False

    def stop_play(self):
        self.on_pause_timer()
        self.timeString = self.pattern.format(0, 0, 0)
        self.Label_updater(self.timeString)
        self.pattern = '{0:02d}:{1:02d}:{2:02d}'
        self.timer = [0, 0, 0]
        self.score = 'Score: 00'
        # self.manager.get_screen('landing').ids.dridi.text='Daaaaag'# or root.manager.get_screen....
        #self.manager.get_screen('landing').reset_landing()
        #return self.ids.stop_game.bind(on_release=self.screen_transition)


class WindowManager(ScreenManager):

    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)


class MemoApp(App):
    def build(self):
        sm = WindowManager(transition=FadeTransition())
        sm.add_widget(LandingPage(name='landing'))
        sm.add_widget(Scroll(name='game'))
        #sm.add_widget(ImageChooserPage(name='ImageChooser'))
        return sm


if __name__ == '__main__':
    MemoApp().run()




'''
class ImageChooserPage(Screen):

    def __init__(self,**kwargs):
        super(ImageChooserPage, self).__init__(**kwargs)
        self.window_size()
        self.foto = ''
        self.still_to_select=25

    def window_size(self,dt=0,*args):
        if Window.width <270:
            for x in range (1,26):
                foto_id = f'foto_{x}'
                image_list.append(foto_id)
                self.ids[foto_id].size_hint= (.20,.15)



    def file_chooser(self,*args):
        if len(foto_list) >= 25:
            self.full_list()
        else:
           filechooser.open_file(on_selection=self.selected_foto)


    def selected_foto(self,*args):

        print(args)


        extention_list = ['.JPG', '.PNG', '.GIF', '.TIFF', '.WEBP', '.INDD', '.erer','.JPEG']
        try:
            extention_control = pathlib.Path(foto_path[0]).suffix
            if extention_control.upper() in extention_list:
                print(foto_path)
                self.foto = foto_path[0]
                self.create_foto_list(self.foto)
            else:
                print(0)
                self.foto_error()
        except (RuntimeError, TypeError, NameError, IndexError, PIL.UnidentifiedImageError):
            pass


    def create_foto_list(self, foto):
        if len(foto_list) >= 25:
            self.full_list()

        if foto in foto_list:
            self.foto_in_list()
        if len(foto_list) < 25 and foto not in foto_list:
            foto_list.append(foto)
            print(foto_list)
            self.file_chooser()



        print(len(foto_list))
        print(foto_list)

    def foto_in_list(self, *args):
        foto_in_list_instance = PopupFotoInList()
        popup_inlist = Popup(content=foto_in_list_instance, title='', separator_height=dp(0),auto_dismiss=False, size_hint=(.6, .3))
        foto_in_list_instance.ids.foto_in_list.bind(on_press=popup_inlist.dismiss, on_release= self.file_chooser)
        popup_inlist.open()

    def full_list(self,*args):
        full_list_instance = PopupFullList()
        popup_full_list = Popup(content=full_list_instance, title='', separator_height=dp(0),auto_dismiss=False, size_hint=(.8, .4))
        full_list_instance.ids.start_game_bt.bind(on_press=popup_full_list.dismiss, on_release=self.screen_transition)
        popup_full_list.open()

    def foto_error(self, *args):
        print(34)
        content = PopupFotoError()
        popup_foto_error = Popup(content=content, title='', separator_height=dp(0), auto_dismiss=False, size_hint=(.6, .3))
        content.ids.dismiss_bt.bind(on_press=popup_foto_error.dismiss, on_release=self.file_chooser)
        popup_foto_error.open()

    def screen_transition(self, *args):
        self.manager.current = 'game'

   def exit_app(self):
        exit_app = PopupExitApp()
        exit_app_content = exit_app
        popup_exit_app = Popup(content=exit_app_content, title='', separator_height=dp(0),
                               auto_dismiss=True, size_hint=(.6, .4))
        exit_app_content.ids.no_exit_bt.bind(on_press=popup_exit_app.dismiss)
        popup_exit_app.open()'''


