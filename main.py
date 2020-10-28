from pyfifarenderz import Card

# id_noplayer = [
#     21502385
# ]

# for i in id_noplayer:
#     c = Card('https://fifarenderz.com/20/player/{}'.format(i), rating=106)
#     c.make(bgcolor=(0, 0, 0, 0), show_player=False, show_name=False)
#     c.to_pngs()

id_normal = [
    # (21503603, 110), # Ronaldo
#     (21505279, 106), # Piero
    (21505917, 106), # Saele
#     (21505422, 104), # Rabiot
#     (21504686, 104), # Rooney
    # (21505281, 108), # Davies
#     (21505282, 104), # Kimpe
    # (21506619, 110), # Duffy
#     (21505916, 106), # Niles
      # (21505280, 106), # Lopes
]

for i, r in id_normal:
    c = Card('https://fifarenderz.com/20/player/{}'.format(i), rating=r)
    c.make(bgcolor=(0, 0, 0, 0))
    # c.make(show_card=False, bgcolor=(0, 0, 0, 0))
    c.to_pngs()

