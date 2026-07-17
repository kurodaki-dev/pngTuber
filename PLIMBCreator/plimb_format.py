import os
import json
import zipfile
import shutil
import tempfile


PLIMB_VERSION = 1


def create_plimb(
    output_file,
    project_name,
    images,
    background
):
    """
    images :
    {
        "mouth_closed":"chemin/image.png",
        "mouth_open":"chemin/image.png",
        "idle":"chemin/image.png"
    }
    """

    temp = tempfile.mkdtemp()

    try:
        sprites = os.path.join(temp, "sprites")
        os.makedirs(sprites)

        manifest = {
            "version": PLIMB_VERSION,
            "name": project_name,
            "background": background,
            "sprites": {}
        }


        for role, path in images.items():

            if path:

                filename = os.path.basename(path)

                shutil.copy(
                    path,
                    os.path.join(
                        sprites,
                        filename
                    )
                )

                manifest["sprites"][role] = filename


        with open(
            os.path.join(temp, "manifest.json"),
            "w",
            encoding="utf8"
        ) as f:

            json.dump(
                manifest,
                f,
                indent=4
            )


        zip_path = output_file + ".zip"


        with zipfile.ZipFile(
            zip_path,
            "w",
            zipfile.ZIP_DEFLATED
        ) as z:


            for root, dirs, files in os.walk(temp):

                for file in files:

                    full = os.path.join(
                        root,
                        file
                    )

                    rel = os.path.relpath(
                        full,
                        temp
                    )

                    z.write(
                        full,
                        rel
                    )


        if os.path.exists(output_file):
            os.remove(output_file)


        os.rename(
            zip_path,
            output_file
        )


    finally:
        shutil.rmtree(temp)