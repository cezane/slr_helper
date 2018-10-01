import sys, csv, os, json

def main():
    #TODO add a usage guide: filter results (input --> output)
    #                 remove duplicated entries (input --> output)
    # --> when excluding reviews/surveys --> get titles for "related works"
    args = sys.argv[1:]
    if not len(args) > 2:
        sys.exit("Usage: python3 slr_helper.py input_file.csv output_file.csv related_works_file.csv")

    in_filename = str(args[0]) # if len(args) != 0 else ""
    newfilename = str(args[1]) # if len(args) > 1 else ""
    rw_filename = str(args[2])
    files = [newfilename, rw_filename]
    file_exists = [os.path.isfile(newfilename), os.path.isfile(rw_filename)]

    header = ["Title", "Authors", "Year", "Abstract", "Keywords"]

    print("This is a Tabajara SLR helper script which aims to " \
          "remove duplicated entries and, maybe, do some more good stuff.")
    print("Enter the exact field names in the exact following order: \n")
    print('"Title", "Authors", "Year", "Abstract", "Keywords"')

    field_names = list()
    field_values = list()
    relatedworks_values = list()
    for i in range(0, len(header)):
        field_name = input("Enter the exact name of {} field in the file: ".format(header[i]))
        field_names.append(field_name)

    try:
        with open(in_filename, 'r', encoding='utf-8-sig') as infile:
            rowsreader = csv.DictReader(infile, delimiter=",")
            outrowsreader = list()
            if file_exists:
                with open(newfilename, 'r') as outfile:
                    outrowsreader = list(csv.DictReader(outfile))
            count = 0;
            for row in rowsreader:
                dict_row = {}
                for i in range(0, len(field_names)):
                    field = field_names[i]
                    dict_row[header[i]] = row[field] if field in row else ""

                if not any(r["Title"] == dict_row["Title"] for r in outrowsreader) \
                   or not file_exists:
                    if any (s in dict_row["Title"].lower() for s in ["survey", "review"]):
                        relatedworks_values.append(dict_row)
                    else:
                        field_values.append(dict_row)
                        count += 1
            print(count)
    except IOError:
        print("Could not open csv file: {}.".format(in_filename))

    fields = [field_values, relatedworks_values]

    for i in range(0, len(files)):
        try:
            with open(files[i], 'a') as outfile:
                rowswriter = csv.DictWriter(outfile, header)
                if not file_exists[i]:
                    rowswriter.writeheader()
                for row in fields[i]:
                    rowswriter.writerow(row)
        except IOError:
            print("Could not convert to csv file: {}.".format(files[i]))

if __name__ == "__main__":
    main()
