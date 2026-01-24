"""
A1クエリの検証
Query Validator for Assignment 1
"""

from sample_database import PharmacyDatabase
from relational_algebra import RelationalAlgebra, print_relation
from typing import Set, Tuple


class QueryValidator:
    """各クエリを実装して検証"""
    
    def __init__(self, db: PharmacyDatabase):
        self.db = db
        self.ra = RelationalAlgebra()
    
    def query1_frugal_doctors(self) -> Set[Tuple]:
        """
        Query 1: Frugal doctors
        最安値のジェネリックまたは代替なしブランド薬のみを処方する医師
        """
        print("\n" + "=" * 70)
        print("QUERY 1: Frugal Doctors")
        print("=" * 70)
        
        # All drugs with recorded prices
        AllPricedDrugs = self.ra.project(self.db.Price, [0])
        print_relation("AllPricedDrugs", AllPricedDrugs, ['DIN'])
        
        # Brand-name drugs with at least one generic alternative
        BrandWithGeneric = self.ra.project(self.db.Generic, [1])
        print_relation("BrandWithGeneric", BrandWithGeneric, ['brand'])
        
        # Brand-name drugs with no generic alternative
        all_brands = self.ra.project(self.db.Product, [0])
        BrandWithoutGeneric = self.ra.difference(all_brands, BrandWithGeneric)
        print_relation("BrandWithoutGeneric", BrandWithoutGeneric, ['DIN'])
        
        # Generics with prices
        GenericWithPrice = {
            (g[0], g[1], p[1])  # DIN, brand, price
            for g in self.db.Generic
            for p in self.db.Price
            if g[0] == p[0]
        }
        print_relation("GenericWithPrice", GenericWithPrice, ['DIN', 'brand', 'price'])
        
        # Find generics that are NOT cheapest (more expensive than another generic of same brand)
        NotCheapestGeneric = set()
        for g1 in GenericWithPrice:
            for g2 in GenericWithPrice:
                if g1[1] == g2[1] and g1[0] != g2[0] and g1[2] > g2[2]:
                    NotCheapestGeneric.add((g1[0],))
        print_relation("NotCheapestGeneric", NotCheapestGeneric, ['DIN'])
        
        # Cheapest generics
        all_generics = self.ra.project(GenericWithPrice, [0])
        CheapestGeneric = self.ra.difference(all_generics, NotCheapestGeneric)
        print_relation("CheapestGeneric", CheapestGeneric, ['DIN'])
        
        # Priced brands without generics
        PricedBrandWithoutGeneric = self.ra.intersection(BrandWithoutGeneric, AllPricedDrugs)
        print_relation("PricedBrandWithoutGeneric", PricedBrandWithoutGeneric, ['DIN'])
        
        # Acceptable drugs
        AcceptableDrugs = self.ra.union(CheapestGeneric, PricedBrandWithoutGeneric)
        print_relation("AcceptableDrugs", AcceptableDrugs, ['DIN'])
        
        # Doctors who prescribed unacceptable drugs
        DoctorsWithBadPrescriptions = set()
        for p in self.db.Prescription:
            drug_din = (p[3],)
            if drug_din not in AcceptableDrugs:
                DoctorsWithBadPrescriptions.add((p[4],))
        print_relation("DoctorsWithBadPrescriptions", DoctorsWithBadPrescriptions, ['doctor'])
        
        # Doctors and their distinct drugs
        DoctorDrugs = self.ra.project(
            {(p[4], p[3]) for p in self.db.Prescription}, [0, 1]
        )
        print_relation("DoctorDrugs", DoctorDrugs, ['doctor', 'drug'])
        
        # Doctors who prescribed at least 2 different drugs
        DoctorsWithTwoOrMoreDrugs = set()
        doctor_drug_dict = {}
        for dd in DoctorDrugs:
            doctor, drug = dd
            if doctor not in doctor_drug_dict:
                doctor_drug_dict[doctor] = set()
            doctor_drug_dict[doctor].add(drug)
        
        for doctor, drugs in doctor_drug_dict.items():
            if len(drugs) >= 2:
                DoctorsWithTwoOrMoreDrugs.add((doctor,))
        print_relation("DoctorsWithTwoOrMoreDrugs", DoctorsWithTwoOrMoreDrugs, ['doctor'])
        
        # All eligible doctors (prescribed at least one priced drug)
        AllEligibleDoctors = set()
        for p in self.db.Prescription:
            if (p[3],) in AllPricedDrugs:
                AllEligibleDoctors.add((p[4],))
        print_relation("AllEligibleDoctors", AllEligibleDoctors, ['doctor'])
        
        # Frugal doctors
        FrugalDoctors = AllEligibleDoctors - DoctorsWithBadPrescriptions
        FrugalDoctors = FrugalDoctors & DoctorsWithTwoOrMoreDrugs
        
        print("\n" + "-" * 70)
        print("RESULT: Frugal Doctors")
        print_relation("FrugalDoctors", FrugalDoctors, ['doctor'])
        
        return FrugalDoctors
    
    def query2_doctor_shopping(self) -> Set[Tuple]:
        """
        Query 2: Potential doctor shopping
        異なる医師から同等の薬を処方された患者
        """
        print("\n" + "=" * 70)
        print("QUERY 2: Potential Doctor Shopping")
        print("=" * 70)
        
        # Create all equivalent drug pairs
        EquivalentDrugs = set()
        
        # Case 1: Same DIN (trivial)
        all_dins = self.ra.project(self.db.Product, [0]) | self.ra.project(self.db.Generic, [0])
        for din in all_dins:
            EquivalentDrugs.add((din[0], din[0]))
        
        # Case 2: Brand and its generic
        for g in self.db.Generic:
            EquivalentDrugs.add((g[1], g[0]))  # brand -> generic
            EquivalentDrugs.add((g[0], g[1]))  # generic -> brand
        
        # Case 3: Two generics sharing same brand
        for g1 in self.db.Generic:
            for g2 in self.db.Generic:
                if g1[1] == g2[1] and g1[0] != g2[0]:
                    EquivalentDrugs.add((g1[0], g2[0]))
        
        print_relation("EquivalentDrugs (sample)", 
                      set(list(EquivalentDrugs)[:10]), ['DIN1', 'DIN2'])
        
        # Find patients prescribed equivalent meds by different doctors
        PatientsDoctorShopping = set()
        for p1 in self.db.Prescription:
            for p2 in self.db.Prescription:
                if (p1[2] == p2[2] and  # same patient
                    p1[4] != p2[4] and  # different doctors
                    (p1[3], p2[3]) in EquivalentDrugs):  # equivalent drugs
                    PatientsDoctorShopping.add((p1[2],))
        
        print_relation("PatientsDoctorShopping", PatientsDoctorShopping, ['patient'])
        
        # Get patient details
        Result = set()
        for patient_ohip in PatientsDoctorShopping:
            for patient in self.db.Patient:
                if patient[0] == patient_ohip[0]:
                    Result.add((patient[0], patient[1], patient[3]))
        
        print("\n" + "-" * 70)
        print("RESULT: Patients at Risk of Doctor Shopping")
        print_relation("Result", Result, ['OHIP', 'name', 'phone'])
        
        return Result
    
    def query3_safest_ingredient(self) -> Set[Tuple]:
        """
        Query 3: Safest ingredient
        他成分との相互作用が最少の成分
        """
        print("\n" + "=" * 70)
        print("QUERY 3: Safest Ingredient")
        print("=" * 70)
        
        # Count interactions per ingredient
        interaction_count = {}
        for ing in self.db.ActiveIngredient:
            ingredient = ing[0]
            count = 0
            for inter in self.db.Interaction:
                if inter[0] == ingredient or inter[1] == ingredient:
                    count += 1
            interaction_count[ingredient] = count
        
        print("\nInteraction counts:")
        for ing, count in sorted(interaction_count.items()):
            print(f"  {ing}: {count} interactions")
        
        # Find minimum count
        min_count = min(interaction_count.values())
        SafestIngredients = {(ing,) for ing, count in interaction_count.items() 
                           if count == min_count}
        
        print("\n" + "-" * 70)
        print(f"RESULT: Safest Ingredients (with {min_count} interactions)")
        print_relation("SafestIngredients", SafestIngredients, ['name'])
        
        return SafestIngredients
    
    def query4_drug_shortage(self) -> Set[Tuple]:
        """
        Query 4: Drug shortage
        未調剤処方が3件以上で2人以上の患者
        """
        print("\n" + "=" * 70)
        print("QUERY 4: Drug Shortage")
        print("=" * 70)
        
        # Unfilled prescriptions
        filled_rx_ids = {f[0] for f in self.db.Filled}
        UnfilledPrescriptions = {
            (p[0], p[3], p[2])  # RxID, drug, patient
            for p in self.db.Prescription
            if p[0] not in filled_rx_ids
        }
        print_relation("UnfilledPrescriptions", UnfilledPrescriptions, 
                      ['RxID', 'drug', 'patient'])
        
        # Count unfilled prescriptions per drug
        drug_unfilled_count = {}
        drug_patients = {}
        for uf in UnfilledPrescriptions:
            drug = uf[1]
            patient = uf[2]
            drug_unfilled_count[drug] = drug_unfilled_count.get(drug, 0) + 1
            if drug not in drug_patients:
                drug_patients[drug] = set()
            drug_patients[drug].add(patient)
        
        print("\nUnfilled prescription counts:")
        for drug, count in sorted(drug_unfilled_count.items()):
            print(f"  Drug {drug}: {count} unfilled, {len(drug_patients[drug])} patients")
        
        # Drugs in shortage (>= 3 unfilled, >= 2 patients)
        DrugShortage = {
            drug for drug, count in drug_unfilled_count.items()
            if count >= 3 and len(drug_patients[drug]) >= 2
        }
        
        # Get manufacturer info
        all_drug_info = {(p[0], p[2]) for p in self.db.Product}  # DIN, manufacturer
        all_drug_info |= {(g[0], g[3]) for g in self.db.Generic}  # DIN, manufacturer
        
        Result = {
            (drug, mfr) for drug, mfr in all_drug_info
            if drug in DrugShortage
        }
        
        print("\n" + "-" * 70)
        print("RESULT: Drugs in Shortage")
        print_relation("Result", Result, ['DIN', 'manufacturer'])
        
        return Result
    
    def query6_patients_at_risk(self) -> Set[Tuple]:
        """
        Query 6: Patients at risk
        同日に相互作用する薬を処方された患者
        """
        print("\n" + "=" * 70)
        print("QUERY 6: Patients at Risk (Interacting Drugs)")
        print("=" * 70)
        
        # Get ingredients for all drugs (brand and generic)
        AllDrugIngredients = {}
        
        # Brand drugs
        for c in self.db.Contains:
            din, ingredient = c[0], c[1]
            if din not in AllDrugIngredients:
                AllDrugIngredients[din] = set()
            AllDrugIngredients[din].add(ingredient)
        
        # Generic drugs (use brand's ingredients)
        for g in self.db.Generic:
            generic_din, brand_din = g[0], g[1]
            if brand_din in AllDrugIngredients:
                AllDrugIngredients[generic_din] = AllDrugIngredients[brand_din]
        
        print("Drug ingredients:")
        for din, ingredients in sorted(AllDrugIngredients.items())[:5]:
            print(f"  Drug {din}: {ingredients}")
        
        # All interactions (both directions)
        AllInteractions = set()
        for inter in self.db.Interaction:
            AllInteractions.add((inter[0], inter[1]))
            AllInteractions.add((inter[1], inter[0]))  # Ensure symmetry
        
        # Find prescriptions on same day by same doctor
        Result = set()
        for p1 in self.db.Prescription:
            for p2 in self.db.Prescription:
                if (p1[4] == p2[4] and  # same doctor
                    p1[2] == p2[2] and  # same patient
                    p1[1] == p2[1] and  # same date
                    p1[0] != p2[0]):    # different prescriptions
                    
                    # Check if drugs interact
                    drug1, drug2 = p1[3], p2[3]
                    if drug1 in AllDrugIngredients and drug2 in AllDrugIngredients:
                        for ing1 in AllDrugIngredients[drug1]:
                            for ing2 in AllDrugIngredients[drug2]:
                                if (ing1, ing2) in AllInteractions:
                                    Result.add((p1[4], p1[1]))  # doctor, date
        
        print("\n" + "-" * 70)
        print("RESULT: Doctors who prescribed interacting drugs")
        print_relation("Result", Result, ['doctor', 'date'])
        
        return Result
    
    def query7_many_generics(self) -> Set[Tuple]:
        """
        Query 7: Many generics
        ジェネリック薬の調剤数が最多の薬剤師
        """
        print("\n" + "=" * 70)
        print("QUERY 7: Pharmacist with Most Generic Fills")
        print("=" * 70)
        
        # Generic DINs
        GenericDINs = {g[0] for g in self.db.Generic}
        print_relation("GenericDINs", {(d,) for d in GenericDINs}, ['DIN'])
        
        # Count generic fills per pharmacist
        pharmacist_generic_count = {}
        pharmacist_last_date = {}
        
        for f in self.db.Filled:
            rx_id, date, pharmacist = f
            # Check if this prescription is for a generic
            for p in self.db.Prescription:
                if p[0] == rx_id and p[3] in GenericDINs:
                    pharmacist_generic_count[pharmacist] = \
                        pharmacist_generic_count.get(pharmacist, 0) + 1
                    # Track last date
                    if pharmacist not in pharmacist_last_date:
                        pharmacist_last_date[pharmacist] = date
                    else:
                        pharmacist_last_date[pharmacist] = \
                            max(pharmacist_last_date[pharmacist], date)
                    break
        
        print("\nGeneric fill counts:")
        for pharm, count in sorted(pharmacist_generic_count.items()):
            print(f"  Pharmacist {pharm}: {count} generic fills")
        
        # Find max count
        if pharmacist_generic_count:
            max_count = max(pharmacist_generic_count.values())
            TopPharmacists = {
                pharm for pharm, count in pharmacist_generic_count.items()
                if count == max_count
            }
            
            Result = {
                (pharm, pharmacist_last_date.get(pharm, 'N/A'))
                for pharm in TopPharmacists
            }
        else:
            Result = set()
        
        print("\n" + "-" * 70)
        print("RESULT: Pharmacist(s) with most generic fills")
        print_relation("Result", Result, ['OCP', 'last_date'])
        
        return Result


