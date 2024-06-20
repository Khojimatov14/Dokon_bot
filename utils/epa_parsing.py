import asyncio
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from loader import products_db, categories_db


def format_price(price):
    clean_price = price.replace(" ", "").replace(" ", "")
    if "," in clean_price:
        summa = clean_price.split(",")[0]
    else:
        summa = clean_price.split("s")[0]
    return int(summa)


async def create_datas(havola, category, subcategory, product_price):

    response_uz = requests.get(url=f"https://epamarket.uz{havola}")
    response_ru = requests.get(url=f"https://epamarket.uz{havola.replace("/uz", "/ru")}")
    htmldom_uz = BeautifulSoup(response_uz.text, features="html.parser")
    htmldom_ru = BeautifulSoup(response_ru.text, features="html.parser")

    product_title_uz = htmldom_uz.find(name="div", class_="Product_title__cIAXF !leading-[130%]").text.strip()
    product_title_ru = htmldom_ru.find(name="div", class_="Product_title__cIAXF !leading-[130%]").text.strip()

    description_div_uz = htmldom_uz.find(name="div", class_="Product_table__HPY32 mb-3 hidden lg:block")
    description_div_ru = htmldom_ru.find(name="div", class_="Product_table__HPY32 mb-3 hidden lg:block")

    description_key_uz = description_div_uz.find_all(name="div", class_="Product_table_row_key__GDkj8")
    description_key_ru = description_div_ru.find_all(name="div", class_="Product_table_row_key__GDkj8")

    description_val_uz = description_div_uz.find_all(name="div", class_="Product_table_row_val__TxmiP")
    description_val_ru = description_div_ru.find_all(name="div", class_="Product_table_row_val__TxmiP")

    product_description_uz = "\n".join(f"{des_key.text}: {des_val.text}" for des_key, des_val in zip(description_key_uz, description_val_uz))
    product_description_ru = "\n".join(f"{des_key.text}: {des_val.text}" for des_key, des_val in zip(description_key_ru, description_val_ru))


    image_urls = []
    image_div = htmldom_uz.find(name="div", class_="swiper-pagination swiper-pagination-clickable swiper-pagination-bullets swiper-pagination-vertical")
    if image_div:
        image_urls = [img["src"] for img in image_div.find_all(name="img")]
    else:
        single_image_url = htmldom_uz.find(name="div", class_="product-vertical-slider").get("images")
        if single_image_url:
            image_urls.append(single_image_url)

    products_db.add_product(up_category=category,
                            sub_category=subcategory,
                            product_name_uz=product_title_uz,
                            product_name_ru=product_title_ru,
                            product_name_en="none",
                            price=product_price,
                            product_photos=','.join(image_urls),
                            description_uz=product_description_uz,
                            description_ru=product_description_ru,
                            description_en="none",
                            brand_name="epa")


async def get_categories_and_products():

    response_uz = requests.get(url="https://epamarket.uz/uz/catalog/elektr-asboblar")
    # response_ru = requests.get(url="https://epamarket.uz/ru/catalog/elektr-asboblar")
    soup_uz = BeautifulSoup(response_uz.text, features='html.parser')
    # soup_ru = BeautifulSoup(response_ru.text, features='html.parser')

    categories_div_uz = soup_uz.find(name='div', class_='Catolog_left_bar_container_in__Mvnuj')
    # categories_div_ru = soup_ru.find(name='div', class_='Catolog_left_bar_container_in__Mvnuj')

    category_names_uz = categories_div_uz.find_all(name="span", class_="inline-flex h-6 w-6 items-center")
    # category_names_ru = categories_div_ru.find_all(name="span", class_="inline-flex h-6 w-6 items-center")

    subcategory_names_uz = categories_div_uz.find_all(name="ul", class_="category_dropdown_item")
    # subcategory_names_ru = categories_div_ru.find_all(name="ul", class_="category_dropdown_item")



    def format_name(text):
        return text.strip().lower().replace(' ', '-').replace("'", '').replace("(", '').replace(")", '')

    # for category_name_uz, category_name_ru, subcategory_name_uz, subcategory_name_ru in zip(category_names_uz, category_names_ru, subcategory_names_uz, subcategory_names_ru):
    for category_name_uz, subcategory_name_uz in zip(category_names_uz, subcategory_names_uz, ):
        category_name_uz_in = format_name(category_name_uz.find("img")["alt"])

        # categories_db.add_category(up_category="True",
        #                            sub_category=category_name_uz_in,
        #                            category_name_uz=category_name_uz.find("img")["alt"].strip(),
        #                            category_name_ru=category_name_ru.find("img")["alt"].strip())

        # for name_uz, name_ru in zip(subcategory_name_uz, subcategory_name_ru):
        for name_uz in subcategory_name_uz:
            subcategory_name_uz_in = format_name(text=name_uz.text)

            # categories_db.add_category(up_category=category_name_uz_in,
            #                            sub_category=subcategory_name_uz_in,
            #                            category_name_uz=name_uz.text.strip(),
            #                            category_name_ru=name_ru.text.strip())

            driver = webdriver.Safari()
            driver.get(f"https://epamarket.uz/uz/catalog/{category_name_uz_in}/{subcategory_name_uz_in}")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            products_url = BeautifulSoup(driver.page_source, features="html.parser")
            driver.quit()
            pagination_buttons = products_url.find_all(name="a", class_="CustomComponent_pagination_btn__zqDdn")
            page_numbers = [int(btn.find("span").text) for btn in pagination_buttons if btn.find("span")]
            prices = [format_price(price=div.find("span").text) for div in products_url.find_all(name="div", class_="pricing")]

            if prices:
                if page_numbers:
                    last_page_number = max(page_numbers)
                    page_num = 0
                    while True:
                        page_num += 1
                        # page_url = requests.get(url=f"{link}{category_name_uz_in}/{subcategory_name_uz_in}?page={page_num}")
                        driver = webdriver.Safari()
                        driver.get(f"https://epamarket.uz/uz/catalog/{category_name_uz_in}/{subcategory_name_uz_in}?page={page_num}")
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                        products_url_in_page = BeautifulSoup(driver.page_source, features="html.parser")
                        driver.quit()
                        pages_div_in = products_url_in_page.find(name="div", class_="products-grid grid")
                        prices1 = [format_price(price=div.find("span").text) for div in products_url_in_page.find_all(name="div", class_="pricing")]

                        if prices1:
                            for item, price in zip(pages_div_in, prices1):
                                product_url_in = item.find("a")["href"].strip()
                                await create_datas(havola=product_url_in, category=category_name_uz_in, subcategory=subcategory_name_uz_in, product_price=price)
                        if page_num == last_page_number:
                            break
                else:
                    pages_div = products_url.find(name="div", class_="products-grid grid")
                    for item, price in zip(pages_div, prices):
                        product_url_in = item.find("a")["href"].strip()
                        await create_datas(havola=product_url_in, category=category_name_uz_in, subcategory=subcategory_name_uz_in, product_price=price)


async def main():
    await get_categories_and_products()

asyncio.run(main())
