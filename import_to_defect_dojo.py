import requests
import sys
import os

def uploadToDefectDojo(is_new_import, token, url, product_name, engagement_name, scan_type, filename):
    multipart_form_data = {
        'file': (filename, open(filename, 'rb')),
        'scan_type': (None, scan_type),
        'product_name': (None, product_name),
        'engagement_name': (None, engagement_name),
    }

    endpoint = '/api/v2/import-scan/' if is_new_import else '/api/v2/reimport-scan/'
    r = requests.post(
        url + endpoint,
        files=multipart_form_data,
        headers={
            'Authorization': 'Token ' + token,
        }
    )
    if r.status_code != 200:
        sys.exit(f'Post failed: {r.text}')
    print(r.text)

if __name__ == "__main__":
    try:
        token = os.getenv("DEFECT_DOJO_API_TOKEN")
    except KeyError: 
        print("Please set the environment variable DEFECT_DOJO_API_TOKEN") 
        sys.exit(1)
    if len(sys.argv) == 11:
        url = sys.argv[2]
        product_name = sys.argv[4]
        engagement_name = sys.argv[6]
        scan_type = sys.argv[8]  # Corrected order
        report = sys.argv[10]
        uploadToDefectDojo(False, token, url, product_name, engagement_name, scan_type, report)  # Corrected order
    else:
        print(
            'Usage: python3 import_semgrep_to_defect_dojo.py --host DOJO_URL --product PRODUCT_NAME --engagement ENGAGEMENT_NAME --scan_type SCAN_TYPE --report REPORT_FILE')
