## pyfifarenderz

### Overview

pyfifarenderz is an immature Python module to export the card GIF (and PNG sequence) from [**FIFARenderZ**](https://fifarenderz.com) for FIFA Mobile players. You can simply change the rating shown on the card, the background of the card, or anything you want. You can also compress the exported GIF.

**Notes: This code can only export non-transparent GIF because the quality of the exported GIF with transparent background using Pillow is quite low. It is encouraged to export the PNG sequence with transparent background and then use Photoshop to generate a GIF.**



### Requirements

Python 3, [Pillow](https://github.com/python-pillow/Pillow), and [Requests-HTML](https://github.com/psf/requests-html). To compress the exported GIF, the [Gifsicle](http://www.lcdf.org/gifsicle) binary is also required.



### How to use

```python
# use main.py as example
from pyfifarenderz import Card

# c = Card('https://fifarenderz.com/21/player/22501045')
c = Card('https://fifarenderz.com/21/player/22501045', rating=100) # change the rating

c.make() # render all the frames for the animated card or the only frame for the static card
         # default: transparent background for PNG; black background for GIF
# c.make(bgcolor=(0, 0, 0, 255)) # black background for GIF and PNG

c.to_gif(compress=False) # export GIF; compression requires the Gifsicle binary
# c.to_pngs() # export PNG sequence
# c.to_png() # export PNG for the first frame
```



### Exported GIF
![C. RONALDO-100-LW.gif](https://i.loli.net/2021/01/23/yosRAbXWSBKDd1k.gif)



### Acknowledgment

- [**FIFARenderZ**](https://fifarenderz.com) - For FIFA Mobile players, you can’t live without it. Really appreciate!
- **My former teammates** - Herobox 和反转地球的兄弟们，谢谢你们！

