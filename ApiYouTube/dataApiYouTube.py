from googleapiclient.discovery import build
from datetime import datetime, timezone
import pandas as pd
import numpy as np
import json
import os

##################################################################
##################################################################
##################################################################

def dataPlayList(api_Key,playlist_Id,df=True):
    
    k,p = api_Key,playlist_Id
    youtube = build('youtube','v3',developerKey=k)
    videos = []

    nextPageToken = None
    # Inicio del bucle infinito
    while True: 
        pl_request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=p, #link de play list
            maxResults=50,
            pageToken=nextPageToken)

        pl_response = pl_request.execute()

        vid_ids = [] #  Solicitando id de los videos en la playlist
        # bucle que navega entre los id de los videos en la playlist
        for item in pl_response['items']:
            vid_ids.append(item['contentDetails']['videoId'])        

        # Objeto que contiene los datos estadísticos de la lista de reproducción dado que usa todas las ids anteriores
        vid_request = youtube.videos().list( # Generando .json de las estadisticas en los videos ( ','.join(vid_ids) ) para extraer luego los likes)
            part = 'statistics,contentDetails,recordingDetails,snippet',
            id = ','.join(vid_ids))        
        vid_response = vid_request.execute()

        # bucle for que crea las filas de la lista que vamos a ejecutar
        for item in vid_response['items']:
            # Vistas
            vid_views = item['statistics']['viewCount']
            # Conteo de me_gusta
            vid_likes = item['statistics']['likeCount']
            # Conteo de no_me_guta (deprecated)
            #vid_dislikes = item['statistics']['dislikeCount']
            # Conteo de favorito
            vid_favorite = item['statistics']['favoriteCount']
            # Conteo de comentarios 
            vid_coments = item['statistics']['commentCount']

            # Duracion del video 
            vid_duration = item['contentDetails']['duration']
            # Dimension del video 
            vid_dimension = item['contentDetails']['dimension']
            # Definicion del video
            vid_definition = item['contentDetails']['definition']
            # Tenencia de subtitulos
            vid_caption = item['contentDetails']['caption']

            # Fecha de subida
            vid_publishedAt = item['snippet']['publishedAt']
            # Titulo del video
            vid_title = item['snippet']['title']
            # link del video
            vid_id = item['id'] # Guardando los ids de los videos en la lista de reproducción
            yt_link = f'https://youtu.be/{vid_id}' # Creando links de los videos en youtube en la lista de reproducción

            # Juntando la lista
            videos.append({ # Creando fila
                'Views': int(vid_views),
                'Likes': int(vid_likes),                    
                    
                #'dislikes' : int(vid_dislikes),
                'Favorite' : int(vid_favorite),
                'Coments' : int(vid_coments),

                'Duration' : vid_duration,
                'Dimension' : vid_dimension,
                'Definition' : vid_definition,
                'Caption' : vid_caption,

                'UploadDate' : vid_publishedAt,
                'Title' : vid_title,

                'URL' : yt_link
                })          

        nextPageToken = pl_response.get('nextPageToken') # contador del bucle

        if not nextPageToken:# Condición de salida del bucle infinito
            break
    
    if df:
        videos = pd.DataFrame(videos)
    
    return(videos)

##################################################################
##################################################################
##################################################################

