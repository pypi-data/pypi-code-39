import klazor_client as kc

kc.config(
    API_URL='http://127.0.0.1:8000/api',
    LOGIN='wilcoln',
    PASSWORD='password'
)
course = kc.fetch_course(1)
sheet = kc.fetch_sheet(2)
courses = kc.fetch_courses()
sheets = kc.fetch_sheets()
print(sheets)
