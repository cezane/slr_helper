import sys, csv, os, json


def main():
    #TODO add a menu: filter results (input --> output)
    #                 remove duplicated entries (input --> output)
    args = sys.argv[1:]
    filename = str(args[0]) if len(args) != 0 else ""
    newfilename = str(args[1]) if len(args) > 1 else ""
    file_exists = os.path.isfile(newfilename)

    header = ["Title", "Authors", "Year", "Abstract", "Keywords"]

    print("This is a Tabajara SLR helper script which aims to " \
          "remove duplicated entries and, maybe, do some more good stuff.")
    print("Enter the exact field names in the exact following order: \n")
    print('"Title", "Authors", "Year", "Abstract", "Keywords"')

    field_names = list()
    field_values = list()
    for i in range(0, len(header)):
        field_name = input("Enter the exact name of {} field in the file: ".format(header[i]))
        field_names.append(field_name)

    try:    
        with open(filename, 'r', encoding='utf-8-sig') as infile:
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
                    field_values.append(dict_row)
                    count += 1
            print(count)
    except IOError:
        print("Could not open csv file: {}.".format(filename))

    try:
        with open(newfilename, 'a') as outfile:
            rowswriter = csv.DictWriter(outfile, header)
            if not file_exists:
                rowswriter.writeheader()
            for row in field_values:
                rowswriter.writerow(row)
    except IOError:
        print("Could not convert to csv file: {}.".format(newfilename))

if __name__ == "__main__":
    main()