def run_all_queries():
    """全クエリを実行"""
    print("=" * 70)
    print("PHARMACY DATABASE QUERY VALIDATOR")
    print("Assignment 1 - CSC343")
    print("=" * 70)
    
    # データベースを作成
    db = PharmacyDatabase()
    db.print_summary()
    
    # バリデータを作成
    validator = QueryValidator(db)
    
    # 各クエリを実行
    queries = [
        ("Query 1: Frugal Doctors", validator.query1_frugal_doctors),
        ("Query 2: Doctor Shopping", validator.query2_doctor_shopping),
        ("Query 3: Safest Ingredient", validator.query3_safest_ingredient),
        ("Query 4: Drug Shortage", validator.query4_drug_shortage),
        ("Query 6: Patients at Risk", validator.query6_patients_at_risk),
        ("Query 7: Many Generics", validator.query7_many_generics),
    ]
    
    results = {}
    for name, query_func in queries:
        try:
            result = query_func()
            results[name] = result
        except Exception as e:
            print(f"\n❌ ERROR in {name}: {e}")
            results[name] = None
    
    # サマリー
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    for name, result in results.items():
        if result is not None:
            print(f"✓ {name}: {len(result)} result(s)")
        else:
            print(f"✗ {name}: Failed")


if __name__ == "__main__":
    run_all_queries()
