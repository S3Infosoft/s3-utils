import os
import csv
from sys import argv
from datetime import datetime
from pathlib import Path
from fpdf import FPDF

# Company Name HEADER in Payslip
COMPANY_NAME = 'ABC'
# The values in these lists should match column names in the CSV file
INCOME_LIST = ['Gross Salary Proposed', 'Performance Bonus', 'Overtime']
DEDUCTIONS_LIST = ['Adjusted During the Month', 'Professional Tax']

class PDF(FPDF):
    pass


def read_file():
    csv_file = argv[1]
    file_path = Path(argv[1])
    if not file_path.is_file():
        print('File not found, exiting program')
        exit()


    # stores the first row of the CSV file assuming they will be column names
    column_names = []

    # store payslip information as a dict
    payslip_info = {}

    # stores employee names as key and pay slip_info as value pairs
    employee_record = {}

    with open(csv_file, 'r') as userFile:
        csvFileReader = csv.reader(userFile)
        # reading the CSV row by row
        for i, employee in enumerate(csvFileReader):
            # checks if the first row is being read, assuming first row consists of column names
            if i == 0:
                column_names = employee
            else:
                for j, column in enumerate(column_names):
                    # ignore the first column assuming it's always the name
                    if j == 0:
                        continue
                    else:
                        # store play slip information inside the dict
                        payslip_info[column] = employee[j]
                # create a dictionary for the given employee name
                employee_record = {employee[0]: payslip_info}

            if i != 0:
                generate_pdf(employee[0], employee_record)

    print('PDFs created successfully.')


