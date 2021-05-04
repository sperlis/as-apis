
from asapis.services.aselib import ASE
from asapis.ase.aseEnums import JobActions
from asapis.ase.aseScanMonitor import monitor_scan_progress


def run_dast_scan(ase:ASE, job_id:str = None):
    do_job_action(ase, JobActions.run, job_id)
    if ase.config["ScanMonitor"]["Automatic"]:
        monitor_scan_progress(ase, job_id)

def do_job_action(ase:ASE, action:JobActions, job_id:str = None):
    if not job_id:
        job_id = job_id = ase.config["SubjectId"]

    res = ase.get(f"jobs/{job_id}")
    action = { "type": action.name }
    headers = {}
    headers["If-Match"] = res.headers["Etag"]
    res = ase.post(f"jobs/{job_id}/actions",json=action,headers=headers)
    if not res.ok:
        ase.print_response_error(res)

if __name__ == "__main__":
    ase = ASE()
    run_dast_scan(ase)
