import random
import pandas as pd
from datetime import datetime, timedelta

# ==================================================
# Duplicate MRN Analytics Platform
# Synthetic Dataset Generator
# Version 1.0
# ==================================================

random.seed(42)

# ==================================================
# LOOKUP TABLES
# ==================================================

departments = [
    {"department_id": 1, "department_name": "Primary Care", "service_line": "Ambulatory"},
    {"department_id": 2, "department_name": "Emergency Department", "service_line": "Emergency"},
    {"department_id": 3, "department_name": "Urgent Care", "service_line": "Ambulatory"},
    {"department_id": 4, "department_name": "Radiology", "service_line": "Ancillary"},
    {"department_id": 5, "department_name": "Lab", "service_line": "Ancillary"},
    {"department_id": 6, "department_name": "Surgery", "service_line": "Surgical Services"},
    {"department_id": 7, "department_name": "Specialty Clinic", "service_line": "Ambulatory"},
    {"department_id": 8, "department_name": "Behavioral Health", "service_line": "Behavioral Health"},
    {"department_id": 9, "department_name": "Rehabilitation", "service_line": "Rehabilitation"},
    {"department_id": 10, "department_name": "Self-Schedule", "service_line": "Patient Portal"}
]

source_types = [
    {"source_id": 1, "source_name": "Self-Schedule"},
    {"source_id": 2, "source_name": "Internal Registration"},
    {"source_id": 3, "source_name": "External Provider"}
]

factor_definitions = [
    {"factor_id": 1, "factor_type": "Data Entry Error", "primary_category": "Patient Name", "specific_cause": "Guardian entered own name"},
    {"factor_id": 2, "factor_type": "Data Entry Error", "primary_category": "Patient Name", "specific_cause": "Sibling name entered"},
    {"factor_id": 3, "factor_type": "Data Entry Error", "primary_category": "Patient Name", "specific_cause": "Name typo"},
    {"factor_id": 4, "factor_type": "Data Entry Error", "primary_category": "Patient Name", "specific_cause": "Transposed first/last name"},
    {"factor_id": 5, "factor_type": "Data Entry Error", "primary_category": "Patient Name", "specific_cause": "Referring provider name entered as patient name"},
    {"factor_id": 6, "factor_type": "Data Entry Error", "primary_category": "Date of Birth", "specific_cause": "Guardian entered own DOB"},
    {"factor_id": 7, "factor_type": "Data Entry Error", "primary_category": "Date of Birth", "specific_cause": "Sibling DOB entered"},
    {"factor_id": 8, "factor_type": "Data Entry Error", "primary_category": "Date of Birth", "specific_cause": "DOB typo"},
    {"factor_id": 9, "factor_type": "Data Entry Error", "primary_category": "Date of Birth", "specific_cause": "Transposed DOB"},
    {"factor_id": 10, "factor_type": "Data Entry Error", "primary_category": "Date of Birth", "specific_cause": "Entered current date as DOB"},
    {"factor_id": 11, "factor_type": "Data Entry Error", "primary_category": "Sex/Gender", "specific_cause": "Guardian entered own legal sex"},
    {"factor_id": 12, "factor_type": "Data Entry Error", "primary_category": "Sex/Gender", "specific_cause": "Sibling legal sex entered"},
    {"factor_id": 13, "factor_type": "Data Entry Error", "primary_category": "Contact Information", "specific_cause": "Address typo"},
    {"factor_id": 14, "factor_type": "Demographic Change", "primary_category": "Patient Name", "specific_cause": "Legal name changed"},
    {"factor_id": 15, "factor_type": "Demographic Change", "primary_category": "Sex/Gender", "specific_cause": "Legal sex changed"},
    {"factor_id": 16, "factor_type": "Demographic Change", "primary_category": "Contact Information", "specific_cause": "Address changed"},
    {"factor_id": 17, "factor_type": "Demographic Change", "primary_category": "Contact Information", "specific_cause": "Phone number changed"},
    {"factor_id": 18, "factor_type": "Alternative Identity", "primary_category": "Sex/Gender", "specific_cause": "Preferred sex entered"},
    {"factor_id": 19, "factor_type": "Registration Information", "primary_category": "Demographics/Registration", "specific_cause": "Incomplete demographics"}
]

factor_lookup = {
    factor["specific_cause"]: factor
    for factor in factor_definitions
}

# ==================================================
# WEIGHT TABLES
# ==================================================

source_department_weights = {
    "Self-Schedule": {
        "Urgent Care": 70,
        "Behavioral Health": 30
    },
    "Internal Registration": {
        "Primary Care": 25,
        "Emergency Department": 25,
        "Radiology": 15,
        "Lab": 15,
        "Surgery": 10,
        "Specialty Clinic": 10
    },
    "External Provider": {
        "Primary Care": 35,
        "Specialty Clinic": 35,
        "Radiology": 15,
        "Lab": 15
    }
}