def dataChannel(api_Key,channel_Id,df=True):
    
    k,c = api_Key,channel_Id
    youtube = build('youtube','v3',developerKey=k)
    videos = []
    
    try:
        res =  youtube.channels().list(
            forUsername=c,
            part='contentDetails').execute()        
        p = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']        
    except:
        res =  youtube.channels().list(
            id=c,
            part='contentDetails').execute()        
        p = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    nextPageToken = None
    # Inicio del bucle infinito
    while True:

        pl_request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=p, #link de play list
            maxResults=50,
            pageToken=nextPageToken)
        pl_response = pl_request.execute()


        vid_ids = [] #  Solicitando id de los videos en la playlist
        # bucle que navega entre los id de los videos en la playlist
        for item in pl_response['items']:
            vid_ids.append(item['contentDetails']['videoId'])        

        # Objeto que contiene los datos estadísticos de la lista de reproducción dado que usa todas las ids anteriores
        vid_request = youtube.videos().list( # Generando .json de las estadisticas en los videos ( ','.join(vid_ids) ) para extraer luego los likes)
            part = 'contentDetails,statistics,recordingDetails,snippet',
            id = ','.join(vid_ids))
        vid_response = vid_request.execute()

        for item in vid_response['items']:
            # Vistas
            vid_views = item['statistics']['viewCount']
            # Conteo de me_gusta
            vid_likes = item['statistics']
            # Conteo de no_me_guta (deprecated)
            #vid_dislikes = item['statistics']['dislikeCount']
            # Conteo de favorito
            vid_favorite = item['statistics']['favoriteCount']
            # Conteo de comentarios 
            vid_coments = item['statistics']

            # Duracion del video 
            vid_duration = item['contentDetails']['duration']
            # Dimension del video 
            vid_dimension = item['contentDetails']['dimension']
            # Definicion del video
            vid_definition = item['contentDetails']['definition']
            # Tenencia de subtitulos
            vid_caption = item['contentDetails']['caption']

            # Fecha de subida
            vid_publishedAt = item['snippet']['publishedAt']
            # Titulo del video
            vid_title = item['snippet']['title']

            # link del video
            vid_id = item['id'] # Guardando los ids de los videos en la lista de reproducción
            yt_link = f'https://youtu.be/{vid_id}' # Creando links de los videos en youtube en la lista de reproducción

            videos.append({# Creando fila
                'Views': int(vid_views),
                'Likes': vid_likes.get('likeCount'), # No todos los videos tienen la posibilidad de likes, en tal caso None
                #'dislikes' : int(vid_dislikes),
                'Favorite' : int(vid_favorite),
                'Coments' : vid_coments.get('commentCount'), # No todos los videos tienen la posibilidad de comentar, en tal caso None

                'Duration' : vid_duration,
                'Dimension' : vid_dimension,
                'Definition' : vid_definition,
                'Caption' : vid_caption,

                'UploadDate' : vid_publishedAt,
                'Title' : vid_title,
                
                'URL' : yt_link
                    })   

        nextPageToken = pl_response.get('nextPageToken') # contador del bucle

        if not nextPageToken:# Condición de salida del bucle infinito
            break
    
    
    
    if df:
        videos = pd.DataFrame(videos)
    
    return(videos)

##################################################################
##################################################################
##################################################################

