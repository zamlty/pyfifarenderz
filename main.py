from pyfifarenderz import Card


# # id_ut = [
# #     21501472,
# #     21501511
# # ]

# id_normal = [
#     # 21501073,
#     # 21501868,
#     # 21502013,
#     # 21501718,
#     # 21501677,
#     # 21501941,
#     # 21500198,
#     21501151,
#     21501805,
#     21500482,
# ]

# # for i in id_ut:
# #     c = Card('https://www.fifarenderz.com/20/player/{}?rating=100'.format(i))
# #     c.make(show_name=False)
# #     c.to_gif()

# for i in id_normal:
#     c = Card('https://www.fifarenderz.com/20/player/{}?rating=100'.format(i))
#     c.make()
#     c.to_gif()


c1 = Card('https://www.fifarenderz.com/20/player/21501718?rating=100')
c2 = Card('https://www.fifarenderz.com/20/player/21501983?rating=100')

c1.rating = c2.rating
c1.pos = c2.pos
c1.name = c2.name
c1.img_player = c2.img_player
c1.img_reg = c2.img_reg

c1.make()
c1.to_gif()






