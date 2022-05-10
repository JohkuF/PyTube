from faulthandler import disable
from sysconfig import get_path
import PySimpleGUI as sg
from pytube import YouTube
from pathlib import Path
import os


def progress_check(stream, chunk, bytes_remaining):
    progress_amount = 100 - round(bytes_remaining / stream.filesize * 100)
    window['-PROGRESSBAR-'].update(progress_amount)

def on_complete(sream, file_path):
    window['-PROGRESSBAR-'].update(0)

sg.theme('Darkred1')

start_layout = [[sg.Input(key = '-INPUT-'), sg.Button('Submit', bind_return_key=True)]]

info_tab = [
    [sg.Text('Title:'), sg.Text('',key = '-TITLE-')],
    [sg.Text('Lenght:'), sg.Text('',key = '-LENGHT-')],
    [sg.Text('Views:'), sg.Text('',key = '-VIEWS-')],
    [sg.Text('Author:'), sg.Text('', key = '-AUTHOR-')],
    [sg.Text('Description:'), sg.Multiline('',key = '-DESCRIPTION-', size = (40,20),no_scrollbar = True, disabled = True)],
]

download_tab = [
    [sg.Text('', key = '-TITLE2-')],
    [sg.Frame('Best Quality', [[sg.Button('Download', key = '-BEST-'), sg.Text('', key = '-BESTRES-'), sg.Text('', key = '-BESTSIZE-')]])],
    [sg.Frame('Worst Quality', [[sg.Button('Download', key = '-WORST-'), sg.Text('', key = '-WORSTRES-'), sg.Text('', key = '-WORSTSIZE-')]])],
    [sg.Frame('Audio', [[sg.Button('Download', key = '-AUDIO-'), sg.Text('', key = '-AUDIOSIZE-')]])],
    [sg.VPush()],
    [sg.Progress(100, size = (20,20), expand_x = True, key = '-PROGRESSBAR-')],
]

new_download_tab = [
    [sg.Frame('New Download Link',[[sg.Input(key = '-NEWINPUT-'), sg.Button('Submit', key='-NEWSUBMIT-', bind_return_key=True)]])],
]

settings_tab = [
    [sg.Frame('Save Location',[
        [sg.Multiline('', key='-SAVEPATH-',no_scrollbar=True,disabled=True),sg.Button('Browse Folder', key='-SAVE-')]])]]


layout = [[sg.TabGroup([[
    sg.Tab('Info',info_tab),sg.Tab('Download',download_tab),sg.Tab('New', new_download_tab),sg.Tab('Settings', settings_tab)]])]]

window = sg.Window('pyTube',start_layout)

#Auto save folder
file = os.getcwd()

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    
    if event == 'Submit':

        
        video_object = YouTube(values['-INPUT-'],on_progress_callback= progress_check, on_complete_callback= on_complete)
        window.close()

        window = sg.Window('pyTube', layout, finalize = True)
        window['-TITLE-'].update(video_object.title)
        window['-TITLE2-'].update(video_object.title)
        window['-LENGHT-'].update(f'{round(video_object.length / 60, 2)} minutes')
        window['-VIEWS-'].update(video_object.views)
        window['-AUTHOR-'].update(video_object.author)
        window['-DESCRIPTION-'].update(video_object.description)

        window['-BESTSIZE-'].update(f'{round(video_object.streams.get_highest_resolution().filesize / 1048576,1)} MB')
        window['-BESTRES-'].update(video_object.streams.get_highest_resolution().resolution)

        window['-WORSTSIZE-'].update(f'{round(video_object.streams.get_lowest_resolution().filesize / 1048576,1)} MB')
        window['-WORSTRES-'].update(video_object.streams.get_highest_resolution().resolution)

        window['-AUDIOSIZE-'].update(f'{round(video_object.streams.get_audio_only().filesize / 1048576,1)} MB')

    if event == '-NEWSUBMIT-':
        video_object = YouTube(values['-NEWINPUT-'],on_progress_callback= progress_check, on_complete_callback= on_complete)
    
        #window = sg.Window('pyTube', layout, finalize = True)
        window['-TITLE-'].update(video_object.title)
        window['-TITLE2-'].update(video_object.title)
        window['-LENGHT-'].update(f'{round(video_object.length / 60, 2)} minutes')
        window['-VIEWS-'].update(video_object.views)
        window['-AUTHOR-'].update(video_object.author)
        window['-DESCRIPTION-'].update(video_object.description)

        window['-BESTSIZE-'].update(f'{round(video_object.streams.get_highest_resolution().filesize / 1048576,1)} MB')
        window['-BESTRES-'].update(video_object.streams.get_highest_resolution().resolution)

        window['-WORSTSIZE-'].update(f'{round(video_object.streams.get_lowest_resolution().filesize / 1048576,1)} MB')
        window['-WORSTRES-'].update(video_object.streams.get_highest_resolution().resolution)

        window['-AUDIOSIZE-'].update(f'{round(video_object.streams.get_audio_only().filesize / 1048576,1)} MB')

    if event == '-DEFAULTTHEME-':
        sg.theme('Darkred1')
        window.refresh()
    
    if event == '-LIGHTTHEME-':
        sg.theme('SystemDefault1')
        window.refresh()

    if event == '-DARKTHEME-':
        sg.theme('Darkblue1')
        window.refresh()

    if event == '-SAVE-':
        file_path = sg.popup_get_folder('Folder Browse', no_window=True)
        file = Path(file_path)
        window['-SAVEPATH-'].update(file)

    if event == '-BEST-':
        video_object.streams.get_highest_resolution().download(file)
    if event == '-WORST-':
        video_object.streams.get_lowest_resolution().download(file)
    if event == '-AUDIO-':
        video_object.streams.get_audio_only().download(file)


window.close()