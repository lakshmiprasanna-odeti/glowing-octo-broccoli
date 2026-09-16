import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
import pyarrow.ipc as ipc


# TASK 1: Create an Arrow Table

data = {
    "employee_id": [1, 2, 3, 4, 5, 6],
    "name": ["Asha", "Rahul", "Neha", "Vikram", "Priya", "Arjun"],
    "department": ["IT", "HR", "IT", "Finance", "HR", "Finance"],
    "salary": [60000, 45000, 70000, 55000, 48000, 65000],
    "city": ["Delhi", "Mumbai", "Bengaluru", "Delhi", "Mumbai", "Chennai"]
}

employee_table = pa.table(data)

print("TASK 1: Arrow Table")
print(employee_table)


# TASK 2: Display Schema

print("\nTASK 2: Schema")
print(employee_table.schema)


# TASK 3: Inspect the Table

print("\nTASK 3: Inspect Table")

print("Rows:", employee_table.num_rows)
print("Columns:", employee_table.num_columns)
print("Column names:", employee_table.column_names)

print("Name column:")
print(employee_table.column("name"))

print("First three rows:")
print(employee_table.slice(0, 3))


# TASK 4: Select Specific Columns

print("\nTASK 4: Selected Columns")

selected_table = employee_table.select(
    ["name", "department", "salary"]
)

print(selected_table)


# TASK 5: Filter Salary Greater Than 50000

print("\nTASK 5: Salary Greater Than 50000")

salary_filter = pc.greater(
    employee_table["salary"],
    50000
)

high_salary_table = employee_table.filter(
    salary_filter
)

print(high_salary_table)


# TASK 6: Filter IT Department

print("\nTASK 6: IT Employees")

department_filter = pc.equal(
    employee_table["department"],
    "IT"
)

it_employees = employee_table.filter(
    department_filter
)

print(it_employees)


# TASK 7: Perform Calculations

print("\nTASK 7: Salary Calculations")

salary_column = employee_table["salary"]

print("Average salary:", pc.mean(salary_column).as_py())
print("Maximum salary:", pc.max(salary_column).as_py())
print("Minimum salary:", pc.min(salary_column).as_py())
print("Total salary:", pc.sum(salary_column).as_py())


# TASK 8: Add Bonus Column

print("\nTASK 8: Bonus Column")

bonus_column = pc.multiply(
    employee_table["salary"],
    0.10
)

employee_table = employee_table.append_column(
    "bonus",
    bonus_column
)

print(employee_table)


# TASK 9: Convert Arrow to Pandas

print("\nTASK 9: Arrow to Pandas")

employee_df = employee_table.to_pandas()

print(employee_df)


# TASK 10: Convert Pandas to Arrow

print("\nTASK 10: Pandas to Arrow")

new_arrow_table = pa.Table.from_pandas(
    employee_df,
    preserve_index=False
)

print(new_arrow_table)


# TASK 11: Save as Parquet File

print("\nTASK 11: Save Parquet")

pq.write_table(
    employee_table,
    "employees.parquet"
)

print("Parquet file created successfully.")


# TASK 12: Read Parquet File

print("\nTASK 12: Read Parquet")

loaded_table = pq.read_table(
    "employees.parquet"
)

print(loaded_table)


# TASK 13: Save as Arrow IPC File

print("\nTASK 13: Save Arrow IPC")

with ipc.new_file(
    "employees.arrow",
    employee_table.schema
) as writer:

    writer.write_table(employee_table)

print("Arrow IPC file created successfully.")


# TASK 14: Read Arrow IPC File

print("\nTASK 14: Read Arrow IPC")

with ipc.open_file("employees.arrow") as reader:

    ipc_table = reader.read_all()

print(ipc_table)


# BONUS 1: Employees in Delhi

print("\nBONUS 1: Delhi Employees")

delhi_filter = pc.equal(
    employee_table["city"],
    "Delhi"
)

delhi_employees = employee_table.filter(
    delhi_filter
)

print(delhi_employees)


# BONUS 2: Salary Between 50000 and 65000

print("\nBONUS 2: Salary Between 50000 and 65000")

salary_range_filter = pc.and_(
    pc.greater_equal(employee_table["salary"], 50000),
    pc.less_equal(employee_table["salary"], 65000)
)

salary_range_table = employee_table.filter(
    salary_range_filter
)

print(salary_range_table)


# BONUS 3: Add Annual Salary

print("\nBONUS 3: Annual Salary")

annual_salary_column = pc.multiply(
    employee_table["salary"],
    12
)

employee_table = employee_table.append_column(
    "annual_salary",
    annual_salary_column
)

print(employee_table)


# BONUS 4: Save IT Employees

print("\nBONUS 4: Save IT Employees")

it_employees = employee_table.filter(
    department_filter
)

pq.write_table(
    it_employees,
    "it_employees.parquet"
)

print("IT employees file created successfully.")


# BONUS 5: Read Name and Salary Columns

print("\nBONUS 5: Selected Columns from Parquet")

selected_columns = pq.read_table(
    "employees.parquet",
    columns=["name", "salary"]
)

print(selected_columns)


# BONUS 6: Sort Employees by Salary

print("\nBONUS 6: Sort by Salary")

sorted_df = employee_df.sort_values(
    by="salary",
    ascending=False
)

print(sorted_df)

print("\nALL TASKS COMPLETED SUCCESSFULLY!")
