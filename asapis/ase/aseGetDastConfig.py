from asapis.services.aselib import ASE
from asapis.utils.printUtil import logger

ase = ASE()

job_id = ase.config["SubjectId"]

file_path = ase.config["Destination"]

ase.download(f"jobs/{job_id}/dastconfig",file_path)

logger(F"Report downloaded to {file_path}")