def generate_pdf(emp_name, employee_record):

    # Use to to increase/decrease column widths
    increased_w = 10

    # The values in these lists should match column names in the CSV file
    #INCOME_LIST = ['Gross Salary Proposed', 'Performance Bonus', 'Overtime']
    #DEDUCTIONS_LIST = ['Adjusted During the Month', 'Professional Tax']
    total_income = 0
    total_deduction = 0
    for value in INCOME_LIST:
        total_income = total_income + float(employee_record[emp_name][value])
    for value in DEDUCTIONS_LIST:
        total_deduction = total_deduction + float(employee_record[emp_name][value])

    pdf = PDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", size=18, style='B')
    col_width = pdf.w - 20
    row_height = pdf.font_size + 5

    # Configuration for first row
    pdf.set_fill_color(122, 255, 228)   # light blue
    pdf.cell(col_width, row_height, txt=COMPANY_NAME, border=1, fill=True, align='C')
    pdf.ln(row_height)

    # configuration for second row
    pdf.set_font("Arial", size=12, style='B')
    pdf.cell(col_width / 2, row_height, txt='Salary Slip', border=1, fill=True, align='C')
    pdf.cell(col_width / 4 + increased_w, row_height, txt='Date', border=1, fill=True, align='C')
    pdf.cell(col_width / 4 - increased_w, row_height, txt=employee_record[emp_name]['Date'], border=1, fill=True, align='C')
    pdf.ln(row_height)

    # inserts employee name outside loop
    # since it's not a part of the nested dictionary
    pdf.set_font("Arial", size=12)
    pdf.cell(col_width / 4 + increased_w, row_height, txt='Name', border=1)
    pdf.cell(col_width / 4 - increased_w, row_height, txt=emp_name, border=1, align='R')

    # Loop through all keys of the dictionary for a given employee
    # Insert a new line in the table every time cell_ctr reaches 4
    cell_ctr = 2    # counts number of cells inserted in a row
    for info in employee_record[emp_name].items():
        # Skipping specific columns
        if info[0] == 'Date' or info[0] in INCOME_LIST or info[0] in DEDUCTIONS_LIST:
            continue

        if cell_ctr == 4:
            pdf.ln(row_height)
            cell_ctr = 0
        field_name = info[0]
        pdf.cell(col_width/4 + increased_w, row_height, txt=field_name[0:20], border=1)
        pdf.cell(col_width/4 - increased_w, row_height, txt=info[1], border=1, align='R')
        cell_ctr = cell_ctr + 2

    pdf.ln(row_height)
    # Income/deduction generation
    pdf.set_font("Arial", size=12, style='B')
    pdf.cell(col_width / 2, row_height, txt='Income', border=1, fill=True, align='C')
    pdf.cell(col_width / 2, row_height, txt='Deductions', border=1, fill=True, align='C')
    pdf.ln(row_height)
    # Particulars & amount
    pdf.cell(col_width / 4 + 10, row_height, txt='Particulars', border=1, fill=True, align='C')
    pdf.cell(col_width / 4 - 10, row_height, txt='Amount', border=1, fill=True, align='C')
    pdf.cell(col_width / 4 + 10, row_height, txt='Particulars', border=1, fill=True, align='C')
    pdf.cell(col_width / 4 - 10, row_height, txt='Amount', border=1, fill=True, align='C')
    pdf.ln(row_height)
    # Filling cells alternately with income and deduction, starting with income
    # alt is 1 if cell is to be filled with income, 0 otherwise
    alt = 1
    i = 0   # index for income
    j = 0   # index for deduction
    cell_ctr = 0
    pdf.set_font("Arial", size=12)

    while True:
        if i > len(INCOME_LIST)-1 and j > len(DEDUCTIONS_LIST)-1:
            break

        if i > len(INCOME_LIST)-1 and j <= len(DEDUCTIONS_LIST)-1:
            alt = 0
        elif j > len(DEDUCTIONS_LIST)-1 and i <= len(INCOME_LIST)-1:
            alt = 1

        if cell_ctr == 4:
            pdf.ln(row_height)
            cell_ctr = 0

        if alt == 1 and i <= len(INCOME_LIST)-1:
            if cell_ctr == 2:
                # Inserts blank cells for deduction
                pdf.cell(col_width / 4 + increased_w, row_height, txt='', border=1)
                pdf.cell(col_width / 4 - increased_w, row_height, txt='', border=1)
                pdf.ln(row_height)
                cell_ctr = 0
            else:
                pdf.cell(col_width / 4 + increased_w, row_height, txt=INCOME_LIST[i], border=1)
                pdf.cell(col_width / 4 - increased_w, row_height, txt=employee_record[emp_name][INCOME_LIST[i]], border=1, align='R')
                cell_ctr = cell_ctr + 2
                alt = 0
                i = i + 1
        elif alt == 0 and j <= len(DEDUCTIONS_LIST)-1:
            if cell_ctr == 0:
                # Inserts blank cells for income
                pdf.cell(col_width / 4 + increased_w, row_height, txt='', border=1)
                pdf.cell(col_width / 4 - increased_w, row_height, txt='', border=1)
                cell_ctr = cell_ctr + 2
            else:
                pdf.cell(col_width / 4 + increased_w, row_height, txt=DEDUCTIONS_LIST[j], border=1)
                pdf.cell(col_width / 4 - increased_w, row_height, txt=employee_record[emp_name][DEDUCTIONS_LIST[j]], border=1, align='R')
                cell_ctr = cell_ctr + 2
                alt = 1
                j = j + 1

    # displaying totals
    pdf.set_font("Arial", size=12, style='B')
    if cell_ctr == 2:
        pdf.cell(col_width / 4 + increased_w, row_height, txt='', border=1)
        pdf.cell(col_width / 4 - increased_w, row_height, txt='', border=1)
        pdf.ln(row_height)
    elif cell_ctr == 4:
        pdf.ln(row_height)
    pdf.cell(col_width / 4 + increased_w, row_height, txt='Total', border=1, fill=True)
    pdf.cell(col_width / 4 - increased_w, row_height, txt=str(total_income), border=1, fill=True, align='R')
    pdf.cell(col_width / 4 + increased_w, row_height, txt='Total', border=1, fill=True)
    pdf.cell(col_width / 4 - increased_w, row_height, txt=str(total_deduction), border=1, fill=True, align='R')
    pdf.ln(row_height)
    pdf.cell(col_width / 2, row_height, txt='Net salary', border=1, fill=True, align='C')
    pdf.cell(col_width / 2, row_height, txt=str(total_income-total_deduction), border=1, fill=True, align='C')
    pdf.ln(row_height)
    # signature area
    pdf.cell(col_width / 2, row_height, txt='Employee Signature', border=1, align='C')
    pdf.cell(col_width / 2, row_height, txt='Employer Signature', border=1, align='C')
    pdf.ln(row_height)
    pdf.cell(col_width / 2, row_height + 25, txt='', border=1)
    pdf.cell(col_width / 2, row_height + 25, txt='', border=1)
    output_filename = 'output' + os.sep + emp_name + '-' + str(datetime.now().month) + '-' + str(datetime.now().year) + '.pdf'
    pdf.output(output_filename, 'F')


def main():
    read_file()


if __name__ == "__main__":
    main()
