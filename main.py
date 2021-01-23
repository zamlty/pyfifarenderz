from pyfifarenderz import Card

# c = Card('https://fifarenderz.com/21/player/22501045')
c = Card('https://fifarenderz.com/21/player/22501045', rating=100) # change the rating

c.make() # render all the frames for the animated card or the only frame for the static card
         # default: transparent background for PNG; black background for GIF
# c.make(bgcolor=(0, 0, 0, 255)) # black background for GIF and PNG

c.to_gif(compress=False) # export GIF; compression requires the Gifsicle binary
# c.to_pngs() # export PNG sequence
# c.to_png() # export PNG for the first frame
