import requests

def search_books(title):
    url= f"https://openlibrary.org/search.json?q={title}"
    response = requests.get(url)

    if response.status_code != 200:
        print("Error: Fail to connect with API")
        return []
    data = response.json()
    results = data.get("docs",[])[:5]   #pruebo con 5 titulos, TODO: paginados de resultados...
    books=[]
    
    for doc in results:
        title = doc.get("title")
        key = doc.get("key")
        if title and key:
            books.append({
                "Title" : title,
                "Link" : f"https://openlibrary.org{key}"
            })
    
    return books