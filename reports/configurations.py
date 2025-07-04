"""
USAGE:

  cd /Users/s.hendrickson/Documents/OneDrive - F5, Inc
  python ~/Working/2023-08-23_project_visibility/bin/update_summary.py
  cat "./Project Folders/summary.csv"

# Locations
# SH Local Path: /Users/s.hendrickson/Documents/OneDrive - F5, Inc
# KW Local Path: /Users/ke.wilson/Desktop/test_data_accel
"""

import os

# Import Project Module(s) Below
from resources.path_utils import SystemInfo

"""
USAGE: 
    Path from SystemInfo() class is based on `os.environ['USER']` and the username following '/Users/' in system path.
    If `os.environ['USER']` & `/Users/[username]` match, AND the user is...
    ...Scott, then Scott's path: "/Users/s.hendrickson/Documents/OneDrive - F5, Inc"
    ...Keelor, then record option from user input:
          ...test: "/Users/ke.wilson/Desktop/test_data_accel"
          ...OneDrive: "/Users/ke.wilson/Library/CloudStorage/OneDrive-F5,Inc/Documents - Data Accelerator - Enterprise Analytics"
          ...other: path from user input()
    ...anyone else: path from user input()
"""

system_info = SystemInfo()
projects_tree_root = system_info.return_system_info()

project_folders_root = "Projects Folders"
project_info_filename = "PROJECT_INFO.txt"
projects_tree_project_folders = os.path.join(projects_tree_root, project_folders_root)
sharepoint_url = "https://f5.sharepoint.com/"
sharepoint_path = ":w:/r/sites/salesandmktg/mktg/Enterprise Analytics/Shared Documents/Projects Folders/"

# Files
summary_path = os.path.join(projects_tree_project_folders, "summary.csv")
analytics_summary_path = os.path.join(projects_tree_project_folders, "analytics_summary.csv")
data_product_links_path = os.path.join(projects_tree_project_folders, "data_product_links.md")
owner_views_active_path = os.path.join(projects_tree_project_folders, "owner_views_active.md")
owner_views_commit_path = os.path.join(projects_tree_project_folders, "owner_views_commit.md")
weekly_owner_views_active_path = os.path.join(projects_tree_project_folders, "weekly_owner_views_active.html")
owner_views_completed_path = os.path.join(projects_tree_project_folders, "owner_views_completed.md")
stakeholders_views_active_path = os.path.join(projects_tree_project_folders, "stakeholders_views_active.md")
title_phase_views_path = os.path.join(projects_tree_project_folders, "phase_views.md")
stakeholder_list_path = os.path.join(projects_tree_project_folders, "stakeholder_list.txt")


NOTES_DELIMITER = "**;**"
DATE_FMT = "%Y-%m-%d"

"""
These are the data elements to populate columns of the output csv for the status spreadsheet
  All-caps items are read from the project_info_file while normal case items are derived or computed.
"""