def dataSearch(api_Key,
               query_Id,
               df=True,
               fechaAntes=datetime.now(timezone.utc).astimezone(),
               fechaDespues= datetime(2005, 2, 15, 0, 0, 0, 0).astimezone(),
               tipo="video",
               idCategoria = 0):
    k,c = api_Key,query_Id
    youtube = build('youtube','v3',developerKey=k)
    videos = []

    nextPageToken = None
    # Inicio del bucle infinito
    while True:

        sch_request = youtube.search().list(
            q=c,
            part='snippet',
            type=tipo,
            maxResults=50,
            publishedBefore = fechaAntes.isoformat(),
            publishedAfter = fechaDespues.isoformat(),
            videoCategoryId = idCategoria,
            pageToken=nextPageToken)
        sch_response = sch_request.execute()

        vid_ids = [] #  Solicitando id de los videos en la busqueda
        # bucle que navega entre los id de los videos en la busqueda
        for item in sch_response['items']:
            vid_ids.append(item['id']['videoId'])

         # Objeto que contiene los datos estadísticos de la lista de reproducción dado que usa todas las ids anteriores
        vid_request = youtube.videos().list( # Generando .json de las estadisticas en los videos ( ','.join(vid_ids) ) para extraer luego los likes)
            part = 'contentDetails,statistics,recordingDetails,snippet',
            id = ','.join(vid_ids))
        vid_response = vid_request.execute()   

        for item in vid_response['items']:
            # Vistas
            vid_views = item['statistics']['viewCount']
            # Conteo de me_gusta
            vid_likes = item['statistics']
            # Conteo de no_me_guta (deprecated)
            #vid_dislikes = item['statistics']['dislikeCount']
            # Conteo de favorito
            vid_favorite = item['statistics']['favoriteCount']
            # Conteo de comentarios 
            vid_coments = item['statistics']

            # Duracion del video 
            vid_duration = item['contentDetails']['duration']
            # Dimension del video 
            vid_dimension = item['contentDetails']['dimension']
            # Definicion del video
            vid_definition = item['contentDetails']['definition']
            # Tenencia de subtitulos
            vid_caption = item['contentDetails']['caption']

            # Fecha de subida
            vid_publishedAt = item['snippet']['publishedAt']
            # Titulo del video
            vid_title = item['snippet']['title']
            # Id del canal
            vid_channelId = item['snippet']['channelId']

            # link del video
            vid_id = item['id'] # Guardando los ids de los videos en la lista de reproducción
            yt_link = f'https://youtu.be/{vid_id}' # Creando links de los videos en youtube en la lista de reproducción

            videos.append({# Creando fila
                'Views': int(vid_views),
                'Likes': vid_likes.get('likeCount'), # No todos los videos tienen la posibilidad de likes, en tal caso None
                #'dislikes' : int(vid_dislikes),
                'Favorite' : int(vid_favorite),
                'Coments' : vid_coments.get('commentCount'), # No todos los videos tienen la posibilidad de comentar, en tal caso None

                'Duration' : vid_duration,
                'Dimension' : vid_dimension,
                'Definition' : vid_definition,
                'Caption' : vid_caption,

                'UploadDate' : vid_publishedAt,
                'Title' : vid_title,
                
                'URL' : yt_link,
                'ChannelId' : vid_channelId
            })  

        nextPageToken = sch_response.get('nextPageToken') # contador del bucle

        if not nextPageToken:# Condición de salida del bucle infinito
            break
    
    if df:
        videos = pd.DataFrame(videos)
        
    return(videos)


##################################################################
##################################################################
##################################################################


def dataComments(api_Key,video_Id,df=True):
    
    k,c = api_Key,video_Id
    youtube = build('youtube','v3',developerKey=k)
    comments = []
    
    nextPageToken = None
    # Inicio del bucle infinito
    while True:

        com_request = youtube.commentThreads().list(
            part="snippet",
            videoId=c,
            maxResults=50,
            order='time',
            pageToken=nextPageToken)  
        com_response = com_request.execute()

        com_ids = [] #  Solicitando id de los comentarios en la busqueda
        # bucle que navega entre los id de los comentarios en la busqueda
        for item in com_response['items']:
            com_ids.append(item['snippet']['topLevelComment']['snippet']['authorChannelId']['value'])
        com_ids

        for item in com_response['items']:
            # Comentario 
            com_Display = item['snippet']['topLevelComment']['snippet']['textDisplay']
            com_Original = item['snippet']['topLevelComment']['snippet']['textOriginal']
            
            # Canal del comentario
            com_AutorName = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
            com_ChannelId = item['snippet']['topLevelComment']['snippet']['authorChannelId']
            com_authorChannelUrl = item['snippet']['topLevelComment']['snippet']['authorChannelUrl'] 
            
            # Conteo de likes
            com_likeCount = item['snippet']['topLevelComment']['snippet']['likeCount']
            
            # Fecha
            com_publishedAt = item['snippet']['topLevelComment']['snippet']['publishedAt']
            com_updatedAt = item['snippet']['topLevelComment']['snippet']['updatedAt']
            
            comments.append({# Creando fila
                'Likes': int(com_likeCount),
                #'dislikes' : int(com_dislikes),
                
                'CommentDisplay': com_Display,
                'CommentOriginal': com_Original,
                'Published': com_publishedAt,
                'Updated':com_updatedAt,                
                
                'Autor': com_AutorName,
                'ChannelId':com_ChannelId,
                'ChannelUrl':com_authorChannelUrl
            })  

        nextPageToken = com_response.get('nextPageToken') # contador del bucle

        if not nextPageToken:# Condición de salida del bucle infinito
            break
    
    if df:
        comments = pd.DataFrame(comments)
        
    return(comments)