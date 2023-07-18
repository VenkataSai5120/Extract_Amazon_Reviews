import pandas as pd
import requests
from bs4 import BeautifulSoup

# while True:
#     proxy = {
#         "http": f"http://Kh072ICB0vRFuRg9:wifi;;@proxy.soax.com:{9000 + random.randint(0, 9)}",
#         "https": f"http://Kh072ICB0vRFuRg9:wifi;;@proxy.soax.com:{9000 + random.randint(0, 9)}"
#     }
#     response = requests.get("http://checker.soax.com/api/ipinfo", proxies = proxy)
#     print(response)

review_list = []

def extract_reviews(review_url):
    r = requests.get(review_url)
    response = r.text
    soup = BeautifulSoup(response, 'html.parser')
    reviews = soup.find_all('div', {'data-hook':"review"})

    for item in reviews:
        # with open('filehtml/file.html', 'w', encoding='utf-8') as f:
        #     f.write(str(item))
        review = {
            'Product Title' : soup.title.text.replace('Amazon.in:Customer reviews:', '').strip(),
            'Review Title' : item.find('a', {'data-hook' : "review-title"}).text.strip(),
            'Rating' : item.find('i', {'data-hook' : "review-star-rating"}).text.strip(),
            'Review Body' : item.find('span', {'data-hook' : "review-body"}).text.strip()
        }
        review_list.append(review)

    return len(reviews)

def find_total_reviews(review_url):
    response = requests.get(review_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)
    pages = soup.find('div', {'data-hook' : "cr-filter-info-review-rating-count"})
    num = pages.text.strip().split(', ')[1].split(' ')[0]
    total_pages = ""
    for i in num:
        if i.isdigit():
            total_pages += i
    return int(total_pages)


def main():
    product_url = "https://www.amazon.in/Heads-900-Wired-Headphones-White/dp/B078W65FJ7/ref=sr_1_15"
    review_url = product_url.replace("dp", "product-reviews") + "?productNumber=" + str(1)
    total_reviews = -1

    while total_reviews == -1:
        try :
            total_reviews = find_total_reviews(review_url)
        except Exception as e:
            continue

    i = 0
    print(total_reviews)
    while i < total_reviews // 10:
        print(f'Running Page : {i}')
        try :
            review_url = product_url.replace('dp', 'product-reviews') + '?pageNumber' + str(i)
            num = extract_reviews(review_url)
        except Exception as e :
            print(e)
        
        if num != 10:
            i -= 1
        i += 1

    df = pd.DataFrame(review_list)
    df.to_excel('All_Reviews.xlsx', index = False)
    df.to_csv('All_R.csv')

main()
