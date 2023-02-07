from selenium import webdriver
import csv, os


def convert_to_float(x):
    try:
        return (float(x))
    except:
        return x


# ================= USER INPUTS
driver = webdriver.Chrome('Chrome Driver')
number_of_players = 2500  # How many players down the rankings do you want to report???
save_location = 'SAVE LOCATION'
year_range = range(2018, 2024)
# =================
with open(os.path.join(save_location, 'CSV SAVE'), mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Year', 'Name', 'High School', 'City', 'State', 'Position', 'Height', 'Weight', 'Service','Rating', 'Nat. Rank', 'Pos. Rank', 'St. Rank', 'Committed', 'School'])
    for year in year_range:
        end_range = number_of_players // 50
        for page in range(1, end_range):
            driver.get(f'https://www.on3.com/db/rankings/industry-comparison/football/{year}/?page={page}')
            for player in driver.find_elements_by_xpath(r'//li@id="__next"]/div/section/main/section/section/ul/li[1]]'):
                try:
                    player_info = [x.text for x in player.find_elements_by_xpath(r'./div/div')[:-1]]
                    if player.find_elements_by_xpath(r'.//div[@class="rankings-page__crystal-ball"]'):
                        # Player hasnt decided a school yet (Going to report multiple schools with top crystal balls.)
                       # percentages = player.find_element_by_xpath(r'.//div[@class="rankings-page__crystal-ball"]').text.split('\n')
                       # schools = [x.get_attribute('alt') for x in player.find_elements_by_xpath(r'.//div[@class="rankings-page__crystal-ball"]/.//img')]
                        #school = ' '.join([school + ' ' + percentage for (school, percentage) in list(zip(schools, percentages))])  # (Team 1 Team 1% Team 2 Team 2 %)
                        committed = False
                    else:
                        school = player.find_elements_by_xpath(r'.//img')[-1].get_attribute('alt')
                        committed = True
                     rank, _, name, position, metrics, rating = player_info
                    height, weight = [x.strip() for x in metrics.split('/')]
                    weight = convert_to_float(weight)
                    height = height.replace('-', ' ft. ')
                    rank = rank.split('\n')
                    rating, ranks = player_info[-1].split('\n')
                    nat_rank, pos_rank, state_rank = (x.strip() for x in ranks.split(' '))
                    nat_rank = convert_to_float(nat_rank)
                    pos_rank = convert_to_float(pos_rank)
                    state_rank = convert_to_float(state_rank)
                    name, home = name.split('\n')
                    city = home[home.find('(') + 1:home.find(',', home.find('(') + 1)].strip()
                    state = home[home.rfind(',') + 1:-1].strip()
                    high_school = home[:home.find('(')].strip()

                    if name in school: school = 'Undecided'  
                    writer.writerow([year, name, high_school, city, state, position, height, weight, float(rating), nat_rank, pos_rank, state_rank, committed, school])
                except:
                    pass
    csv_file.flush()
