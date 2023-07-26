import scrapy
import json


class collect_player_info(scrapy.Spider):
    name = 'players_info'

    def __init__(self):
        try:
            with open('dataset/players_urls.json') as f:
                self.players = json.load(f)
            self.player_count = 1
        except IOError:
            print("File not found")

    def start_requests(self):
        urls = ['https://sofifa.com/player/231747?units=mks']

        # YOUR CODE HERE
        # raise NotImplementedError()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # YOUR CODE HERE
        #   raise NotImplementedError()
        players_info = response.css('body > div.center > .grid > .col.col-12')

        # hàng tuổi, ngày sinh,...
        info = players_info[0].css(
            'div.bp3-card > .info > div.meta.ellipsis::text')[-1]
        index_overall = players_info[0].css(
            'div.bp3-card > .card.spacing > div.block-quarter')
        # profile
        profile = players_info[0].css('div.block-quarter')[4]
        specialities = players_info[0].css('div.block-quarter')[5]
        # teams
        teams = players_info[0].css('div.block-quarter')[6:8]

        # chỉ số cụ thể
        primary_position = response.css(
            'body > div.center > .grid > .col.col-4')
        specific_index = players_info[1].css(
            'div.block-quarter')  # từng mục chỉ số
        name_specific_index = []  # tên thông số cụ thể
        index_specific_index = []  # chỉ số thông số cụ thể
        for i in range(len(specific_index)):
            duplicate_index = specific_index[i].css(
                'div.card > ul.pl > li > span.plus::text').getall()
            duplicate_index += specific_index[i].css(
                'div.card > ul.pl > li > span.minus::text').getall()
            values = specific_index[i].css(
                'div.card > ul.pl > li > span::text').getall()
            values = [i for i in values if i not in duplicate_index] #xóa phần tử chỉ số plus
            
            name_specific_index.append(values[1::2])
            name_specific_index[i] = [
                x.replace(" ", "") for x in name_specific_index[i]]
            index_specific_index.append(values[::2])

        items = {
            "id": profile.css('div.card > ul.pl >.ellipsis::text')[-1].get(),
            "name": players_info[0].css('.info > h1::text').get(),
            "primary_position": primary_position[1].css('ul.pl > li.ellipsis > .pos::text').get(),
            "positions": players_info[0].css('.info > div.meta.ellipsis > span.pos::text').getall(),
            "age": info.get().split(' ')[1][:-4],
            "birth_date": info.get().split(' ')[4][:-1] + '/'+info.get().split(' ')[2][1:] + '/'+info.get().split(' ')[3][:-1],
            "height": int(info.get().split(' ')[5][:-2]),
            "weight": int(info.get().split(' ')[6][:-2]),
            "Overall Rating": int(index_overall.css('span.bp3-tag::text')[0].get()),
            "Potential": int(index_overall.css('span.bp3-tag::text')[1].get()),
            "Value": index_overall.css('div::text')[4].get(),
            "Wage": index_overall.css('div::text')[6].get(),
        }
        #xử lý mục profile
        profile_keys = profile.css(
            'div.card > ul.pl >.ellipsis > label::text').getall()[:-1]
        upper_profile_value = [i for i in profile.css('div.card > ul.pl >.ellipsis::text').getall(
        ) if i != ' '][:-1]
        index_of_upper_profile_value = list(map(int,upper_profile_value[1:]))
        index_of_upper_profile_value.insert(0,upper_profile_value[0])

        profile_values = index_of_upper_profile_value + profile.css('div.card > ul.pl >.ellipsis > span::text').getall()[-4:]
        
        for i in range(len(profile_keys)):
            items[profile_keys[i]] = profile_values[i]
            
        # Xử lý mục teams
        u = {}
        for i in range(len(teams)):
            u[teams.css('div.card > h5 > a::text').getall()[i]] = int(
                teams.css('div.card > ul.ellipsis.pl > li > span.bp3-tag::text')[i].get())
        items["teams"] = u
        
        x = {
            specific_index[0].css('div.card>h5::text').get().lower(): {
                name_specific_index[0][0]: int(index_specific_index[0][0]),
                name_specific_index[0][1]: int(index_specific_index[0][1]),
                name_specific_index[0][2]: int(index_specific_index[0][2]),
                name_specific_index[0][3]: int(index_specific_index[0][3]),
                name_specific_index[0][4]: int(index_specific_index[0][4]),
            },
            specific_index[1].css('div.card>h5::text').get().lower(): {
                name_specific_index[1][0]: int(index_specific_index[1][0]),
                name_specific_index[1][1]: int(index_specific_index[1][1]),
                name_specific_index[1][2]: int(index_specific_index[1][2]),
                name_specific_index[1][3]: int(index_specific_index[1][3]),
                name_specific_index[1][4]: int(index_specific_index[1][4]),
            },
            specific_index[2].css('div.card>h5::text').get().lower(): {
                name_specific_index[2][0]: int(index_specific_index[2][0]),
                name_specific_index[2][1]: int(index_specific_index[2][1]),
                name_specific_index[2][2]: int(index_specific_index[2][2]),
                name_specific_index[2][3]: int(index_specific_index[2][3]),
                name_specific_index[2][4]: int(index_specific_index[2][4]),
            },
            specific_index[3].css('div.card>h5::text').get().lower(): {
                name_specific_index[3][0]: int(index_specific_index[3][0]),
                name_specific_index[3][1]: int(index_specific_index[3][1]),
                name_specific_index[3][2]: int(index_specific_index[3][2]),
                name_specific_index[3][3]: int(index_specific_index[3][3]),
                name_specific_index[3][4]: int(index_specific_index[3][4]),
            },
            specific_index[4].css('div.card>h5::text').get().lower(): {
                name_specific_index[4][0]: int(index_specific_index[4][0]),
                name_specific_index[4][1]: int(index_specific_index[4][1]),
                name_specific_index[4][2]: int(index_specific_index[4][2]),
                name_specific_index[4][3]: int(index_specific_index[4][3]),
                name_specific_index[4][4]: int(index_specific_index[4][4]),
                name_specific_index[4][5]: int(index_specific_index[4][5]),
            },
            specific_index[5].css('div.card>h5::text').get().lower(): {
                name_specific_index[5][0]: int(index_specific_index[5][0]),
                name_specific_index[5][1]: int(index_specific_index[5][1]),
                name_specific_index[5][2]: int(index_specific_index[5][2]),
            },
            specific_index[6].css('div.card>h5::text').get().lower(): {
                name_specific_index[6][0]: int(index_specific_index[6][0]),
                name_specific_index[6][1]: int(index_specific_index[6][1]),
                name_specific_index[6][2]: int(index_specific_index[6][2]),
                name_specific_index[6][3]: int(index_specific_index[6][3]),
                name_specific_index[6][4]: int(index_specific_index[6][4]),
            },
            "player_traits":
                specific_index[7].css(
                    'div.card > ul.pl > li > span::text').getall(),
            "player_specialities": specialities.css('div.card > ul.pl >.ellipsis > a::text').getall()
        }
        items.update(x)
        yield items

        if self.player_count < len(self.players):
            next_page_url = 'https://sofifa.com' + \
                self.players[self.player_count]['player_url'] + '?units=mks'
            self.player_count += 1
            yield scrapy.Request(url=next_page_url, callback=self.parse)

