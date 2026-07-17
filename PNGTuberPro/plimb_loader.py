import zipfile
import json
import os
import tempfile
import shutil

from PIL import Image


class Plimb:

    def __init__(self, path):

        self.path = path
        self.temp = tempfile.mkdtemp()

        with zipfile.ZipFile(path, "r") as z:
            z.extractall(self.temp)


        with open(
            os.path.join(
                self.temp,
                "manifest.json"
            ),
            encoding="utf8"
        ) as f:

            self.data=json.load(f)



    def get_background(self):

        return self.data.get(
            "background",
            [0,255,0]
        )


    def get_sprite_path(self,name):

        sprites=self.data["sprites"]

        if name not in sprites:
            return None


        return os.path.join(
            self.temp,
            "sprites",
            sprites[name]
        )



    def load_image(self,name,size):

        path=self.get_sprite_path(name)

        if not path:
            return None


        img=Image.open(path)

        img=img.convert(
            "RGBA"
        )

        img=img.resize(
            size
        )

        return img