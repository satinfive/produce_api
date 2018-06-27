import scrapy
import scrapy_splash
import os
from imgurpython import ImgurClient
from .config import API_SECRET, API_CLIENT
from ..items import ImgData
import csv
from .utils import kor_to_utf8

destination_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../tmp.txt')


class PersonalSpider(scrapy.Spider):

    name = "personal"

    start_urls = ['https://www.reddit.com/r/Produce48/wiki/profiles',
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy_splash.SplashRequest(url=url, callback=self.parse, endpoint='render.html')

    def parse(self, response):

        filas = response.css('tr')
        rows = [['name_rom', 'name_kor', 'agency', 'birth', 'blood_type', 'height', 'weight', 'trainee_period', 'hobbies', 'speciality',
                 'url_video']]

        with open('personal_data.csv', 'w') as csvf:
            writer = csv.writer(csvf)
            writer.writerows(rows)

            for fila in filas:
                campos = fila.css('td')
                enlaces = campos.css('a::attr(href)').extract()
                url_imagen = enlaces[0] if enlaces else None
                url_video = enlaces[1] if len(enlaces) > 1 else None
                textos = campos.css('::text').extract()
                nombre = textos[0] if textos else None
                if nombre is None:
                    continue
                if textos:
                    trash = ['Eng', ', ', 'Raw', '. ']
                    textos = [el for el in textos if el not in trash]
                nombre_splitted = nombre.split('(')  # nom_rom ,nom_kor)
                nombre_rom = nombre_splitted[0]
                if nombre_rom[-1] == ' ':
                    nombre_rom = nombre_rom[:-1]
                nombre_cor = kor_to_utf8(nombre_splitted[1].replace(')', ''))
                textos = textos[1:]
                textos = [nombre_rom, nombre_cor] + textos + [url_video]
                writer.writerow(textos)
                # yield response.follow(url_imagen, callback=self.parse)

        if 'imgur.com/a/' in response.url:

            nombre = response.css('div.post-header').css('h1::text').extract()[0]
            nombre_rom = nombre.split('(')[0]
            if nombre_rom[-1] == ' ':
                nombre_rom = nombre_rom[:-1]
            album_id = response.url.split('/')[-1]
            client = ImgurClient(API_CLIENT, API_SECRET)
            imagenes = [img.link for img in client.get_album_images(album_id)]
            with open('imag_data.csv', 'a') as csv_im:
                writer = csv.writer(csv_im)
                writer.writerow([nombre_rom, ','.join(imagenes)])
            yield ImgData(image_urls=imagenes, idol_name=nombre_rom)