from textnode import *
from htmlnode import *
import os, shutil

def copy_source_to_destination():
    # delete all contents in public
    shutil.rmtree()







def main():
    dummy = TextNode("some dummy text", TextType.LINK, "https://downloads.khinsider.com/game-soundtracks/album/phantasy-star-online-2-ost-vol.-1")
    print(dummy)

if __name__ == "__main__":
    main()