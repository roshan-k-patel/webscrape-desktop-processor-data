from urllib.request import urlopen as UReq
from bs4 import BeautifulSoup as soup

# List to log the product descriptions - Used to maintain uniqueness
descriptionlog = []

def containerScrape(container):
    container_title = container.find("a", {"class": "item-brand"})
    container_descrption = container.select('a.item-title')[0]
    container_price = container.find("li", {"class": "price-current"})
    container_shipping = container.find("li", {"class": "price-ship"})
    container_link = container.select('a.item-title')[0]['href']
    container_num_reviews = getReviews(container)

    processor_brand = container_title.img["title"]
    description = container_descrption.text.replace(',', ' -')
    price = (container_price.text.strip()).split()[0].replace(',', '')
    shipping = container_shipping.text.strip()
    link = container_link
    num_offers = getOffers(container)
    num_reviews = container_num_reviews.replace('(', '').replace(')', '').replace(',', '')

    return (processor_brand, description, price, shipping, num_offers, num_reviews, link)


def getOffers(container):
    try:
        return container.select('a.price-current-num')[0].text
    except IndexError:
        return "(0 Offers)"

def getReviews(container):
    try:
        return (container.select('span.item-rating-num')[0]).text
    except IndexError:
        return "0"


def mainPageScrape(f):
    address = "https://www.newegg.com/Processors-Desktops/SubCategory/ID-343"

    # opening up connection grabbing the page
    uClient = UReq(address)
    page_html = uClient.read()
    uClient.close()

    # html parsing
    page_soup = soup(page_html, "html.parser")

    # add each processor item container to a list of containers
    containers = page_soup.findAll("div", {"class": "item-container"})

    for container in containers:
        list = (containerScrape(container))
        csv_string = list[0] + "," + list[1] + "," + list[2] + "," + list[3] + "," + list[4] + "," + list[5] + "," + \
                     list[6]
        if descriptionlog.__contains__(list[1]):
            print("Duplicate processor found. Not writing to list.")
        else:
            descriptionlog.append(list[1])
            print(csv_string)
            f.write(csv_string + "\n")

    containers.clear()


def remainingPagesScrape(f):
    page = 2
    duplicateCount = 0
    link = 'https://www.newegg.com/Processors-Desktops/SubCategory/ID-343/Page-'

    while True:
        try:
            address = link + str(page)
            print()
            print("Preparing to Scrape Page: " + str(page))
            print("Address: " + address)
            print()

            # opening up connection grabbing the page
            uClient = UReq(address)
            page_html = uClient.read()
            uClient.close()

            # html parsing
            page_soup = soup(page_html, "html.parser")

            # add each processor item container to a list of containers
            containers = page_soup.findAll("div", {"class": "item-container"})

            for container in containers:
                list = (containerScrape(container))
                csv_string = list[0] + "," + list[1] + "," + list[2] + "," + list[3] + "," + list[4] + "," + list[
                    5] + "," + list[6]
                if descriptionlog.__contains__(list[1]):
                    print("Duplicate processor found. Not writing to list.")
                    duplicateCount = duplicateCount + 1
                else:
                    descriptionlog.append(list[1])
                    print(csv_string)
                    f.write(csv_string + "\n")
            containers.clear()

            if duplicateCount > 100:
                print()
                print("Duplicate Count Is " + str(duplicateCount) + ". This Suggests The Data Is Being Reiterated. The Script Will Stop.")
                print("Processor Scrape Complete")
                print()
                print("Traversed " + str(page) + " Pages")
                print(str(descriptionlog.__len__()) + " Unique Processors Found")
                print()
                print("Data Written To: " + f.name)
                f.close()
                break

            page = page + 1

        except IndexError as e:
            print()
            page = page + 1
           # f.close()
            print("So Far We Have Traversed " + str(page-1) + " Pages")
            print(str(descriptionlog.__len__()) + " Unique Processors Found")
            print(str(duplicateCount) + " Duplicates Ignored")
           # print("Data written to: " + f.name)
           # break


def main():
    filename = "processors.csv"
    f = open(filename, "w")
    headers = "Brand, Description, Cost, Shipping, Offers (No.), Reviews (No.), Link\n"

    f.write(headers)

    mainPageScrape(f)
    remainingPagesScrape(f)


if __name__ == '__main__':
    main()
