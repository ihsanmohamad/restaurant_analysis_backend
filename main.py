from analyze_restaurant import analyze_data

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import googlemaps
import pandas as pd

from slugify import slugify

from fastapi.responses import StreamingResponse

import io

def fastApp() -> FastAPI:
    app = FastAPI(title="Makan Manoi", description="Makan Manoi System")
    
    origins = [
    "https://makanmanoi.netlify.app/",
    "https://makanmanoi.netlify.app",
    "http://makanmanoi.netlify.app",
    "http://192.168.1.9:3000"
]


    app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )
    return app

app = fastApp()

API_KEY = os.environ['API_KEY']

gmaps = googlemaps.Client(key=API_KEY)


@app.get('/search_place')
async def search_place(restaurant: str):
    place_name = restaurant
    lat = 4.924981468858695
    lng = 100.64908965731956
    place = gmaps.places(query=restaurant, type="restaurant", location=(lat, lng))
    data = [] 

    for i in range(len( place['results'])):


        place_result = {
            "name": place['results'][i]['name'],
            "formatted_address": place['results'][i]['formatted_address'],
            "place_id": place['results'][i]['place_id'],
            "rating": int(place['results'][i]['rating']),
            "user_ratings_total": place['results'][i]['user_ratings_total']
        }
        data.append(place_result)

    return data

@app.get('/place_detail')
async def place_detail(place_id: str):
    place_id = place_id

    place = gmaps.place(place_id = place_id)

    return place


   

@app.get('/restaurant_review')
async def get_review(place_id: str):


    place_id = place_id

    place = gmaps.place(place_id=place_id)

    reviews = [] #empty list which will hold dictionaries of review
    if place.get('result', {}).get('reviews')!=None:
        for i in range(len( place['result']['reviews'])):
            text = place['result']['reviews'][i]['text']
            rating = place['result']['reviews'][i]['rating']
            name = place['result']['reviews'][i]['author_name']
            
            reviews.append({
                        'name': name,
                        'rating':rating,
                        'text':text
                        }
                        )
        

        df = pd.DataFrame(reviews)
        result = df.to_dict('records')
        return result

    else:
        return None
    

@app.get('/download_data')
async def download_data(place_id: str):


    place_id = place_id

    place = gmaps.place(place_id=place_id)

    reviews = [] #empty list which will hold dictionaries of review
    
    if place.get('result', {}).get('reviews')!=None:
        for i in range(len( place['result']['reviews'])):
            text = place['result']['reviews'][i]['text']
            rating = place['result']['reviews'][i]['rating']
            
            reviews.append({'rating':rating,
                        'text':text
                        }
                        )
        df = pd.DataFrame(reviews)

        output = io.BytesIO()

        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        
        file_name = slugify(place['result']['name'])
            
        # result = df.to_excel(f"{file_name}.xlsx")
        result = df.to_excel(writer)
        writer.save()
        xlsx_data = output.getvalue()


        return StreamingResponse(io.BytesIO(xlsx_data), media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers={
                "Content-Disposition": f'attachment; filename="{file_name}.xlsx"'
            })
    else:
        return None
    
    
   
    

@app.get('/get_analysis')
async def analysis_data(place_id: str):

    place_id = place_id

    place = gmaps.place(place_id=place_id)

    reviews = [] #empty list which will hold dictionaries of review
    if place.get('result', {}).get('reviews')!=None:
        for i in range(len( place['result']['reviews'])):
            text = place['result']['reviews'][i]['text']
            rating = place['result']['reviews'][i]['rating']
            
            reviews.append({'rating':rating,
                        'text':text
                        }
                        )

        df = pd.DataFrame(reviews)

        result = analyze_data(dataframe=df)
        return result

    else:
        return None
    
