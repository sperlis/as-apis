from asapis.services.asoclib import ASoC
import os

from asapis.utils.printUtil import out

asoc = ASoC()

file_path = asoc.config["filePath"]

if not os.path.exists(file_path):
    out(f"File does not exist: {file_path}")
elif not os.path.isfile(file_path):
    out(f"File is not a valid file: {file_path}")
else:
    file_id = asoc.upload(file_path)
    if file_id:
        out(f"Uploaded file ID: {file_id}")
