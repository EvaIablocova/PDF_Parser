import requests

url = 'https://www.asp.gov.md/sites/default/files/date-deschise/avizele-agentilor-economici/total/Denumirea_2008_2024.pdf'
# url = 'https://www.asp.gov.md/sites/default/files/date-deschise/avizele-agentilor-economici/Denumirea.pdf'
response = requests.get(url)

goal_file = 'Denumirea_2008_2024.pdf'

with open(goal_file, 'wb') as f:
    f.write(response.content)