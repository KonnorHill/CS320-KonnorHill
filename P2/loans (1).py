import json
import csv
import zipfile as z
import io


class Applicant:
    
    def __init__(self, age, race):
        self.age = age
        self.race = set()
        for r in race:
            if r in race_lookup:
                self.race.add(race_lookup[r])
    
    def __repr__(self):
        sorted_race = sorted(list(self.race))
        return f"Applicant('{self.age}', {sorted_race})"
    
    def lower_age(self):
        filtered_age = self.age.replace('<', '').replace('>', '')
        age_parts = filtered_age.split('-')
        return int(age_parts[0])
    
    def __lt__(self, other):
        return self.lower_age() < other.lower_age()


    
class Loan:
    
    def __init__(self, values):
        for attr in ['loan_amount', 'property_value', 'interest_rate']:
            try:
                setattr(self, attr, float(values.get(attr, -1)))
            except ValueError:
                setattr(self, attr, -1)
        applicant_races = [values.get(f"applicant_race-{n}", None) for n in range(1, 6)]
        applicant_races = [race for race in applicant_races if race is not None]
        applicants_list = [Applicant(values["applicant_age"], applicant_races)]
        if values["co-applicant_age"] != "9999":
            coapp_races = [values.get(f"co-applicant_race-{n}", None) for n in range(1, 6)]
            coapp_races = [race for race in coapp_races if race is not None]
            applicants_list.append(Applicant(values["co-applicant_age"], coapp_races))
        self.applicants = applicants_list
    
    def __str__(self):
        num_applicants = len(self.applicants)
        return f"<Loan: {self.interest_rate}% on ${self.property_value} with {num_applicants} applicant(s)>"
   
    def __repr__(self):
        return self.__str__()
    
    def yearly_amounts(self, yearly_payment):
        assert(self.interest_rate > 0 and self.loan_amount > 0)
        amt = self.loan_amount
        while amt > 0:
            yield amt
            amt += (self.interest_rate/100 * amt)
            amt -= yearly_payment

            

class Bank:
    def __init__(self, name):
        self.loans = []
        
        with open("banks.json") as f:
            data = f.read()
        for i in json.loads(data):
            if i["name"] == name:
                self.name = name
                self.lei = i["lei"]
                
        with z.ZipFile("wi.zip") as zf:
            with zf.open("wi.csv", "r") as file:
                reader = csv.DictReader(io.TextIOWrapper(file, "utf-8"))
                for row in reader:
                    if self.lei == row["lei"]:
                        l = Loan(row)
                        self.loans.append(l)
                        
    def __len__(self):
        return len(self.loans)
    
    def __getitem__(self, value):
        return self.loans[value]
                         
    
race_lookup = {
    "1": "American Indian or Alaska Native",
    "2": "Asian",
    "3": "Black or African American",
    "4": "Native Hawaiian or Other Pacific Islander",
    "5": "White",
    "21": "Asian Indian",
    "22": "Chinese",
    "23": "Filipino",
    "24": "Japanese",
    "25": "Korean",
    "26": "Vietnamese",
    "27": "Other Asian",
    "41": "Native Hawaiian",
    "42": "Guamanian or Chamorro",
    "43": "Samoan",
    "44": "Other Pacific Islander"
}



values = {'activity_year': '2021', 'lei': '549300Q76VHK6FGPX546', 'derived_msa-md': '24580', 'state_code': 'WI','county_code': '55009', 'census_tract': '55009020702', 'conforming_loan_limit': 'C', 'derived_loan_product_type': 'Conventional:First Lien', 'derived_dwelling_category': 'Single Family (1-4 Units):Site-Built', 'derived_ethnicity': 'Not Hispanic or Latino', 'derived_race': 'White', 'derived_sex': 'Joint', 'action_taken': '1', 'purchaser_type': '1', 'preapproval': '2', 'loan_type': '1', 'loan_purpose': '31', 'lien_status': '1', 'reverse_mortgage': '2', 'open-end_line_of_credit': '2', 'business_or_commercial_purpose': '2', 'loan_amount': '325000.0', 'loan_to_value_ratio': '73.409', 'interest_rate': '2.5', 'rate_spread': '0.304', 'hoepa_status': '2', 'total_loan_costs': '3932.75', 'total_points_and_fees': 'NA', 'origination_charges': '3117.5', 'discount_points': '', 'lender_credits': '', 'loan_term': '240', 'prepayment_penalty_term': 'NA', 'intro_rate_period': 'NA', 'negative_amortization': '2', 'interest_only_payment': '2', 'balloon_payment': '2', 'other_nonamortizing_features': '2', 'property_value': '445000', 'construction_method': '1', 'occupancy_type': '1', 'manufactured_home_secured_property_type': '3', 'manufactured_home_land_property_interest': '5', 'total_units': '1', 'multifamily_affordable_units': 'NA', 'income': '264', 'debt_to_income_ratio': '20%-<30%', 'applicant_credit_score_type': '2', 'co-applicant_credit_score_type': '9', 'applicant_ethnicity-1': '2', 'applicant_ethnicity-2': '', 'applicant_ethnicity-3': '', 'applicant_ethnicity-4': '', 'applicant_ethnicity-5': '', 'co-applicant_ethnicity-1': '2', 'co-applicant_ethnicity-2': '', 'co-applicant_ethnicity-3': '', 'co-applicant_ethnicity-4': '', 'co-applicant_ethnicity-5': '', 'applicant_ethnicity_observed': '2', 'co-applicant_ethnicity_observed': '2', 'applicant_race-1': '5', 'applicant_race-2': '', 'applicant_race-3': '', 'applicant_race-4': '', 'applicant_race-5': '', 'co-applicant_race-1': '5', 'co-applicant_race-2': '', 'co-applicant_race-3': '', 'co-applicant_race-4': '', 'co-applicant_race-5': '', 'applicant_race_observed': '2', 'co-applicant_race_observed': '2', 'applicant_sex': '1', 'co-applicant_sex': '2', 'applicant_sex_observed': '2', 'co-applicant_sex_observed': '2', 'applicant_age': '35-44', 'co-applicant_age': '35-44', 'applicant_age_above_62': 'No', 'co-applicant_age_above_62': 'No', 'submission_of_application': '1', 'initially_payable_to_institution': '1', 'aus-1': '1', 'aus-2': '', 'aus-3': '', 'aus-4': '', 'aus-5': '', 'denial_reason-1': '10', 'denial_reason-2': '', 'denial_reason-3': '', 'denial_reason-4': '', 'tract_population': '6839', 'tract_minority_population_percent': '8.85999999999999943', 'ffiec_msa_md_median_family_income': '80100', 'tract_to_msa_income_percentage': '150', 'tract_owner_occupied_units': '1701', 'tract_one_to_four_family_homes': '2056', 'tract_median_age_of_housing_units': '15'}