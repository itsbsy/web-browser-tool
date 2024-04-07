from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from src.browser.browser import Browser
from src.browser.search import WebSearch
from src.agents.formatter.formatter import Formatter

app = FastAPI()

@app.get("/")
def read_root():
  return {"message": "Yo, I'm alive! 🚀"}

class QueryParams(BaseModel):
  query: str

@app.post("/get_query")
def create_item(payload: QueryParams):
  return {"message": f"Item '{payload.query}' created successfully"}

class QueryParams(BaseModel):
  queries: list

@app.post("/bowser-search")
def search_queries(payload: dict) -> dict:
  print("Searching for payload...", payload['queries'])
  formatter = Formatter(base_model="mixtral-8x7b-32768")
  results = {}
  
  bing_search = WebSearch()
  browser = Browser() 

  for query in payload['queries']:
      query = query.strip().lower()

      """
      Search for the query and get the first link
      """
      bing_search.search(query)
      print("Searching for query...", query)
      link = bing_search.get_first_link()
      print("Link found...", link)

      """
      Browse to the link and take a screenshot, then extract the text
      """
      browser.go_to(link)

      """
      Formatter Agent is invoked to format and learn from the contents
      """
      print("Extracting text...", browser.extract_text())
      results[query] = formatter.execute(
          browser.extract_text()
      )
      
      browser.close()
  return {"response": results[query]}

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)  