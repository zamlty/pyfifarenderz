#!/usr/bin/env python
# coding: utf-8


from requests_html import HTMLSession
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
from os import path


class Card:

    __session = HTMLSession()
    __cwd = path.dirname(path.abspath(__file__))
    __left_center = 78

    def __init__(self, card_id, rating=None):

        url = 'https://fifarenderz.com/20/player/%s' % card_id
        if rating:
            url += '?rating=%d' % rating

        # r = self.__session.get(url, proxies={'http': 'http://127.0.0.1:1080', 'https': 'http://127.0.0.1:1080'})
        r = self.__session.get(url)
        card = r.html.find('div[class=player-card] > div[class^=fm-card]', first=True)

        self.rating, self.pos, name = (span.text for span in card.find('div > span')[0:3])
        self.name = name.upper()

        print('{:<8}    {:<20}  {:<4}  {:>3}'.format(card_id, self.name, self.pos, self.rating))

        img_urls = (img.attrs['data-src'] for img in card.find('div > img[data-src]'))
        self.img_card, self.img_player, self.img_club, self.img_reg = (
            Image.open(BytesIO(self.__session.get(u).content)).convert('RGBA') for u in img_urls)

        anim_names = [div.attrs['data-name'] for div in card.find('div > div[class=card-animation-insert]')]
        if anim_names:
            self.is_anim = True
            self.img_anims = []

            if not os.path.exists(self.__cwd+'/sprites_20'):
                os.mkdir(self.__cwd+'/sprites_20')

            for n in anim_names:
                fname = '{}/sprites_20/{}.png'.format(self.__cwd, n)
                if not os.path.exists(fname):
                    anim_url = 'https://cdn-p2.frzdb.net/fifamobile/images/sprites_20/{}.png'.format(n)
                    with open(fname, 'wb') as f:
                        f.write(self.__session.get(anim_url).content)
                self.img_anims.append(Image.open(fname).convert('RGBA'))
        else:
            self.is_anim = False


    def __make_single(self, width, height, bgcolor, show_card, show_player, show_name, img_anims=None):
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

        im.paste(img_club, (self.__left_center-19, 92), mask=img_club.getchannel('A'))
        im.paste(img_reg, (self.__left_center-15, 138))

        draw = ImageDraw.Draw(im)

        # 评分
        font = ImageFont.truetype(self.__cwd+'/assets/DINPro-CondBold.woff', size=55)
        fontsize = font.getsize(self.rating)
        # draw.text((self.__left_center-fontsize[0]//2+1, 13), rating, font=font)
        draw.text((57, 15), self.rating, font=font)

        # 位置
        font = ImageFont.truetype(self.__cwd+'/assets/Posterama-Text-Light.otf', size=17)
        fontsize = font.getsize(self.pos)
        draw.text((self.__left_center-fontsize[0]//2, 72), self.pos, font=font)

        # 姓名
        if show_name:
            font = ImageFont.truetype(self.__cwd+'/assets/Posterama-Text-Light.otf', size=21)
            fontsize = font.getsize(self.name)

            # print(fontsize[0]) # height=16
            if fontsize[0] <= 130:
                draw.text((128-fontsize[0]//2, 178), self.name, font=font)
            else:
                # im_tmp = Image.new('RGBA', (fontsize[0]+2, fontsize[1]), (0, 0, 0, 0))
                im_tmp = Image.new('RGBA', (fontsize[0], fontsize[1]), (0, 0, 0, 0))
                draw_tmp = ImageDraw.Draw(im_tmp)
                draw_tmp.text((0, 0), self.name, font=font)
                # if 130 < fontsize[0] < 200:
                #     draw_tmp.text((0.5, 0), self.name, font=font)
                #     draw_tmp.text((1, 0), self.name, font=font)
                #     draw_tmp.text((1.5, 0), self.name, font=font)
                # else:
                #     draw_tmp.text((0, 0), self.name, font=font)
                #     draw_tmp.text((1, 0), self.name, font=font)
                #     draw_tmp.text((2, 0), self.name, font=font)
                im_tmp = im_tmp.resize((130, 16), Image.ANTIALIAS)
                im.paste(im_tmp, (128-65, 178), mask=im_tmp.getchannel('A'))

        bg.paste(im, ((width-256)//2, (height-256)//2), mask=im.getchannel('A'))
        return bg


    def make(self, width=256, height=256, bgcolor=(0, 0, 0), show_card=True, show_player=True, show_name=True):
        if not self.is_anim:
            self.im = self.__make_single(width, height, bgcolor, show_card, show_player, show_name)
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
                        if np.all(np.array(crops[0].getchannel('A')) == 0):
                            break

                    im = self.__make_single(width, height, bgcolor, show_card, show_player, show_name, crops)
                    ims.append(im)
                else:
                    continue
                break

            self.ims = ims
            self.im = ims[len(ims)//2]


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
        self.ims[0].save(fname, save_all=True, append_images=self.ims, duration=31.25, loop=0)
        if compress:
            fname_tmp = '{0}out.gif'.format(export_dir)
            fname_tmpc = '{0}out_c.gif'.format(export_dir)
            fname_c = '{0}{1}-{2}-{3}_c.gif'.format(export_dir, self.name, self.rating, self.pos)
            os.rename(fname, fname_tmp)
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