source_cause_weights = {
    "Self-Schedule": {
        "Guardian entered own name": 25,
        "Guardian entered own DOB": 25,
        "Sibling name entered": 15,
        "Sibling DOB entered": 15,
        "Name typo": 10,
        "DOB typo": 10
    },
    "Internal Registration": {
        "Name typo": 20,
        "DOB typo": 20,
        "Transposed first/last name": 15,
        "Transposed DOB": 15,
        "Address typo": 10,
        "Incomplete demographics": 20
    },
    "External Provider": {
        "Referring provider name entered as patient name": 30,
        "Name typo": 20,
        "DOB typo": 20,
        "Incomplete demographics": 20,
        "Address typo": 10
    }
}

# ==================================================
# BUSINESS RULES
# ==================================================

mutually_exclusive_groups = [
    [
        "Guardian entered own name",
        "Sibling name entered",
        "Preferred name entered",
        "Legal name changed",
        "Name typo",
        "Transposed first/last name",
        "Referring provider name entered as patient name"
    ],
    [
        "Guardian entered own DOB",
        "Sibling DOB entered",
        "DOB typo",
        "Transposed DOB",
        "Entered current date as DOB"
    ],
    [
        "Guardian entered own legal sex",
        "Sibling legal sex entered",
        "Legal sex changed"
    ]
]

# ==================================================
# HELPER FUNCTIONS
# ==================================================

def causes_conflict(cause, selected_causes):
    for group in mutually_exclusive_groups:
        if cause in group:
            for selected in selected_causes:
                if selected in group:
                    return True
    return False


def choose_source():
    selected_source = random.choices(
        source_types,
        weights=[50, 40, 10],
        k=1
    )[0]

    return selected_source["source_name"]


def choose_department(source):
    possible_departments = list(source_department_weights[source].keys())
    weights = list(source_department_weights[source].values())

    selected_department_name = random.choices(
        possible_departments,
        weights=weights,
        k=1
    )[0]

    for department in departments:
        if department["department_name"] == selected_department_name:
            return department

    raise ValueError(f"Department not found: {selected_department_name}")


def generate_contributing_factors(source_name):
    possible_causes = list(source_cause_weights[source_name].keys())
    weights = list(source_cause_weights[source_name].values())

    number_of_factors = random.choices(
        [1, 2],
        weights=[70, 30],
        k=1
    )[0]

    selected_causes = []
    attempts = 0

    while len(selected_causes) < number_of_factors and attempts < 50:
        selected_cause = random.choices(
            possible_causes,
            weights=weights,
            k=1
        )[0]

        if (
            selected_cause not in selected_causes
            and not causes_conflict(selected_cause, selected_causes)
        ):
            selected_causes.append(selected_cause)

        attempts += 1

    return selected_causes


def choose_status():
    return random.choices(
        ["Resolved", "Open"],
        weights=[95, 5],
        k=1
    )[0]


def choose_resolution_type(status):
    if status == "Open":
        return None

    return random.choices(
        ["Merge", "KND"],
        weights=[75, 25],
        k=1
    )[0]


def generate_event_date(start_date, end_date):
    date_range = end_date - start_date
    random_days = random.randint(0, date_range.days)

    return start_date + timedelta(days=random_days)


def generate_duplicate_event(duplicate_id):
    source = choose_source()
    department = choose_department(source)
    contributing_factors = generate_contributing_factors(source)

    factor_types = sorted({
        factor_lookup[f]["factor_type"]
        for f in contributing_factors
    })

    primary_category = factor_lookup[
        contributing_factors[0]
    ]["primary_category"]

    status = choose_status()
    resolution_type = choose_resolution_type(status)

    event_date = generate_event_date(
        datetime(2025, 1, 1),
        datetime(2025, 12, 31)
    )

    return {
        "duplicate_id": duplicate_id,
        "event_date": event_date.strftime("%Y-%m-%d"),
        "source": source,
        "department_id": department["department_id"],
        "department_name": department["department_name"],
        "service_line": department["service_line"],
        "contributing_factors": "; ".join(contributing_factors),
        "contributing_factor_types": "; ".join(factor_types),
        "primary_category": primary_category,
        "status": status,
        "resolution_type": resolution_type
    }


# ==================================================
# DATASET GENERATION
# ==================================================

duplicate_events = []

for i in range(1, 1001):
    duplicate_events.append(generate_duplicate_event(i))

df = pd.DataFrame(duplicate_events)

df.to_csv("duplicate_events.csv", index=False)

print("Dataset created successfully!")

# ==================================================
# DATA VALIDATION
# ==================================================

print("\nSample Contributing Factors")
print(df[[
    "contributing_factors",
    "contributing_factor_types",
    "primary_category"
]].head(10))

print("\nSource Distribution")
print(df["source"].value_counts())

print("\nSource Percentages")
print(df["source"].value_counts(normalize=True))

print("\nDepartment Distribution")
print(df["department_name"].value_counts())

print("\nService Line Distribution")
print(df["service_line"].value_counts())

print("\nContributing Factor Type Distribution")
print(df["contributing_factor_types"].value_counts())

print("\nPrimary Category Distribution")
print(df["primary_category"].value_counts())