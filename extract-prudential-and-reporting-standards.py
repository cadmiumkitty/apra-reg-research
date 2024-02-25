from bs4 import BeautifulSoup
import csv
import re
import requests

standards = [
        ('Authorised Depsit-Taking Institutions',   'https://www.apra.gov.au/industries/1/standards'),
        ('General Insurance',                       'https://www.apra.gov.au/industries/2/standards'),
        ('Life Insurance and Friendly Societies',   'https://www.apra.gov.au/industries/30/standards'),
        ('Private Health Insurance',                'https://www.apra.gov.au/industries/32/standards'),
        ('Superannuation',                          'https://www.apra.gov.au/industries/33/standards')]

standards_list = []

# Retrieve each standard in the list
for standard in standards:

    print(f'Requesting: {standard}')

    response = requests.get(standard[1])

    standard_soup = BeautifulSoup(response.text, features='html.parser')

    # Pick Sections first (Governance, Risk Management, etc.)
    standard_soup_sections = standard_soup.find_all('div', class_ = 'item-list')

    for standard_soup_section in standard_soup_sections:

        section_title = standard_soup_section.find('div', class_ = 'section-title__title')
        section_title_text = section_title.text

        # Pick each Series in the seaction (310 Audit and Related Matters, etc.)
        section_standards = standard_soup_section.find_all('details')

        for section_standard in section_standards:

            # Series number and title are common for all sections
            summary = section_standard.find('summary')
            summary_standard_set_number = summary.find('div', class_ = 'field field-field-set-number field-type-integer field-label-hidden')
            summary_standard_set_number_text = summary_standard_set_number.text.strip()
            summary_standard_set_title = summary.find('h3', class_ = 'standard__title')
            summary_standard_set_title_text = summary_standard_set_title.text

            # Pick Documents for each of the series (SPS 310 Audit and Related Matters, etc.)
            documents = section_standard.find_all('div', 'standard__document__content')

            for document in documents:

                # Set default values - some things are common between the documents, but APRA is using different styles between
                # Standards and Guidance, Related material and simple files
                status = ''
                status_date = ''
                type = ''
                href = ''
                title = ''
                description = ''

                # Standards and Guidance - Status
                document_standard_tag_key = document.find('div', class_ = 'standard__tag__key')
                if document_standard_tag_key:
                    # Need to remove embedded tag and looking for all of the childder with text seems to be the only way
                    # Need to use strip() to get rid of the empty lines that result
                    status = ''.join(document_standard_tag_key.find_all(string=True, recursive=False)).strip()

                # Format of the dates is not consistent, so need pick a date pattern
                document_standard_tag_value = document.find('div', class_ = 'standard__tag__value')
                if document_standard_tag_value:
                    document_standard_tag_value_text = document_standard_tag_value.text.strip()
                    document_standard_tag_value_text_date_extract = re.search('(([0-9]{1,2}.?)?[A-Za-z]*\s[0-9]{4})', document_standard_tag_value_text)
                    if document_standard_tag_value_text_date_extract:
                        status_date = document_standard_tag_value_text_date_extract.group(1)

                # Standards and Guidance - Title, Description and Link
                document_link = document.find('div', class_ = 'standard__document__link')
                if document_link:
                    href = document_link.find('a')['href']
                    document_link_title = document_link.find('div', class_ = 'standard__document__title')
                    
                    # Simplest way to retrieve the type is actually look at the first 3 letters of the standard or guidance
                    # Need to include numbers because some (like 3PS for Level 3 ADIs) include numbers
                    title = document_link_title.text.strip()
                    title_type_extrcat = re.search('^([0-9A-Z]{3})', title)
                    if title_type_extrcat:
                        type = title_type_extrcat.group(1)
                    document_description = document.find('div', class_ = 'standard__document__description')
                    if document_description:
                        document_description.find('div')
                        description = document_description.text.strip()
                else:

                    # Related documents
                    document_link = document.find('a', class_ = 'standard__document__link')
                    if document_link:
                        href = document_link['href']
                        document_link_title = document.find('div', class_ = 'standard__document__title')
                        title = document_link_title.text.strip()
                        document_description = document.find('div', class_ = 'standard__document__description')
                        if document_description:
                            document_description.find('div')
                            description = document_description.text.strip()
                    else:

                        # Files
                        document_link = document.find('a', class_ = 'document-link')
                        if document_link:
                            href = document_link['href']
                            document_link_title = document.find('span', class_ = 'document-link__label')
                            title = document_link_title.text.strip()

                standard = (
                    standard[0],                        # Industry
                    section_title_text,                 # Section
                    summary_standard_set_number_text,   # Series
                    summary_standard_set_title_text,    # Standard
                    status,                             # Status (standards and guidance)
                    status_date,                        # Status date (standards and guidance)
                    type,
                    title,                              # Title (all documents)
                    description,                        # Description (all documents, but mostly standards and guidance)
                    href)                               # Link (all documents)
                
                standards_list.append(standard)
                print(f'Appended: {standard}')

# Write to CSV assuming a simple format. Need to use newline='' to avoid extra empty lines in the CSV 
with open('standards.csv', 'w', newline='', encoding='utf-8') as standards_file:
    writer = csv.writer(standards_file)
    writer.writerow(('Industry', 'Section', 'Series', 'Standard', 'Status', 'Status Date', 'Type', 'Title', 'Description', 'Link'))
    for standard in standards_list:
            writer.writerow(standard)

