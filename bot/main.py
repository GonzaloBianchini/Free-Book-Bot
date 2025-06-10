import requests

def search_books(title):
    url= f"https://openlibrary.org/search.json?q={title}"
    response = requests.get(url)

    if response.status_code != 200:
        print("Error: Fail to connect with API")
        return []
    data = response.json()
    
    books=[]
    
    for doc in data.get("docs",[])[:5]:
        title = doc.get("title")
        key = doc.get("key")
        if title and key:
            books.append({
                "Title" : title,
                "Link" : f"https://openlibrary.org{key}"
            })
    
    return books
    
    
#main
    
if __name__ == "__main__":
        query = input(" Ingresá el título de un libro: ") #🔍
        results = search_books(query)
        
        if results:
            print("\n📚 Resultados:")
            for book in results:
                print(f" - {book['Title']}")
                print(f" - {book['Link']}\n")
        else:
            print(" No se encontraron resultados.") #⚠️

        print(results)