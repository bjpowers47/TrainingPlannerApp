from app.workbook import WorkbookManager

wb = WorkbookManager()

wb.open("Soccer 101 Training Schedule.xlsx")

print()

print("Headers")

print("--------------------")

print(wb.get_headers())

print()

print("Rows")

print("--------------------")

for session in wb.get_sessions():

    print(session.values)