#!/usr/bin/env python
# coding: utf-8


from requests_html import HTMLSession
import re
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os


class Card:

    _session = HTMLSession()
    _cwd = os.path.dirname(os.path.abspath(__file__))
    _left_center = 78

    def __init__(self, url, rating=None):

        r = self._session.get(url, params={'rating': rating})
        card = r.html.find('div[id=fm-card-download]', first=True)

        self.version = card.attrs['class'][0]
        self.rating = card.find('span[class=rating]', first=True).text
        self.pos = card.find('span[class=position]', first=True).text
        self.name = card.find('span[class=name]', first=True).text.upper()

        print('{:<15}  {:<20}  {:<4}  {:>3}'.format(self.version, self.name, self.pos, self.rating))

        self.url_card = card.find('img[class=background]', first=True).attrs['data-src']
        self.url_player = card.find('img[class=player-img]', first=True).attrs['data-src']
        self.url_club = card.find('img[class=club-img]', first=True).attrs['data-error']
        self.url_reg = card.find('img[class=nation-img]', first=True).attrs['data-src']

        self.img_card = self._url_to_RGBA(self.url_card)
        self.img_player = self._url_to_RGBA(self.url_player)
        self.img_club = self._url_to_RGBA(self.url_club)
        self.img_reg = self._url_to_RGBA(self.url_reg)

        anims = card.find('div[class=card-animation]')
        if anims:
            self.is_anim = True
            self.url_anims = [re.findall('background-image:url\((.+)\)', anim.attrs['style'])[0] for anim in anims]
            self.img_anims = []

            anim_dir = self._cwd + os.sep + re.findall('/(sprites.+)/', self.url_anims[0])[0]
            if not os.path.exists(anim_dir):
                os.mkdir(anim_dir)

            for url_anim in self.url_anims:
                fname = anim_dir + os.sep + re.findall('.+/(.+\.png)', url_anim)[0]
                if not os.path.exists(fname):
                    with open(fname, 'wb') as f:
                        f.write(self._session.get(url_anim).content)
                self.img_anims.append(Image.open(fname).convert('RGBA'))
        else:
            self.is_anim = False


    def _url_to_RGBA(self, url):
        return Image.open(BytesIO(self._session.get(url).content)).convert('RGBA')


    def _make_single(self, width, height, bgcolor, show_card, show_player, show_name, img_anims=None):
        bg = Image.new('RGBA', (width, height), bgcolor)

        if show_card:
            im = self.img_card.copy()
        else:
            im = Image.new('RGBA', (width, height), (0, 0, 0, 0))

        img_club = self.img_club.resize((38, 38), Image.ANTIALIAS)
        img_reg = self.img_reg.resize((30, 18), Image.ANTIALIAS)

        if img_anims:
            for img_anim in img_anims:
                im = Image.alpha_composite(im, img_anim)

        if show_player:
            im = Image.alpha_composite(im, self.img_player)

        im.paste(img_club, (self._left_center-19, 92), mask=img_club.getchannel('A'))
        im.paste(img_reg, (self._left_center-15, 138))

        draw = ImageDraw.Draw(im)

        # Rating
        font = ImageFont.truetype(self._cwd+'/assets/DINPro-CondBold.woff', size=55)
        fontsize = font.getsize(self.rating)
        draw.text((57, 15), self.rating, font=font)

        # Position
        font = ImageFont.truetype(self._cwd+'/assets/Posterama-Text-Light.otf', size=17)
        fontsize = font.getsize(self.pos)
        draw.text((self._left_center-fontsize[0]//2, 72), self.pos, font=font)

        # Name
        if show_name:
            font = ImageFont.truetype(self._cwd+'/assets/Posterama-Text-Light.otf', size=21)
            fontsize = font.getsize(self.name)

            if fontsize[0] <= 130:
                if self.version == 'fm-card-21':
                    draw.text((128-fontsize[0]//2, 172), self.name, font=font)
                else:
                    draw.text((128-fontsize[0]//2, 178), self.name, font=font)
            else:
                im_tmp = Image.new('RGBA', (fontsize[0], fontsize[1]), (0, 0, 0, 0))
                draw_tmp = ImageDraw.Draw(im_tmp)
                draw_tmp.text((0, 0), self.name, font=font)
                im_tmp = im_tmp.resize((130, 16), Image.ANTIALIAS)
                if self.version == 'fm-card-21':
                    im.paste(im_tmp, (128-65, 172), mask=im_tmp.getchannel('A'))
                else:
                    im.paste(im_tmp, (128-65, 178), mask=im_tmp.getchannel('A'))

        bg.paste(im, ((width-256)//2, (height-256)//2), mask=im.getchannel('A'))
        return bg


    def make(self, width=256, height=256, bgcolor=(0, 0, 0, 0), show_card=True, show_player=True, show_name=True):
        if not self.is_anim:
            self.im = self._make_single(width, height, bgcolor, show_card, show_player, show_name)
        else:
            ims = []
            anim_frames = self.img_anims[0].width // 256

            for frame in range(anim_frames):
                anims = [img_anim.crop((frame*256, 0, (frame+1)*256, 256)) for img_anim in self.img_anims]

                if len(anims) > 1:
                    if np.all(np.bitwise_or(*[anim.getchannel('A') for anim in anims]) == 0):
                        break
                else:
                    if np.all(np.array(anims[0].getchannel('A')) == 0):
                        break

                im = self._make_single(width, height, bgcolor, show_card, show_player, show_name, anims)
                ims.append(im)

            self.ims = ims
            self.im = ims[0]


    def to_gif(self, export_dir='gif', compress=False, compress_loss=False):
        try:
            self.ims
        except:
            print('Not animated card!')
            return

        export_dir += os.sep
        if not os.path.exists(export_dir):
            os.mkdir(export_dir)

        fname = '{0}{1}-{2}-{3}.gif'.format(export_dir, self.name, self.rating, self.pos)
        self.ims[0].save(fname, save_all=True, append_images=self.ims[1:], duration=1000/30, loop=0)

        if compress:
            fname_tmp = '{0}out.gif'.format(export_dir)
            fname_tmpc = '{0}out_c.gif'.format(export_dir)
            fname_c = '{0}{1}-{2}-{3}_c.gif'.format(export_dir, self.name, self.rating, self.pos)
            os.rename(fname, fname_tmp)
            if os.path.exists(fname_c):
                os.remove(fname_c)
            if compress_loss:
                os.system('gifsicle.exe -O3 -j2 -k256 {0} -o {1}'.format(fname_tmp, fname_tmpc))
            else:
                os.system('gifsicle.exe -w -O3 -j2 {0} -o {1}'.format(fname_tmp, fname_tmpc))
            os.rename(fname_tmp, fname)
            os.rename(fname_tmpc, fname_c)


    def to_png(self, export_dir='png'):
        export_dir += os.sep
        if not os.path.exists(export_dir):
            os.mkdir(export_dir)
        self.im.save('{0}{1}-{2}-{3}.png'.format(export_dir, self.name, self.rating, self.pos))

    def to_pngs(self, export_dir='pngs'):
        export_dir = export_dir + os.sep + '{0}-{1}-{2}'.format(self.name, self.rating, self.pos) + os.sep
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
        for i, im in enumerate(self.ims, start=1):
            im.save('{0}{1:0>2d}.png'.format(export_dir, i))
