# pyfifarenderz

## Overview

pyfifarenderz is an immature Python module to export the card GIF (and PNG sequence) from [**FIFARenderZ**](https://fifarenderz.com) for FIFA Mobile players. You can simply change the rating shown on the card, the background of the card, or anything you want. You can also compress the exported GIF.

**Notes: This code can only export non-transparent GIF because the quality of the exported GIF with transparent background using Pillow is quite low. It is encouraged to export the PNG sequence with transparent background and then use Photoshop to generate a GIF.**


## Requirements

[Python 3](https://www.python.org), [NumPy](https://numpy.org), [Pillow](https://github.com/python-pillow/Pillow), and [Requests-HTML](https://github.com/psf/requests-html). To compress the exported GIF, the [Gifsicle](http://www.lcdf.org/gifsicle) binary is also required.


## How to use

```python
# use main.py as example
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
```


## Exported GIFs
|default rating|rating=100|rating=110|
|:--:|:--:|:--:|
|![C. RONALDO-95-ST-TOTY_S4_fm-card-20_compressed.gif](https://i.loli.net/2021/01/26/6Heyn3bSuD9wKvJ.gif)|![C. RONALDO-100-ST-TOTY_S4_fm-card-20_compressed.gif](https://i.loli.net/2021/01/26/IbLK1HDqX2JxFCO.gif)|![C. RONALDO-110-ST-TOTY_S4_fm-card-20_compressed.gif](https://i.loli.net/2021/01/26/SAMCGX8ItK57xDm.gif)|
|![C. RONALDO-96-ST-TOTY_S5_fm-card-21_compressed.gif](https://i.loli.net/2021/01/26/Givl81IzJTPFsDC.gif)|![C. RONALDO-100-ST-TOTY_S5_fm-card-21_compressed.gif](https://i.loli.net/2021/01/26/iAfPGuHm5MlsEyK.gif)|![C. RONALDO-110-ST-TOTY_S5_fm-card-21_compressed.gif](https://i.loli.net/2021/01/26/cDopI3awOY1JR5r.gif)|


## Acknowledgment

- [**FIFARenderZ**](https://fifarenderz.com) - For FIFA Mobile players, you can’t live without it. Really appreciate!
- **My former teammates** - Herobox 和反转地球的兄弟们，谢谢你们！

