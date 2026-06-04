_pyder_project = [
    {
        "projectName": "EWgent",
        "domainSystem": "dev.pages.codedave",
        "projectID": "ewgent",
        "packageManager": "pnpm",
        "version": "0.1.0",
        "window": {
            "minSize": [1000, 600],
            "initSize": [1000, 600]
        }
    }
]

pyder_projectName = _pyder_project[0]["projectName"]
pyder_domainSystem = _pyder_project[0]["domainSystem"]
pyder_projectID = _pyder_project[0]["projectID"]
pyder_packageManager = _pyder_project[0]["packageManager"]
pyder_version = _pyder_project[0]["version"]

pyder_window = _pyder_project[0]["window"]
pyder_window_minSize_v1, pyder_window_minSize_v2 = pyder_window["minSize"]
pyder_window_initSize_v1, pyder_window_initSize_v2 = pyder_window["initSize"]