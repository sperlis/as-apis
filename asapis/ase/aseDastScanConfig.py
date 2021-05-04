

from asapis.services.aselib import ASE
from asapis.services.aseModelsFactory import to_dast_config_models


def config_dast_scan(ase:ASE, job_id:str = None, configs_array:list = None):
    if not configs_array:
        configs_array = ase.config["AseDastScan"]["Configuration"]
    if not job_id:
        job_id = ase.config["SubjectId"]
    configs = to_dast_config_models(configs_array)
    for config in configs:
        res = ase.post(f"jobs/{job_id}/dastconfig/updatescant",json=config)
        if not res.ok:
            ase.print_response_error_and_exit(res)


if __name__ == "__main__":
    ase = ASE()
    config_dast_scan(ase)