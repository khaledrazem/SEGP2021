from mendeley import Mendeley
from datetime import datetime

# mendeley authentication
def mendeleyAuth():
    client_id = "8949"
    client_secret = "u38KsziNTLHOD8VB"
    mendeley = Mendeley(client_id, client_secret)
    auth = mendeley.start_client_credentials_flow()
    session = auth.authenticate()
    
    return session

# get current year
def current_year():
    current_year = datetime.now().year
    return current_year

# get starting year(starting from last year)
def getStartYear(setYear):
    start_year = current_year() - setYear -1
    return start_year
    
# get ending year(returns last year)
def getEndYear():
    end_year = current_year() - 1
    return end_year
