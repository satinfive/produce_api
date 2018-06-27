# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.misc import md5sum


class PersonalInfoPipeline(object):
    def process_item(self, item, spider):
        return item


class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        idol_name = item["idol_name"]
        for i, image_url in enumerate(item['image_urls']):
            yield scrapy.Request(image_url, meta={'image_name': idol_name+"_"+str(i),
                                                  'ext': image_url.split('.')[-1]})

    def image_downloaded(self, response, request, info):
        checksum = None
        for path, image, buf in self.get_images(response, request, info):
            if checksum is None:
                buf.seek(0)
                checksum = md5sum(buf)
            width, height = image.size
            path = 'full/%s' % response.meta['image_name']+"."+'jpeg'  # **Here Changed**
            # path = 'full/%s' % response.meta['image_name']  # **Here Changed**
            self.store.persist_file(
                path, buf, info,
                meta={'width': width, 'height': height},
                headers={'Content-Type': 'image/jpeg'})
        return checksum