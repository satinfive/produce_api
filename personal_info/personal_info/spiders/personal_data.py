import scrapy
import scrapy_splash
import os
from imgurpython import ImgurClient
from .config import API_SECRET, API_CLIENT

destination_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../tmp.txt')


class PersonalSpider(scrapy.Spider):

    name = "personal"
    start_urls = ['https://imgur.com/a/8A2Y2XI',
                  ]
    # start_urls = ['https://www.reddit.com/r/Produce48/wiki/profiles',
    #               ]
    # start_urls = ['http://produce48.mnet.com/pc/rank/1',
    #               ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy_splash.SplashRequest(url=url, callback=self.parse, endpoint='render.html')

    def parse(self, response):

        filas = response.css('tr')
        for fila in filas:
            campos = fila.css('td')
            enlaces = campos.css('a::attr(href)').extract()
            url_imagen = enlaces[0] if enlaces else None
            url_video = enlaces[1] if len(enlaces) > 1 else None
            textos = campos.css('::text').extract()
            nombre = textos[0] if textos else None
            if textos:
                while textos[-1] == 'Eng' or textos[-1] == ', ' or textos[-1] == 'Raw':
                    textos.pop()
            print nombre, url_imagen, textos

        if 'imgur.com/a/' in response.url:

            nombre = response.css('div.post-header').css('h1::text').extract()[0]
            nombre_rom = nombre.split('(')[0]
            if nombre_rom[-1] == ' ':
                nombre_rom = nombre_rom[:-1]
            album_id = response.url.split('/')[-1]
            client = ImgurClient(API_CLIENT, API_SECRET)
            imagenes = [img.link for img in client.get_album_images(album_id)]
            yield ImgData(image_urls=imagenes, idol_name=nombre_rom)


            # imagenes = response.css('.album-view-image-link a').extract()
            # print nombre
            # print imagenes


        # descBox = response.css('div.descBox')
        # imagen = descBox.css('.descLeft').css('img::attr(src)').extract()[0]
        # descRight = descBox.css('.descRight')
        # nombre_aux = descRight.css('dt').css('p')[1]
        # nombre_cor = nombre_aux.css('::text')[0].extract().replace(' ', '')
        # nombre_rom = nombre_aux.css('::text')[1].extract()
        # print nombre_cor
        # print normalice_romaji_name(nombre_rom)


        # if 'rank' in response.url:
        #
        #     for a in response.css('li'):
        #         j = a.css('a')
        #         if j:
        #             profile_urls = [link
        #                            for link in j.css("a::attr(href)").extract()
        #                            if 'profile' in link]
        #
        #             if not profile_urls or profile_urls[0].split("/")[-1] == '0':
        #                 continue
        #
        #             valid_profile_url = profile_urls[0]
        #             next_page = response.urljoin(valid_profile_url)
        #             yield scrapy_splash.SplashRequest(next_page, callback=self.parse)
        #
        # else:
        #     print destination_dir
        #     if not os.path.isdir(destination_dir):
        #         print 'joli'
        #         with open('tmp.txt', 'wb') as f:
        #             f.write(response.body)

