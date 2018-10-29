# encoding=utf-8
import vk
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from time import sleep
from threading import Timer

# Constants
token = 'd7c5861a98ba15886fcc337152774e605599ab88c37a7a23614e1e55773996c2884bfda4efc1508b03793' # токен группы ВК
groupId = 22122847                                                                              # ID группы ВК
photo = 'background3.png'                                                                       # путь к картинке, на которую надо добавить надпись
stepDay = 24                                                                                    # день стипендии (число в месяце)
s = requests.session() 
# Constants

def putText( imageDr, txt0, day, txt1 ):
  txt = 'ДО СТИПЕНДИИ ОСТАЛ{} '.format( txt0 )
  font = ImageFont.truetype( 'pt sans.ttf', 31 )
  imageDr.text( ( 550, 284 ), txt, font = font, fill = ( 0, 0, 0 ) )
  size = font.getsize( txt )
  imageDr.text( ( 550 + size[0], 284 ), str( day ) + ' ', font = ImageFont.truetype( 'pt sans bold.ttf', 31 ), fill = ( 0, 0, 0 ) )
  font = ImageFont.truetype( 'pt sans bold.ttf', 31 )
  size1 = font.getsize( str( day ) + ' ' )
  imageDr.text( ( 550 + size[0] + size1[0], 284 ), txt1, font = ImageFont.truetype( 'pt sans.ttf', 31 ), fill = ( 0, 0, 0 ) )

def createPhoto( photo, stepDay ):
  now = datetime.now()
  now = datetime( now.year, now.month, now.day )
  
  image = Image.open( photo )
  imageDr = ImageDraw.Draw( image )
  
  if now.day == stepDay: imageDr.text( ( 550, 284 ), 'СТИПЕНДИЯ СЕГОДНЯ', font = ImageFont.truetype( 'pt sans.ttf', 31 ), fill = ( 0, 0, 0 ) )
  else:
    if now.day > stepDay: 
      Image.open( 'stock.jpg' ).save( 'uploadPhoto.png' )
      return
    else: toStep = datetime( now.year, now.month, stepDay ) - now
    
    toStep = int( str( toStep ).split( ' ' )[0] )
    
    if toStep == 1 or toStep == 21 or toStep == 31: putText( imageDr, 'СЯ', toStep, 'ДЕНЬ' )
    elif ( toStep > 1 and toStep < 5 ) or ( toStep > 21 and toStep < 25 ): putText( imageDr, 'ОСЬ', toStep, 'ДНЯ' )
    elif ( toStep > 4 and toStep < 21 ) or ( toStep > 24 and toStep < 31 ): putText( imageDr, 'ОСЬ', toStep, 'ДНЕЙ' )
    elif toStep == 21: putText( imageDr, 'СЯ', toStep, 'ДЕНЬ' )
  
  image.save( 'uploadPhoto.png' )

def upload( vkAPI, data, photo ):
  try:
    uploadUrl = vkAPI.photos.getOwnerCoverPhotoUploadServer( group_id = data[2], crop_x = 0, crop_y = 0, crop_x2 = 1590, crop_y2 = 400, v = '5.74' )
    uploadUrl = uploadUrl[ 'upload_url' ] 
    r = s.post( uploadUrl, files = { 'photo' : photo } ).json()
    vkAPI.photos.saveOwnerCoverPhoto( hash = r[ 'hash' ], photo = r[ 'photo' ], v = '5.74' )
  except:
    sleep( 960 )
    upload( vkAPI, data, photo )

def timer( vkAPI, data, lastChecked = None ):
  isTime = True
  #isTime = False
  #day = datetime.now().day
  
  #if lastChecked == None: isTime = True
  #elif lastChecked != day:
    #lastChecked = day
    #isTime = True
  
  if isTime:
    print( 'Update photo...' )
    
    createPhoto( data[3], data[4] )
    photo = open( 'uploadPhoto.png', 'rb' ).read()
    upload( vkAPI, data, photo )
    isTime = False
    
    print( 'Successfully\n' )
  
  sleep( 86400 )
  timer( vkAPI, data, lastChecked )

def main():
  data = ( 1, token, groupId, photo, stepDay )
  
  if not data:
    print( 'Incorrect data' )
    
    return
  
  vkSession = vk.Session( access_token = data[1] )
  vkAPI = vk.API( vkSession )
  timer( vkAPI, data, 17 )
  #T = Timer(15,timer, ( vkAPI, data, 17 ))
  #T.start()

main()
