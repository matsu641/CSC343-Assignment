"""
薬局データベースのサンプルデータ
Sample Pharmacy Database Instance
"""

from typing import Set, Tuple


class PharmacyDatabase:
    """薬局データベースのサンプルインスタンス"""
    
    # 各リレーションの主キー（列のインデックス）
    PRIMARY_KEYS = {
        'Product': [0],              # DIN
        'Generic': [0],              # DIN
        'Price': [0],                # DIN
        'ActiveIngredient': [0],     # name
        'Contains': [0, 1],          # DIN, ingredient (複合キー)
        'Interaction': [0, 1],       # ingredient1, ingredient2 (複合キー)
        'Patient': [0],              # OHIP
        'Pharmacist': [0],           # OCP
        'Prescription': [0],         # RxID
        'Filled': [0],               # RxID
    }
    
    def __init__(self):
        # Product(DIN, name, manufacturer, form, schedule, route)
        self.Product = {
            (1001, 'Brufin', 'Boots UK', 'tablet', 'OTC', 'oral'),
            (1002, 'Painex', 'PharmaCo', 'capsule', 'prescription', 'oral'),
            (1003, 'Sleepwell', 'RestPharma', 'tablet', 'prescription', 'oral'),
            (1004, 'VitaBoost', 'HealthCorp', 'capsule', 'OTC', 'oral'),
            (1005, 'StrongBone', 'BoneCare Inc', 'tablet', 'OTC', 'oral'),
        }
        
        # Generic(DIN, brand, name, manufacturer)
        self.Generic = {
            (2001, 1001, 'Ibuprofen', 'GenericMeds'),    # Generic of Brufin
            (2002, 1001, 'Advil', 'PainRelief Inc'),     # Another generic of Brufin
            (2003, 1002, 'GenericPain', 'CheapMeds'),    # Generic of Painex
            (2004, 1003, 'GenericSleep', 'BudgetPharma'), # Generic of Sleepwell
            (2005, 1003, 'NightRest', 'SleepEasy Co'),   # Another generic of Sleepwell
        }
        
        # Price(DIN, price)
        self.Price = {
            # Brand prices
            (1001, 15.00),
            (1002, 25.00),
            (1003, 30.00),
            (1004, 10.00),
            (1005, 12.00),
            # Generic prices
            (2001, 8.00),   # Cheapest generic of Brufin
            (2002, 8.00),   # Tied for cheapest
            (2003, 18.00),  # Generic of Painex
            (2004, 20.00),  # More expensive generic
            (2005, 15.00),  # Cheaper generic of Sleepwell
        }
        
        # ActiveIngredient(name)
        self.ActiveIngredient = {
            ('ibuprofen',),
            ('acetaminophen',),
            ('diphenhydramine',),
            ('melatonin',),
            ('calcium',),
            ('vitamin_d',),
        }
        
        # Contains(DIN, ingredient, strength, unit)
        self.Contains = {
            # Brand drugs
            (1001, 'ibuprofen', 200, 'mg'),
            (1002, 'acetaminophen', 500, 'mg'),
            (1003, 'diphenhydramine', 25, 'mg'),
            (1003, 'melatonin', 3, 'mg'),
            (1004, 'vitamin_d', 1000, 'IU'),
            (1005, 'calcium', 500, 'mg'),
            (1005, 'vitamin_d', 400, 'IU'),
        }
        
        # Interaction(ingredient1, ingredient2)
        self.Interaction = {
            ('ibuprofen', 'acetaminophen'),
            ('acetaminophen', 'ibuprofen'),  # Symmetry
            ('diphenhydramine', 'melatonin'),
            ('melatonin', 'diphenhydramine'),  # Symmetry
        }
        
        # Patient(OHIP, name, dob, phone, address)
        self.Patient = {
            (100001, 'John Smith', '1980-05-15', '416-555-0001', '123 Main St'),
            (100002, 'Jane Doe', '1975-08-22', '416-555-0002', '456 Oak Ave'),
            (100003, 'Bob Johnson', '1990-03-10', '416-555-0003', '789 Pine Rd'),
            (100004, 'Alice Williams', '1985-11-30', '416-555-0004', '321 Elm St'),
        }
        
        # Pharmacist(OCP, name, registered)
        self.Pharmacist = {
            (5001, 'Dr. Sarah Lee', '2010-01-15'),
            (5002, 'Dr. Mike Chen', '2015-06-20'),
            (5003, 'Dr. Emily White', '2018-09-01'),
        }
        
        # Prescription(RxID, date, patient, drug, doctor, dosage, note)
        self.Prescription = {
            # Doctor 101 - Frugal doctor (only prescribes cheapest generics or brands without generics)
            (3001, '2025-01-10', 100001, 2001, 101, '200mg twice daily', ''),  # Cheapest generic
            (3002, '2025-01-15', 100002, 1004, 101, 'once daily', ''),         # Brand without generic
            
            # Doctor 102 - Not frugal (prescribes expensive brand with generics)
            (3003, '2025-01-12', 100001, 1001, 102, '200mg as needed', ''),    # Brand with cheaper generics
            (3004, '2025-01-14', 100003, 2003, 102, '500mg twice daily', ''),  # Generic
            
            # Doctor 103 - Potential doctor shopping scenario
            (3005, '2025-01-20', 100002, 1001, 103, '200mg twice daily', ''),  # Brand Brufin
            (3006, '2025-01-22', 100002, 2001, 104, '200mg twice daily', ''),  # Generic of Brufin (different doctor!)
            
            # Same day interacting prescriptions by Doctor 105
            (3007, '2025-02-01', 100003, 1002, 105, '500mg as needed', ''),    # Acetaminophen
            (3008, '2025-02-01', 100003, 1001, 105, '200mg as needed', ''),    # Ibuprofen (interacts!)
            
            # Unfilled prescriptions for drug shortage
            (3009, '2025-02-05', 100001, 1003, 106, 'once at bedtime', ''),    # Unfilled
            (3010, '2025-02-06', 100002, 1003, 106, 'once at bedtime', ''),    # Unfilled
            (3011, '2025-02-07', 100003, 1003, 106, 'once at bedtime', ''),    # Unfilled
            
            # Generic prescriptions
            (3012, '2025-01-25', 100004, 2001, 107, '200mg twice daily', ''),  # Generic
            (3013, '2025-01-26', 100001, 2002, 107, '200mg twice daily', ''),  # Generic
            (3014, '2025-01-27', 100002, 2004, 107, 'once at bedtime', ''),    # Generic
        }
        
        # Filled(RxID, date, pharmacist)
        self.Filled = {
            (3001, '2025-01-11', 5001),
            (3002, '2025-01-16', 5001),
            (3003, '2025-01-13', 5002),
            (3004, '2025-01-15', 5002),
            (3005, '2025-01-21', 5003),
            (3006, '2025-01-23', 5003),
            (3007, '2025-02-02', 5001),
            (3008, '2025-02-02', 5001),
            # 3009, 3010, 3011 are NOT filled (drug shortage)
            (3012, '2025-01-26', 5002),  # Generic filled by 5002
            (3013, '2025-01-27', 5002),  # Generic filled by 5002
            (3014, '2025-01-28', 5002),  # Generic filled by 5002
        }
    
    def print_summary(self):
        """データベースの概要を表示"""
        print("=" * 70)
        print("PHARMACY DATABASE SUMMARY")
        print("=" * 70)
        
        relations = [
            ("Product", self.Product),
            ("Generic", self.Generic),
            ("Price", self.Price),
            ("ActiveIngredient", self.ActiveIngredient),
            ("Contains", self.Contains),
            ("Interaction", self.Interaction),
            ("Patient", self.Patient),
            ("Pharmacist", self.Pharmacist),
            ("Prescription", self.Prescription),
            ("Filled", self.Filled),
        ]
        
        for name, relation in relations:
            print(f"\n{name}: {len(relation)} tuples")
            for i, t in enumerate(sorted(relation)[:3], 1):
                print(f"  {i}. {t}")
            if len(relation) > 3:
                print(f"  ... and {len(relation) - 3} more")
        
        print("\n" + "=" * 70)
    
    def validate_primary_keys(self):
        """主キー制約の検証"""
        print("\n" + "=" * 70)
        print("PRIMARY KEY CONSTRAINT VALIDATION")
        print("=" * 70)
        
        all_valid = True
        relations = [
            ("Product", self.Product),
            ("Generic", self.Generic),
            ("Price", self.Price),
            ("ActiveIngredient", self.ActiveIngredient),
            ("Contains", self.Contains),
            ("Interaction", self.Interaction),
            ("Patient", self.Patient),
            ("Pharmacist", self.Pharmacist),
            ("Prescription", self.Prescription),
            ("Filled", self.Filled),
        ]
        
        for name, relation in relations:
            key_indices = self.PRIMARY_KEYS[name]
            seen_keys = set()
            duplicates = []
            
            for tuple_val in relation:
                key = tuple(tuple_val[i] for i in key_indices)
                if key in seen_keys:
                    duplicates.append(key)
                seen_keys.add(key)
            
            if duplicates:
                print(f"✗ {name}: DUPLICATE KEYS FOUND!")
                for dup in duplicates[:3]:
                    print(f"    Duplicate: {dup}")
                all_valid = False
            else:
                print(f"✓ {name}: No duplicates ({len(seen_keys)} unique keys)")
        
        return all_valid
    
    def validate_integrity_constraints(self):
        """課題で指定された整合性制約の検証"""
        print("\n" + "=" * 70)
        print("INTEGRITY CONSTRAINT VALIDATION")
        print("=" * 70)
        
        all_valid = True
        
        # 1. πDIN(Product) ∩ πDIN(Generic) = φ
        product_dins = {p[0] for p in self.Product}
        generic_dins = {g[0] for g in self.Generic}
        intersection = product_dins & generic_dins
        if intersection:
            print(f"✗ Constraint 1: Product DINs ∩ Generic DINs ≠ φ")
            print(f"    Violation: {intersection}")
            all_valid = False
        else:
            print(f"✓ Constraint 1: Product DINs ∩ Generic DINs = φ")
        
        # 2. Generic[brand] ⊆ Product[DIN]
        brand_dins = {g[1] for g in self.Generic}
        missing_brands = brand_dins - product_dins
        if missing_brands:
            print(f"✗ Constraint 2: Generic[brand] ⊈ Product[DIN]")
            print(f"    Missing brands: {missing_brands}")
            all_valid = False
        else:
            print(f"✓ Constraint 2: Generic[brand] ⊆ Product[DIN]")
        
        # 3. πDIN(Price) - (πDIN(Product) ∪ πDIN(Generic)) = φ
        price_dins = {p[0] for p in self.Price}
        all_drug_dins = product_dins | generic_dins
        invalid_prices = price_dins - all_drug_dins
        if invalid_prices:
            print(f"✗ Constraint 3: Price contains non-existent drugs")
            print(f"    Invalid DINs: {invalid_prices}")
            all_valid = False
        else:
            print(f"✓ Constraint 3: All priced drugs exist")
        
        # 4. Contains[DIN] ⊆ Product[DIN]
        contains_dins = {c[0] for c in self.Contains}
        missing_in_contains = contains_dins - product_dins
        if missing_in_contains:
            print(f"✗ Constraint 4: Contains[DIN] ⊈ Product[DIN]")
            print(f"    Missing DINs: {missing_in_contains}")
            all_valid = False
        else:
            print(f"✓ Constraint 4: Contains[DIN] ⊆ Product[DIN]")
        
        # 5. ρDIN(πdrug(Prescription)) - (πDIN(Product) ∪ πDIN(Generic)) = φ
        prescription_drugs = {p[3] for p in self.Prescription}
        invalid_prescriptions = prescription_drugs - all_drug_dins
        if invalid_prescriptions:
            print(f"✗ Constraint 5: Prescriptions for non-existent drugs")
            print(f"    Invalid drug DINs: {invalid_prescriptions}")
            all_valid = False
        else:
            print(f"✓ Constraint 5: All prescribed drugs exist")
        
        # 6. Contains[ingredient] ⊆ ActiveIngredient[name]
        contains_ingredients = {c[1] for c in self.Contains}
        active_ingredients = {a[0] for a in self.ActiveIngredient}
        missing_ingredients = contains_ingredients - active_ingredients
        if missing_ingredients:
            print(f"✗ Constraint 6: Contains[ingredient] ⊈ ActiveIngredient[name]")
            print(f"    Missing ingredients: {missing_ingredients}")
            all_valid = False
        else:
            print(f"✓ Constraint 6: Contains[ingredient] ⊆ ActiveIngredient[name]")
        
        # 7. Interaction[ingredient1] ⊆ ActiveIngredient[name]
        interaction_ing1 = {i[0] for i in self.Interaction}
        missing_ing1 = interaction_ing1 - active_ingredients
        if missing_ing1:
            print(f"✗ Constraint 7: Interaction[ingredient1] ⊈ ActiveIngredient[name]")
            print(f"    Missing ingredients: {missing_ing1}")
            all_valid = False
        else:
            print(f"✓ Constraint 7: Interaction[ingredient1] ⊆ ActiveIngredient[name]")
        
        # 8. Interaction[ingredient2] ⊆ ActiveIngredient[name]
        interaction_ing2 = {i[1] for i in self.Interaction}
        missing_ing2 = interaction_ing2 - active_ingredients
        if missing_ing2:
            print(f"✗ Constraint 8: Interaction[ingredient2] ⊈ ActiveIngredient[name]")
            print(f"    Missing ingredients: {missing_ing2}")
            all_valid = False
        else:
            print(f"✓ Constraint 8: Interaction[ingredient2] ⊆ ActiveIngredient[name]")
        
        # 9. Symmetry: If A interacts with B, then B interacts with A
        violations = []
        for inter in self.Interaction:
            reverse = (inter[1], inter[0])
            if reverse not in self.Interaction:
                violations.append((inter, reverse))
        if violations:
            print(f"✗ Constraint 9: Interaction symmetry violated")
            for orig, missing in violations[:3]:
                print(f"    {orig} exists but {missing} is missing")
            all_valid = False
        else:
            print(f"✓ Constraint 9: Interaction symmetry holds")
        
        # 10. Product[DIN] ⊆ Contains[DIN]
        not_in_contains = product_dins - contains_dins
        if not_in_contains:
            print(f"✗ Constraint 10: Product[DIN] ⊈ Contains[DIN]")
            print(f"    Products without ingredients: {not_in_contains}")
            all_valid = False
        else:
            print(f"✓ Constraint 10: Product[DIN] ⊆ Contains[DIN]")
        
        # 11. Prescription[patient] ⊆ Patient[OHIP]
        prescription_patients = {p[2] for p in self.Prescription}
        patient_ohips = {p[0] for p in self.Patient}
        missing_patients = prescription_patients - patient_ohips
        if missing_patients:
            print(f"✗ Constraint 11: Prescription[patient] ⊈ Patient[OHIP]")
            print(f"    Missing patients: {missing_patients}")
            all_valid = False
        else:
            print(f"✓ Constraint 11: Prescription[patient] ⊆ Patient[OHIP]")
        
        # 12. Filled[RxID] ⊆ Prescription[RxID]
        filled_rxids = {f[0] for f in self.Filled}
        prescription_rxids = {p[0] for p in self.Prescription}
        missing_prescriptions = filled_rxids - prescription_rxids
        if missing_prescriptions:
            print(f"✗ Constraint 12: Filled[RxID] ⊈ Prescription[RxID]")
            print(f"    Filled but not prescribed: {missing_prescriptions}")
            all_valid = False
        else:
            print(f"✓ Constraint 12: Filled[RxID] ⊆ Prescription[RxID]")
        
        # 13. Filled[pharmacist] ⊆ Pharmacist[OCP]
        filled_pharmacists = {f[2] for f in self.Filled}
        pharmacist_ocps = {p[0] for p in self.Pharmacist}
        missing_pharmacists = filled_pharmacists - pharmacist_ocps
        if missing_pharmacists:
            print(f"✗ Constraint 13: Filled[pharmacist] ⊈ Pharmacist[OCP]")
            print(f"    Missing pharmacists: {missing_pharmacists}")
            all_valid = False
        else:
            print(f"✓ Constraint 13: Filled[pharmacist] ⊆ Pharmacist[OCP]")
        
        # 14. πschedule(Product) ⊆ {"prescription", "narcotic", "OTC", "homeopathic"}
        valid_schedules = {"prescription", "narcotic", "OTC", "homeopathic"}
        product_schedules = {p[4] for p in self.Product}
        invalid_schedules = product_schedules - valid_schedules
        if invalid_schedules:
            print(f"✗ Constraint 14: Invalid schedules found")
            print(f"    Invalid: {invalid_schedules}")
            all_valid = False
        else:
            print(f"✓ Constraint 14: All schedules are valid")
        
        # 15. No prescription filled before it was written
        date_violations = []
        for filled in self.Filled:
            for prescription in self.Prescription:
                if (filled[0] == prescription[0] and  # Same RxID
                    filled[1] < prescription[1]):     # Filled before prescribed
                    date_violations.append((filled[0], prescription[1], filled[1]))
        if date_violations:
            print(f"✗ Constraint 15: Prescriptions filled before written")
            for rxid, presc_date, fill_date in date_violations[:3]:
                print(f"    RxID {rxid}: prescribed {presc_date}, filled {fill_date}")
            all_valid = False
        else:
            print(f"✓ Constraint 15: All prescriptions filled after written")
        
        print("\n" + "-" * 70)
        if all_valid:
            print("✓ ALL INTEGRITY CONSTRAINTS SATISFIED")
        else:
            print("✗ SOME INTEGRITY CONSTRAINTS VIOLATED")
        
        return all_valid
    
    def validate_all(self):
        """すべての制約を検証"""
        pk_valid = self.validate_primary_keys()
        ic_valid = self.validate_integrity_constraints()
        
        print("\n" + "=" * 70)
        if pk_valid and ic_valid:
            print("✓✓✓ DATABASE IS VALID ✓✓✓")
        else:
            print("✗✗✗ DATABASE HAS CONSTRAINT VIOLATIONS ✗✗✗")
        print("=" * 70)
        
        return pk_valid and ic_valid


if __name__ == "__main__":
    db = PharmacyDatabase()
    db.print_summary()
    db.validate_all()
