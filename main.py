from database import db
import wikipedia
from bs4 import BeautifulSoup
from scraper import sc


months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

days = [i for i in range(1, 32)]

def main():
    dbms = db.MyDatabase(db.SQLITE, dbname='db.sqlite')
    dbms.create_db_tables()
    day_id = 1
    for month in months:
        for day in days:
            print('\nStarted inserting data for {} {}\n'.format(month, str(day)))
            # insert day by day
            dbms.insert_date(day_id, "{} {}".format(month, day))


            if (month == "February" and day > 29) or \
                    ((month == "April" or month == "June" or month == "September" or month == "November") and day > 30):
                break
            else:
                page = BeautifulSoup(wikipedia.WikipediaPage('{} {}'.format(month, str(day))).html(),
                                     features="html.parser")

                scraper = sc.Scraper(page)

                for event in scraper.scrape_events():
                    year, label, description = event[0], event[1], event[2]
                    dbms.insert_event(day_id, "{} {}".format(month, day), year, label, description)

                dbms.insert_event(year, description)

                birth = scraper.scrape_birth()
                if len(birth) == 4:
                    year, person, role, death_year = birth
                    dbms.insert_birth(year, person, role, death_year)
                elif len(birth) == 3:
                    year, person, role = birth
                    dbms.insert_birth(year, person, role)

                year, person, role, birth_year = scraper.scrape_death()
                dbms.insert_death(year, person, role, birth_year)

            print('\nFinished inserting to data for {} {}\n'.format(month, str(day)))
            day_id += 1

    return

if __name__ == "__main__":
    main()
