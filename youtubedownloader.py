import os
import yt_dlp
import pygame
import pyperclip
import threading
import sys
import time

pygame.init()

formate = 10
download_path = os.getcwd()

status_message = ''
download = False
progress = 0.0  

def resource_path(relative_path):
   
    try:
        
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def download_media(url, formate, download_path):
    global status_message, download, progress

    progress = 0.0  

    def hook(d):
        global progress
        if d['status'] == 'downloading' and 'total_bytes' in d and d['total_bytes']:
            progress = d['downloaded_bytes'] / d['total_bytes']
        elif d['status'] == 'finished':
            progress = 1.0

    os.makedirs(download_path, exist_ok=True)

    ydl_optsmp4 = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'progress_hooks': [hook],
    }

    ydl_optsmp3 = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [hook],
    }

    try:
        if formate == 1:
            status_message = "⏳ Stahuji video..."
            with yt_dlp.YoutubeDL(ydl_optsmp4) as ydl:
                ydl.download([url])
            status_message = f"✅ Video bylo uloženo do: {download_path}"
        elif formate == 2:
            status_message = "⏳ Stahuji zvuk..."
            with yt_dlp.YoutubeDL(ydl_optsmp3) as ydl:
                ydl.download([url])
            status_message = f"✅ Zvuk byl uložen do: {download_path}"
    except Exception as e:
        status_message = f"❌ Chyba: {e}"
    finally:
        download = False
        progress = 0.0


screen = pygame.display.set_mode((1025, 1025))
pygame.display.set_caption("YouTube Downloader")

mainimage = pygame.image.load(resource_path("images/mainimage.png"))
mp4image = pygame.image.load(resource_path("images/mainmp4download.png"))
mp4imagenotext = pygame.image.load(resource_path("images/mainmp4downloadxtext.png"))
mp3image = pygame.image.load(resource_path("images/mainmp3download.png"))
mp3imagenotext = pygame.image.load(resource_path("images/mainmp3downloadxtext.png"))
back = pygame.image.load(resource_path("images/back.png"))
logoimage=pygame.image.load(resource_path("images/echodroppericon.png"))

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
COLOR_TEXT = pygame.Color('white')
COLOR_BG = pygame.Color('white')

font = pygame.font.SysFont(None, 46)
fonta = pygame.font.SysFont(None, 32)

input_active = False
input_text = ''
clicked = 0
running = True
logo=False
while running:
    mx, my = pygame.mouse.get_pos()
    if logo==False:
        screen.blit(logoimage,(0,0))
        pygame.display.flip()
        time.sleep(3)
        logo=True
        formate=0


 
    if formate == 0:
        screen.blit(mainimage, (0, 0))
        input_active = False
        input_text = ''
        status_message = ''
        clicked = 0
        download = False

    if formate == 1:
        if not input_active:
            screen.blit(mp4image, (0, 0))
            screen.blit(back, (930, 950)) 
        else:
            screen.blit(mp4imagenotext, (0, 0))
            screen.blit(back, (930, 950))  
            text_surface = font.render(input_text, True, COLOR_TEXT)
            screen.blit(text_surface, (110, 420))

            status_render = fonta.render(status_message, True, COLOR_TEXT)
            screen.blit(status_render, (110, 700))

            if download:
                progress_percent = int(progress * 100)
                progress_text = fonta.render(f"{progress_percent} %", True, COLOR_TEXT)
                screen.blit(progress_text, (110, 740))

    if formate == 2:
        if not input_active:
            screen.blit(mp3image, (0, 0))
            screen.blit(back, (930, 950))  
        else:
            screen.blit(mp3imagenotext, (0, 0))
            screen.blit(back, (930, 950)) 
            text_surface = font.render(input_text, True, COLOR_TEXT)
            screen.blit(text_surface, (110, 420))

            status_render = fonta.render(status_message, True, COLOR_TEXT)
            screen.blit(status_render, (110, 700))

            if download:
                progress_percent = int(progress * 100)
                progress_text = fonta.render(f"{progress_percent} %", True, COLOR_TEXT)
                screen.blit(progress_text, (110, 740))

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if formate == 0:
                if 530 <= mx <= 925 and 730 <= my <= 850:
                    formate = 1
                if 100 <= mx <= 500 and 730 <= my <= 850:
                    formate = 2

            elif formate == 1:
                if 100 <= mx <= 920 and 380 <= my <= 480:
                    if clicked % 2 == 0:
                        input_active = True
                        clicked += 1
                if input_active and 100 <= mx <= 920 and 510 <= my <= 630 and not download:
                    download = True
                    status_message = "⏳ Spouštím stahování..."

                    def thread_download():
                        download_media(input_text, formate, download_path)

                    threading.Thread(target=thread_download, daemon=True).start()

                if mx > 930 and my > 950:
                    formate = 0

            elif formate == 2:
                if 100 <= mx <= 920 and 380 <= my <= 480:
                    if clicked % 2 == 0:
                        input_active = True
                        clicked += 1
                if input_active and 100 <= mx <= 920 and 510 <= my <= 630 and not download:
                    download = True
                    status_message = "⏳ Spouštím stahování..."

                    def thread_download():
                        download_media(input_text, formate, download_path)

                    threading.Thread(target=thread_download, daemon=True).start()

                if mx > 930 and my > 950:
                    formate = 0

        elif event.type == pygame.KEYDOWN and input_active:
            if event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                input_text += pyperclip.paste()
            elif event.unicode.isprintable():
                input_text += event.unicode

    pygame.display.flip()

pygame.quit()
