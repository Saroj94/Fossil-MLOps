from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse
from uvicorn import run as app_run
from typing import Optional
from src.constants import APP_HOST,APP_PORT
from src.pipline.prediction_pipeline import FossilAgeRegression,FossilPrediction
from src.pipline.training_pipeline import TrainPipeline

"FastApi app"
app=FastAPI()

"Access the css folder which is static"
app.mount("/static", StaticFiles(directory="static"),name="static")

"Set up the jinja template to render the HTML template"
templates=Jinja2Templates(directory='templates')

"Allow all origins for Cross-Origin Resource Sharing (CORS)"
origins = ["*"]

"Configure middleware to handle CORS, allowing requests from any origin"
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FossiDataForm:
    def __init__(self,request:Request):
        self.request:Request=request
        self.uranium_lead_ratio:Optional[float]=None
        self.carbon_14_ratio:Optional[float]=None
        self.radioactive_decay_series:Optional[float]=None
        self.stratigraphic_layer_depth:Optional[float]=None
        self.geological_period:Optional[str]=None
        self.paleomagnetic_data:Optional[str]=None
        self.inclusion_of_other_fossils:Optional[bool]=None
        self.isotopic_composition:Optional[float]=None
        self.surrounding_rock_type:Optional[str]=None
        self.stratigraphic_position:Optional[str]=None
        self.fossil_size:Optional[float]=None
        self.fossil_weight:Optional[float]=None

    async def get_fossil_data(self):
        form=await self.request.form()
        self.uranium_lead_ratio= form.get("uranium_lead_ratio")
        self.carbon_14_ratio= form.get("carbon_14_ratio")
        self.radioactive_decay_series= form.get("radioactive_decay_series")
        self.stratigraphic_layer_depth= form.get("stratigraphic_layer_depth")
        self.geological_period= form.get("geological_period")
        self.paleomagnetic_data= form.get("paleomagnetic_data")
        self.inclusion_of_other_fossils= form.get("inclusion_of_other_fossils")
        self.isotopic_composition= form.get("isotopic_composition")
        self.surrounding_rock_type= form.get("surrounding_rock_type")
        self.stratigraphic_position= form.get("stratigraphic_position")
        self.fossil_size= form.get("fossil_size")
        self.fossil_weight= form.get("fossil_weight")

    @app.get("/", tags=["authentication"])
    async def index(request: Request):
        "Renders the main HTML form page for fossil data input."
        return templates.TemplateResponse("index.html",{"request":request,"context":"Rendering"})
    
    @app.get("/train")
    async def trainRouteClient():
        "Endpoint to initiate the model training pipeline."
        try:
            train_pipeline=TrainPipeline()
            train_pipeline.run_pipeline()
            return Response("Training Successful!!")
        except Exception as e:
            return Response(f"Error Occured! {e}")
        
    @app.post("/")
    async def predictRouteClient(request: Request):
        try:
            form = FossiDataForm(request)
            await form.get_fossil_data()
            fossil_data=FossilPrediction(
                uranium_lead_ratio= form.uranium_lead_ratio,
                carbon_14_ratio= form.carbon_14_ratio,
                radioactive_decay_series= form.radioactive_decay_series,
                stratigraphic_layer_depth= form.stratigraphic_layer_depth,
                geological_period= form.geological_period,
                paleomagnetic_data= form.paleomagnetic_data,
                inclusion_of_other_fossils= form.inclusion_of_other_fossils,
                isotopic_composition= form.isotopic_composition,
                surrounding_rock_type= form.surrounding_rock_type,
                stratigraphic_position= form.stratigraphic_position,
                fossil_size= form.fossil_size,
                fossil_weight= form.fossil_weight
            )    
            fossil_df=fossil_data.get_fossil_input_dataframe()

            ##Initialize the prediction pipeline
            model_predictor=FossilAgeRegression()

            ## Make a prediction and retrieve the result
            value=model_predictor.predict(dataframe=fossil_df)[0]

            # Interpret the prediction result
            status=value

            # Render the same HTML page with the prediction result
            return templates.TemplateResponse(
                "index.html",
                {"request": request, "context": status},
            )
        except Exception as e:
            return {"status": False, "error": f"{e}"}

# Main entry point to start the FastAPI server
if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)

