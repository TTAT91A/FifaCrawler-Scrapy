import scrapy

class collect_player_url(scrapy.Spider):
    name = 'players_urls'
    def __init__(self):
        self.count = 60
    def start_requests(self):
        urls = ['https://sofifa.com/players?col=oa&sort=desc&offset=0']
        # # YOUR CODE HERE
        # raise NotImplementedError()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # YOUR CODE HERE
        # raise NotImplementedError()
        players_url = response.css('tbody > tr')
        for player in players_url:
            id = player.css('td.col-name > a::attr(href)').get().split('/')
            items = {
                "player_url": '/' + id[1] + '/' + id[2]
            }
            yield items

        if self.count < 720:
            next_page = 'https://sofifa.com/players?col=oa&sort=desc&offset=' + str(self.count)
            self.count += 60
            yield response.follow(next_page, callback=self.parse)