﻿#!/usr/bin/env python
# coding: utf-8


from requests_html import HTMLSession
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
from os import path


class Card:
    
    __cwd = path.dirname(path.abspath(__file__))
    __left_center = 78

    def __init__(self, url):    
        session = HTMLSession()
        r = session.get(url)
        card = r.html.find('div[class=player-card] > div[class^=fm-card]', first=True)

        self.rating, self.pos, name = (span.text for span in card.find('div > span')[0:3])
        self.name = name.upper()
        
        img_urls = (img.attrs['data-src'] for img in card.find('div > img[data-src]'))
        self.img_card, self.img_player, self.img_club, self.img_reg = (
            Image.open(BytesIO(session.get(u).content)).convert('RGBA') for u in img_urls) 

        anim_names = [div.attrs['data-name'] for div in card.find('div > div[class=card-animation-insert]')]
        if anim_names:
            self.is_anim = True
            anim_urls = ('https://cdn-p2.frzdb.net/fifamobile/images/sprites_20/{}.png'.format(n) for n in anim_names)
            self.img_anims = [Image.open(BytesIO(session.get(u).content)).convert('RGBA') for u in anim_urls]
        else:
            self.is_anim = False
        
        print(self.name, self.pos, self.rating)
        
        
    def __make_single(self, width, height, bgcolor, show_player, show_name, img_anims=None):
        bg = Image.new('RGBA', (width, height), bgcolor)
        
        im = self.img_card.copy()
        img_club = self.img_club.resize((38, 38), Image.ANTIALIAS)
        img_reg = self.img_reg.resize((30, 18), Image.ANTIALIAS)
        
        if img_anims:
            for img_anim in img_anims:
                im = Image.alpha_composite(im, img_anim)
        
        if show_player:
            im = Image.alpha_composite(im, self.img_player)

        im.paste(img_club, (self.__left_center-19, 97), mask=img_club.getchannel('A'))
        im.paste(img_reg, (self.__left_center-15, 143))

        draw = ImageDraw.Draw(im)

        # 评分
        font = ImageFont.truetype(self.__cwd+'/assets/DINPro-CondBold.woff', size=55)
        fontsize = font.getsize(self.rating)
        # draw.text((self.__left_center-fontsize[0]//2+1, 13), rating, font=font)
        draw.text((57, 13), self.rating, font=font)

        # 位置
        font = ImageFont.truetype(self.__cwd+'/assets/Posterama-Bold.ttf', size=17)
        fontsize = font.getsize(self.pos)
        draw.text((self.__left_center-fontsize[0]//2, 67), self.pos, font=font)

        # 姓名
        if show_name:
            font = ImageFont.truetype(self.__cwd+'/assets/Posterama-Bold.ttf', size=21)
            fontsize = font.getsize(self.name)
            #height 16
            draw.text((128-fontsize[0]//2, 178), self.name, font=font)

        bg.paste(im, ((width-256)//2, (height-256)//2), mask=im.getchannel('A'))
        return bg
    
    
    def make(self, width=256, height=256, bgcolor=(0, 0, 0), show_player=True, show_name=True):
        if not self.is_anim:
            self.im = self.__make_single(width, height, bgcolor, show_player, show_name)
        else:
            ims = []
            anim_nx, anim_ny = self.img_anims[0].width // 256, self.img_anims[0].height // 256
            
            for i in range(anim_ny):
                for j in range(anim_nx):
                    l = j * 256
                    u = i * 256
                    crops = [img_anim.crop((l, u, l+256, u+256)) for img_anim in self.img_anims]
                    
                    if len(crops) > 1:
                        if np.all(np.bitwise_or(*[crop.getchannel('A') for crop in crops]) == 0):
                            break
                    else:
                        if np.all(crops[0].getchannel('A') == 0):
                            break
                        
                    im = self.__make_single(width, height, bgcolor, show_player, show_name, crops)
                    ims.append(im)
                else:
                    continue
                break
            
            self.ims = ims
            self.im = ims[len(ims)//2]
            
    
    def to_gif(self, export_dir='gif'):
        try:
            self.ims
        except:
            print('Not animated card!')
            return
        
        export_dir += os.sep
        if not os.path.exists(export_dir):
            os.mkdir(export_dir)
            
        self.ims[0].save('{0}{1}-{2}-{3}.gif'.format(export_dir, self.name, self.rating, self.pos), 
                         save_all=True, append_images=self.ims, duration=31.25, loop=0)

    
    def to_png(self, export_dir='png'):
        export_dir += os.sep        
        if not os.path.exists(export_dir):
            os.mkdir(export_dir)
            
        self.im.save('{0}{1}-{2}-{3}.png'.format(export_dir, self.name, self.rating, self.pos))
        