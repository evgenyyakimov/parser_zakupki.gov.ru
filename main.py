from zakupki import extract_max_page, extract_org
from save import save_to_csv

max_page = extract_max_page()
orgs = extract_org(max_page)
save_to_csv(orgs)