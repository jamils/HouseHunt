# Get information from ValleyMLS

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

mls_url = input('ValleyMLS URL: ')

opts = Options()
opts.headless = False
driver = Firefox(options=opts)

driver.get(mls_url)

title = driver.title
title_pieces = title.split("|")

address = title_pieces[0].strip()

print("Getting information for: ", address)

addr_pieces = address.split(",")

street = addr_pieces[0].strip()
street = street.strip(".")
city = addr_pieces[1].strip()
state = addr_pieces[2].strip()
# zip = addr_pieces[3].strip()

title_summary = driver.find_element(By.ID, "listingdetail-title-summary")

price = float(title_summary.get_attribute("data-price"))
zip = title_summary.get_attribute("data-zipcode")

right_side = title_summary.find_element(By.CLASS_NAME, "right-side-information-container").text

right_side_lines = right_side.splitlines()
sq_text_index = right_side_lines.index("Sq. Ft.")
sq_index = sq_text_index - 1
sqft = float(right_side_lines[sq_index].replace(',', ''))

lot_size = driver.find_element(By.ID, "mls-lot2").text
mls_num = driver.find_element(By.ID, "mls-num2").text
bed_num = driver.find_element(By.ID, "mls-bed2").text
bath_num = driver.find_element(By.ID, "mls-bath2").text

sqft_price = round((price/sqft), 3)

lot_size = float(''.join(c for c in lot_size if (c.isdigit() or c =='.')))


# Write markdown file

filename = "docs/" + street.lower().replace(" ", "-") + ".md"

### Construct zillow URL

zillow_url = "https://www.zillow.com/homes/" + street.replace(" ", "-") + "-" + city.replace(" ", "-") + "," + "-" + state.replace(" ", "-")

with open(filename, "w", encoding="utf-8") as f:
    f.write("---\n")
    f.write("comments: true\n")
    f.write("---\n")
    f.write("\n")
    f.write("# 📫 " + street + "\n")
    f.write("\n")
    f.write("<img\n")
    f.write('    src=\"\" \n')
    f.write('   alt=\"image\" \n' )
    f.write('   width=\"400\" \n' )
    f.write('   style=\"border:2px solid black\"> \n')
    f.write('\n')
    f.write('### :map: Map')
    f.write('\n')
    f.write('\n')
    f.write('### :open_file_folder: Quick Facts')
    f.write('\n')
    f.write("| Description       | Value |\n")
    f.write("| ----------------: | :---- |\n")
    f.write(f"| Price             | ${price:,} |\n")
    f.write(f"| Square Feet       | {sqft:,} |\n")
    f.write(f"| $/sqft            | ${sqft_price:,} |\n")
    f.write(f"| # of Bedrooms     | {bed_num} |\n")
    f.write(f"| # of Bathrooms    | {bed_num} |\n")
    f.write(f"| Lot size (acres)  | {lot_size} |\n")
    f.write("\n")
    f.write("### :globe_with_meridians: Web links\n")
    f.write("\n")
    f.write("??? info :fontawesome-solid-mountain-sun:  Valley MLS\n")
    f.write(f"    [ValleyMLS 	:link:]({mls_url})\n")
    f.write("\n")
    f.write(f'    <iframe width=700, height=500 frameBorder=0 src="{mls_url}"></iframe>\n')
    f.write("\n")
    f.write("??? info :simple-zillow:  Zillow\n")
    f.write(f"    [Zillow :link:]({zillow_url})\n")
    f.write("\n")
    f.write(f'    <iframe width=700, height=500 frameBorder=0 src="{zillow_url}"></iframe>\n')
    f.write("\n")
    
# Adding to index file

with open("docs/index.md", "a", encoding="utf-8") as f:
    f.write(f"* :new: [{address}]({filename})\n")