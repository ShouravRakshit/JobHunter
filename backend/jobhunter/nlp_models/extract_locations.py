import csv

STATES_PROVINCES = {
    # Canada
    "BC", "AB", "SK", "MB", "ON", "QC", "NB", "NS", "PE", "NL", "NT", "YT", "NU",
    # US
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL",
    "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT",
    "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI",
    "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
    # India
    "AP", "AR", "AS", "BR", "CG", "GA", "GJ", "HR", "HP", "JK", "JH", "KA", "KL",
    "MP", "MH", "MN", "ML", "MZ", "NL", "OR", "PB", "RJ", "SK", "TN", "TG", "TR",
    "UP", "UT", "WB",
    # Australia
    "NSW", "QLD", "SA", "TAS", "VIC", "WA",
    # UK
    "ENG", "NIR", "SCT", "WLS",
    # Germany
    "BW", "BY", "BE", "BB", "HB", "HH", "HE", "MV", "NI", "NW", "RP", "SL", "SN", "ST", "SH", "TH",
    # France
    "ARA", "BFC", "BRE", "CVL", "COR", "GES", "IDF", "NAQ", "NOR", "OCC", "PDL",
    # Italy
    "ABR", "BAS", "CAL", "CAM", "EMR", "FVG", "LAZ", "LIG", "LOM", "MAR", "MOL", "PIE", "PUG", "SAR", "SIC", "TOS", "TAA", "UMB", "VDA", "VEN",
    # Spain
    "AN", "AR", "AS", "CN", "CB", "CM", "CL", "CT", "EX", "GA", "IB", "RI", "MD", "MC", "NC", "PV", "VC"
    # Mexico
    "AGU", "BCN", "BCS", "CAM", "CHP", "CHH", "CMX", "COA", "COL", "DUR", "GUA", "GRO", "HID", "JAL", "MEX", "MIC", "MOR", "NAY", "NLE", "OAX",
    "PUE", "QUE", "ROO", "SLP", "SIN", "SON", "TAB", "TAM", "TLA", "VER", "YUC", "ZAC"
    # Brazil
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR",
    "SC", "SP", "SE", "TO"
    # Russia
    "AD", "AL", "ALT", "AMU", "ARK", "AST", "BA", "BEL", "BRY", "BU", "CE", "CHE", "CU", "DA", "IN", "IRK", "IVA", "KB", "KGD", "KL", "KLU",
    "KO", "KOS", "KR", "KRS", "KYA", "LEN", "LIP", "ME", "MO", "MOS", "MOW", "MUR", "NEN", "NGR", "NIZ", "NVS", "OMS", "ORE", "ORL", "PNZ",
    "PRI", "PSK", "ROS", "RYA", "SA", "SAK", "SAM", "SAR", "SE", "SMO", "SPE", "STA", "SVE", "TA", "TAM", "TOM", "TUL", "TVE", "TY", "TYU",
    "UD", "ULY", "VGG", "VL", "VLA", "VOR", "YAN", "YAR", "YEV", "ZAB",
}

def parse_location_line(line):
    tokens = [t.strip() for t in line.split(",")]
    results = []
    i = 0
    while i < len(tokens):
        cityPart = tokens[i]
        j = i + 1
        region = None

        # Look ahead for region code
        while j < len(tokens):
            candidate = tokens[j].strip()
            if candidate.upper() in STATES_PROVINCES:
                region = candidate.upper()
                break
            else:
                cityPart += ", " + candidate
            j += 1

        results.append((cityPart.strip(), region))

        if region is not None:
            i = j + 1
        else:
            i = j

    return results

def parse_locations_in_csv(input_csv, output_csv):
    with open(input_csv, newline="", encoding="utf-8") as fin, \
         open(output_csv, "w", newline="", encoding="utf-8") as fout:
        reader = csv.DictReader(fin)
        fieldnames = reader.fieldnames + ["parsed_locations"]
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            loc_line = row.get("location", "")
            parsed = parse_location_line(loc_line)

            pairs_str = []
            for city, region in parsed:
                if region:
                    pairs_str.append(f"{city} - {region}")
                else:
                    pairs_str.append(city)
            row["parsed_locations"] = " | ".join(pairs_str)

            writer.writerow(row)

def main():
    input_csv = "JobHunter/data/jobs_with_tfidf_keywords.csv"
    output_csv = "JobHunter/data/jobs_with_locations.csv"
    parse_locations_in_csv(input_csv, output_csv)
    print(f"Done. Parsed locations saved in {output_csv}.")

if __name__ == "__main__":
    main()
