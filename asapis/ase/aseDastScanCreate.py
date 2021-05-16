from contextlib import suppress

from asapis.services.aselib import ASE
from asapis.services.aseInventory import NotFoundInventoryError
from asapis.utils.printUtil import logger
from asapis.ase.aseDastScanActions import run_dast_scan
from asapis.ase.aseDastScanConfig import config_dast_scan

ase = ASE()

# start a scan job, using a scant template as a base
job_details = ase.config["AseDastScan"]

test_policy = job_details["TestPolicy"]
test_policy = ase.inventory.get_test_policy_id(test_policy) # translate to ID from a name

folder = job_details["Folder"]
folder = ase.inventory.get_folder_id(folder) # translate to ID from a path

job_name = job_details["Name"]
description = job_details["Description"]
contact = job_details["Contact"]

model = {
  "testPolicyId": test_policy,
  "folderId": folder,
  "name": job_name,
  "description": description,
  "contact": contact
}

# Application is optional. If it's missing, ignore it. 
with suppress(NotFoundInventoryError):
    model["applicationId"] = ase.inventory.get_test_policy_id(job_details["Application"])

template_id = job_details["Template"]
template_id = ase.inventory.get_template_id(template_id)
res = ase.post(f"jobs/{template_id}/dastconfig/createjob",json=model)
if not res.ok:
    ase.print_response_error_and_exit(res)

job_info = res.json()

job_id = job_info["id"]

logger(f"Created scan job Folder Item ID: {job_id}")

if (job_details["AutoConfig"]):
  # Change new job configuration
  config_dast_scan(ase, job_id)

if (job_details["AutoRun"]):
  # Run the job
  run_dast_scan(ase, job_id)
