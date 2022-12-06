import os
import subprocess
import xlwt
import csv

# Function to check if host is up
def is_host_up(ip_address):
    response = subprocess.run(["nmap", "-sP", ip_address], stdout=subprocess.PIPE)
    for line in response.stdout.decode("utf-8").split("\n"):
        if "Host is up" in line:
            return True
    return False

# Function to scan ports
def scan_ports(ip_address):
    response = subprocess.run(["nmap", "-Pn", ip_address], stdout=subprocess.PIPE)
    open_ports = []
    for line in response.stdout.decode("utf-8").split("\n"):
        if "/tcp" in line:
            open_ports.append(line.split("/")[0])
    return open_ports

# Read input file
ip_addresses = []
with open("input.txt", "r") as input_file:
    for line in input_file.readlines():
        ip_addresses.append(line.strip())

# Create Excel file
workbook = xlwt.Workbook()
worksheet = workbook.add_sheet("Ports")

# Write header row
worksheet.write(0, 0, "IP Address")
worksheet.write(0, 1, "Open Ports")

# Write data rows
row_num = 1
for ip_address in ip_addresses:
    if is_host_up(ip_address):
        open_ports = scan_ports(ip_address)
        worksheet.write(row_num, 0, ip_address)
        worksheet.write(row_num, 1, ", ".join(open_ports))
        row_num += 1

# Save Excel file
workbook.save("output.xls")
# Create CSV file
with open("output.csv", "w") as output_file:
    writer = csv.writer(output_file)

    # Write header row
    writer.writerow(["IP Address", "Open Ports"])

    # Write data rows
    for ip_address in ip_addresses:
        if is_host_up(ip_address):
            open_ports = scan_ports(ip_address)
            writer.writerow([ip_address, ", ".join(open_ports)])
