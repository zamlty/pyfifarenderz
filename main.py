from pyfifarenderz import Card
from itertools import product

urls = [
    'https://fifarenderz.com/20/player/21501511',
    'https://fifarenderz.com/21/player/22501454',
]
ratings = [None, 100, 110]

for url, rating in product(urls, ratings):
    c = Card(
        url=url,
        rating=rating,        # default: None
        width=256,            # default: 256
        height=256,           # default: 256
        bgcolor=(0, 0, 0, 0), # default: transparent black for PNG;
                              #          always non-transparent for GIF
        show_card=True,       # default: True
        show_player=True,     # default: True; automatically False if necessary
        show_name=True,       # default: True; automatically False if necessary
    )

    c.to_gif(compress=False)  # export GIF; compression requires the Gifsicle binary
    # c.to_pngs()             # export PNG sequence
    # c.to_png()              # export PNG for the first frame
