import re
from bs4 import NavigableString

class Scraper:
    def __init__(self, page):
        self.page = page

    def strip_html(self, text):
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text).replace('"', "'")

    def check_year(self, year):
        return

    def scrape_events(self):
        events = self.page.find(id='Events').parent
        scraped, siblings = [], []

        # traverse siblings and get only <li> elements containing events data
        events = events.find_next_sibling()
        while events.name != 'h2':
            if events.name == 'ul':
                siblings += [c.contents for c in events.children if c.name]
            events = events.find_next_sibling()

        for sib in siblings:
            tmp = []
            for s in sib:
                if s.name != 'sup':
                    tmp += [self.strip_html(str(s.contents[0]))] if s.name else [self.strip_html(str(s))]

            # get year and description
            tmp = ''.join(tmp).split(' – ', 1)

            # check if the date is AD or BC or an interval
            check_year = len(tmp[0].split(' '))
            # case '1701 to 1800   – see January 12'
            if check_year > 2:
                pass
            # case '42 BC – The Roman Senate...'
            else:
                if check_year == 2:
                    split_year = tmp[0].split(' ')
                    if split_year[0] == 'AD':
                        year, label, description = int(split_year[1]), split_year[0], tmp[1]
                    else:
                        year, label, description = int(split_year[0]), 'BC', tmp[1]

                # easy case
                else:
                    year, label, description = int(tmp[0]), 'AD', tmp[1]

                scraped.append((year, label, description))

        return scraped

    def scrape_birth(self):
        births = self.page.find(id='Births').parent.find_next_sibling()
        for child in births.children:
            try:
                tmp = []
                for nephew in child.contents:
                    if nephew.name:
                        tmp.append(str(nephew.contents[0]))
                    else:
                        tmp.append(str(nephew))
                tmp = ''.join(tmp).split(' – ', 1)
                year = int(tmp[0].rstrip())
                tmp = tmp[1].split(',', 1)
                person = tmp[0]
                tmp = tmp[1].split('(', 1)
                # check if death year present or not
                if len(tmp) > 1:
                    role, death_year = tmp[0].strip(), int(tmp[1][2:-1])
                    return year, person, role, death_year
                    # self.dbms.insert_birth(year, person, role, death_year)
                else:
                    role = tmp
                    return year, person, role
                    # self.dbms.insert_birth(year, person, role)
            except:
                pass

    def scrape_death(self):
        deaths = self.page.find(id='Deaths').parent.find_next_sibling()
        for child in deaths.children:
            try:
                tmp = []
                for nephew in child.contents:
                    if nephew.name:
                        tmp.append(str(nephew.contents[0]))
                    else:
                        tmp.append(str(nephew))
                tmp = ''.join(tmp).split(' – ', 1)
                year = int(tmp[0].rstrip())
                tmp = tmp[1].split(',', 1)
                person = tmp[0]
                tmp = tmp[1].split('(', 1)
                # check if death year present or not
                role, birth_year = tmp[0].strip(), int(tmp[1][2:-1])

                return year, person, role, birth_year

            except:
                pass
