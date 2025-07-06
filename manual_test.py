from fpdf import FPDF

# Data for the test cases table
headers = ["TestCaseID", "Description", "Input", "Expected Output", "Actual Output", "Status"]
data = [
    ["TC01", "User Login - Valid Credentials", "Enter valid username & password", "Dashboard should load", "As expected", "Pass"],
    ["TC02", "User Login - Invalid Credentials", "Enter wrong username or password", "Should show error message", "As expected", "Pass"],
    ["TC03", "User Signup - New User", "Enter new username & matching passwords", "Account created and redirected", "As expected", "Pass"],
    ["TC04", "User Signup - Password Mismatch", "Enter different passwords", "Show password mismatch error", "As expected", "Pass"],
    ["TC05", "User Login - Remember Me", "Enter valid credentials and select 'Remember Me'", "User remains logged in after restart", "As expected", "Pass"],
    ["TC06", "User Logout", "Click on Logout", "Redirect to login page", "As expected", "Pass"],
    ["TC07", "Upload JD & Valid Resumes", "Upload job description and valid resumes", "Ranked resumes shown with missing skills", "As expected", "Pass"],
    ["TC08", "Upload Resume - Missing File", "Upload job description only", "Error: 'Please upload at least one resume'", "As expected", "Pass"],
    ["TC09", "Upload JD - Missing File", "Upload resumes only", "Error: 'Please upload a job description'", "As expected", "Pass"],
    ["TC10", "Upload Without Login", "Try uploading without logging in", "Redirect to login page", "As expected", "Pass"],
    ["TC11", "Invalid Resume Format", "Upload .txt/.docx file", "Error: 'Invalid file format'", "As expected", "Pass"],
    ["TC12", "Extract Skills from Resume", "Upload valid resume", "Correct skills extracted", "As expected", "Pass"],
    ["TC13", "Missing Skills Calculation", "Upload resume & JD with different skills", "Display missing skills", "As expected", "Pass"],
    ["TC14", "Cosine Similarity Calculation", "Upload resume & JD", "Cosine score displayed", "As expected", "Pass"],
    ["TC15", "Job Recommendations", "Upload resume & JD with relevant skills", "Show recommended job roles", "As expected", "Pass"],
    ["TC16", "Download Not Selected", "Click 'Download Not Selected'", "Download Excel file", "As expected", "Pass"],
    ["TC17", "Download Selected", "Click 'Download Selected'", "Download Excel file", "As expected", "Pass"],
    ["TC18", "Missing skills.txt File", "Delete skills.txt & upload resume", "Error: 'skills.txt file is missing'", "As expected", "Pass"],
    ["TC19", "Large Resume Upload", "Upload large PDF", "Resume processed without errors", "As expected", "Pass"],
    ["TC20", "Multiple Resumes Upload", "Upload multiple resumes with JD", "All resumes handled & ranked", "As expected", "Pass"]
]

# Column widths
col_widths = [15, 45, 45, 55, 25, 20]
line_height = 6

# PDF setup
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=10)
pdf.add_page()
pdf.set_font("Arial", "B", 11)
pdf.cell(0, 10, "Manual Test Cases - Resume Analysis App", ln=True, align='C')
pdf.ln(5)

# Table Header
pdf.set_font("Arial", "B", 9)
for i, header in enumerate(headers):
    pdf.cell(col_widths[i], line_height * 2, header, border=1, align='C')
pdf.ln()

# Table Rows
pdf.set_font("Arial", "", 8)
for row in data:
    x_start = pdf.get_x()
    y_start = pdf.get_y()
    
    # Calculate max height needed
    cell_heights = []
    for i, item in enumerate(row):
        num_lines = pdf.multi_cell(col_widths[i], line_height, item, border=0, align='L', split_only=True)
        cell_heights.append(len(num_lines) * line_height)
    row_height = max(cell_heights)

    # Draw cells with fixed height
    for i, item in enumerate(row):
        x = pdf.get_x()
        y = pdf.get_y()
        pdf.multi_cell(col_widths[i], line_height, item, border=1, align='L')
        pdf.set_xy(x + col_widths[i], y)

    pdf.set_y(y_start + row_height)

# Output PDF
pdf.output("manual_test_cases.pdf")
print("✅ Test case PDF successfully created: manual_test_cases.pdf")