project_params_dict = {
    "Phases": None,
    "Project": None,
    "BUSINESS_SPONSOR": None,
    "ANALYTICS_DS_OWNER": None,
    "DATA_OFFICE_SPONSOR": None,
    "MISSION_ALIGNMENT": None,
    "T-SHIRT_SIZE": None,
    "Project Folder": None,
    "DATA_PRODUCT_LINK": None,
    "NOTES": None,
    "COMPUTED_AGE_DAYS": 0,
    "COMPUTED_IN_PROGRESS_AGE_DAYS": 0,
    "COMPUTED_PROJECT_START_DATE": None,
    "COMPUTED_PROJECT_IN_PROGRESS_DATE": None,
    "COMPUTED_PROJECT_ON_HOLD_DATE": None,
    "COMPUTED_PROJECT_ROLLOUT_DATE": None,
    "COMPUTED_PROJECT_END_DATE": None,
    "COMPUTED_PREVIOUS_PHASE": None,
    "COMMIT_JUSTIFICATIONS": None,
    "CharterLink": None,
# New Columns
    # MIN Date in Stage
    "COMPUTED_DATE_IN_STAGE_0_IDEAS": None,
    "COMPUTED_DATE_IN_STAGE_1_CHARTERING": None,
    "COMPUTED_DATE_IN_STAGE_2_COMMITTED": None,
    "COMPUTED_DATE_IN_STAGE_3_IN_PROGRESS": None,
    "COMPUTED_DATE_IN_STAGE_4_ON_HOLD": None,
    "COMPUTED_DATE_IN_STAGE_5_ROLLOUT": None,
    "COMPUTED_DATE_IN_STAGE_6_COMPLETED": None,
    "COMPUTED_DATE_IN_STAGE_7_MAINTENANCE": None,
    "COMPUTED_DATE_IN_STAGE_9_AD_HOC": None,
    # Days In Stage
    "COMPUTED_DAYS_IN_STAGE_0_IDEAS": None,
    "COMPUTED_DAYS_IN_STAGE_1_CHARTERING": None,
    "COMPUTED_DAYS_IN_STAGE_2_COMMITTED": None,
    "COMPUTED_DAYS_IN_STAGE_3_IN_PROGRESS": None,
    "COMPUTED_DAYS_IN_STAGE_4_ON_HOLD": None,
    "COMPUTED_DAYS_IN_STAGE_5_ROLLOUT": None,
    "COMPUTED_DAYS_IN_STAGE_6_COMPLETED": None,
    "COMPUTED_DAYS_IN_STAGE_7_MAINTENANCE": None,
    "COMPUTED_DAYS_IN_STAGE_9_AD_HOC": None,
    # Days Between Stages
    "COMPUTED_COMPLETION_TIME_DAYS": None,
    "COMPUTED_TIME_ON_HOLD_DAYS": None,
    "COMPUTED_IN_PROGRESS_TO_COMPLETION_DAYS": None,
    "COMPUTED_COMPLETION_TIME_MINUS_HOLD_DAYS": None,
    "COMPUTED_COMMIT_TO_COMPLETION_DAYS": None,
    "COMPUTED_CHARTER_TO_COMPLETION_DAYS": None,
# Metadata
    "Project_ID": None,
    "Report_Date": None,
}

"""
Map columns to data elements
  One entry for each of the project_params_dict keys
  Maps to the column name in the output csv
"""
name_field_map = {
    "Phases": "Phases",
    "Project": "Project",
    "Business Sponsor": "BUSINESS_SPONSOR",
    "Analytics-DS Owner": "ANALYTICS_DS_OWNER",
    "Data Office Sponsor": "DATA_OFFICE_SPONSOR",
    "Mission Alignment": "MISSION_ALIGNMENT",
    "T-shirt Size": "T-SHIRT_SIZE",
    "Project Folder": "Project Folder",
    "Data Product Link": "DATA_PRODUCT_LINK",
    "Notes": "NOTES",
    "Age": "COMPUTED_AGE_DAYS",
    "In Progress Age": "COMPUTED_IN_PROGRESS_AGE_DAYS",
    "Project Start Date": "COMPUTED_PROJECT_START_DATE",
    "Project In-Progress Date": "COMPUTED_PROJECT_IN_PROGRESS_DATE",
    "Project On-Hold Date": "COMPUTED_PROJECT_ON_HOLD_DATE",
    "Project Rollout Date": "COMPUTED_PROJECT_ROLLOUT_DATE",
    "Project Previous Phase": "COMPUTED_PROJECT_PREVIOUS_PHASE_DATE",
    "Project End Date": "COMPUTED_PROJECT_END_DATE",
    "Commit Justification": "COMMIT_JUSTIFICATIONS",
#New Columns
    # MIN Date in Stage
    "Stage 0 Ideas Date": "COMPUTED_DATE_IN_STAGE_0_IDEAS",
    "Stage 1 Chartering Date": "COMPUTED_DATE_IN_STAGE_1_CHARTERING",
    "Stage 2 Committed Date": "COMPUTED_DATE_IN_STAGE_2_COMMITTED",
    "Stage 3 In Progress Date": "COMPUTED_DATE_IN_STAGE_3_IN_PROGRESS",
    "Stage 4 On Hold Date": "COMPUTED_DATE_IN_STAGE_4_ON_HOLD",
    "Stage 5 Rollout Date": "COMPUTED_DATE_IN_STAGE_5_ROLLOUT",
    "Stage 6 Completed Date": "COMPUTED_DATE_IN_STAGE_6_COMPLETED",
    "Stage 7 Maintenance Date": "COMPUTED_DATE_IN_STAGE_7_MAINTENANCE",
    "Stage 9 Ad Hoc Date": "COMPUTED_DATE_IN_STAGE_9_AD_HOC",
    # Days In Stage
    "Stage 0 Ideas Age": "COMPUTED_DAYS_IN_STAGE_0_IDEAS",
    "Stage 1 Chartering Age": "COMPUTED_DAYS_IN_STAGE_1_CHARTERING",
    "Stage 2 Committed Age": "COMPUTED_DAYS_IN_STAGE_2_COMMITTED",
    "Stage 3 In Progress Age": "COMPUTED_DAYS_IN_STAGE_3_IN_PROGRESS",
    "Stage 4 On Hold Age": "COMPUTED_DAYS_IN_STAGE_4_ON_HOLD",
    "Stage 5 Rollout Age": "COMPUTED_DAYS_IN_STAGE_5_ROLLOUT",
    "Stage 6 Completed Age": "COMPUTED_DAYS_IN_STAGE_6_COMPLETED",
    "Stage 7 Maintenance Age": "COMPUTED_DAYS_IN_STAGE_7_MAINTENANCE",
    "Stage 9 Ad Hoc Age": "COMPUTED_DAYS_IN_STAGE_9_AD_HOC",
    # Days Between Stages
    "Days to Completion": "COMPUTED_COMPLETION_TIME_DAYS",
    "Days on Hold": "COMPUTED_TIME_ON_HOLD_DAYS",
    "Days In Progress to Complete": "COMPUTED_IN_PROGRESS_TO_COMPLETION_DAYS",
    "Days to Completion less On Hold": "COMPUTED_COMPLETION_TIME_MINUS_HOLD_DAYS",
    "Days Commit to Completion": "COMPUTED_COMMIT_TO_COMPLETION_DAYS",
    # Metadata
    "Project ID": "Project_ID",
    "Report Date": "Report_Date"
}

