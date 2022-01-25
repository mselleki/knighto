from PIL import Image
import glob


def pngtogif():
    # Create the frames
    frames = []
    imgs = glob.glob("board_png/*.png")
    imgs.sort(key=lambda x: float(x.strip('board_png/move')))
    for i in imgs:
        new_frame = Image.open(i)
        frames.append(new_frame)

    # Save into a GIF file that loops forever
    frames[0].save('knighto_walk.gif', format='GIF',
                   append_images=frames[1:],
                   save_all=True,
                   duration=200, loop=0)