# keep a reverse map for lookup
field_name_map = {v: k for k, v in name_field_map.items()}

# phase-dependent attributes
project_phases = {
    "0-Ideas": 0,
    "1-Chartering": 1,
    "2-Committed": 2,
    "3-In Progress": 3,
    "4-On Hold": 4,
    "5-Rollout": 5,
    "6-Completed": 6,
    "7-Maintenance": 7,
    "9-Ad Hoc": 9  # Ad Hoc projects are treated as In Progress WRT ordering and active status
}
# keep a reverse map for lookup
index_project_phases = {v: k for k, v in project_phases.items()}

# Ordering determined by Data Accelerator Analysts for Owners Reports etc.
active_projects_order = [
    "3-In Progress",
    "9-Ad Hoc",
    "4-On Hold",
    "2-Committed",
    "1-Chartering",
    "5-Rollout"
]

# colors https://coolors.co/eef0f2-c6c7c4-a2999e-846a6a-353b3c
CSS_STYLE="""
<!DOCTYPE html>
<html>
<head>
<style>
body {
    background-color: #eef0f2; 
    margin: 20px 20px;
    font-family: Arial, Helvetica, sans-serif;
}
h1   {color: #846a6a;}
p    {color: #eef0f2;}
table {
  border: 1px solid #a2999e;
  border-collapse: collapse;
  padding: 8px;
}
th {
  height: 50px;
  background-color: #c6c7c4;
  font-size: large;
  font-color: #353b3c;
}
td {
  padding: 8px;
  font-size: medium;
  font-color: #353b3c;
  overflow-wrap: anywhere;
}
.tr-owner {
    height: 50px;
    background-color:#846a6a;
    font-size: large;
}
.tr-project {
    background-color:#a2999e;
}
span {
    font-size: small;
    font-weight: normal;
}
</style>
</head>
<body>

"""

HTML_FOOTER="""

</body>
</html>
"""

def size_repr(size_string):
    """
    Convert a size string to a standardized size representation.

    Parameters:
    size_string (str): A string representing the size, which can be "small", "medium",
                       "large", "extra large", etc., or their abbreviations.

    Returns:
    str: A standardized one-letter size representation ("S", "M", "L", "XL").
         Returns "Unsized" if the input does not match any recognized size.
    """
    # Trim and convert the input to lower case for standardization
    standardized_size = size_string.strip().lower()

    # Determine the size representation based on the first character
    if standardized_size.startswith("s"):
        return "S"
    elif standardized_size.startswith("m"):
        return "M"
    elif standardized_size.startswith("l"):
        return "L"
    elif standardized_size.startswith("x") or standardized_size.startswith("e"):
        return "XL"

    # Default return value for unrecognized sizes
    return "Unsized"


def order_strings_by_date(string_list):
    """
    Used for notes ordering in reports
        This works as desired if dates are yyyy-mm-dd format
    """
    res = sorted(string_list, reverse=True, key = lambda x: x[:16].replace("_","-"))
    return res
