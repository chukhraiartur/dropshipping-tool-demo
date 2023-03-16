from serpapi import EbaySearch, WalmartSearch
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import time, os, Levenshtein


def get_walmart_results(query: str) -> list:
    params = {
        'api_key': os.getenv('SERPAPI_API_KEY'),    # https://serpapi.com/manage-api-key
        'engine': 'walmart',                        # search engine
        'query': query,                             # search query
    }

    search = WalmartSearch(params)                  # data extraction on the SerpApi backend
    results = search.get_dict()                     # JSON -> Python dict
    
    return results.get('organic_results', [])


def get_ebay_results(query: str) -> list:
    params = {
        'api_key': os.getenv('SERPAPI_API_KEY'),    # https://serpapi.com/manage-api-key
        'engine': 'ebay',                           # search engine
        '_nkw': query,                              # search query
        'ebay_domain': 'ebay.com',                  # ebay domain
    }

    search = EbaySearch(params)                     # data extraction on the SerpApi backend
    results = search.get_dict()                     # JSON -> Python dict
    
    return results.get('organic_results', [])


def compare_walmart_with_ebay(query: str, number_of_products: int, percentage_of_uniqueness: float) -> list:
    data = []

    walmart_results = get_walmart_results(query)

    for walmart_result in walmart_results[:number_of_products]:
        ebay_results = get_ebay_results(walmart_result.get('title'))

        for ebay_result in ebay_results:
            if Levenshtein.ratio(walmart_result.get('title'), ebay_result.get('title')) < percentage_of_uniqueness:
                continue

            walmart_price = walmart_result.get('primary_offer', {}).get('offer_price')
            ebay_price = ebay_result.get('price', {}).get('extracted')

            if not ebay_price:
                ebay_price = ebay_result.get('price', {}).get('from', {}).get('extracted')

            profit = 0

            if walmart_price and ebay_price:
                profit = round(walmart_price - ebay_price, 2)

            data.append({
                'Walmart': {
                    'thumbnail': walmart_result.get('thumbnail'),
                    'title': walmart_result.get('title'),
                    'link': walmart_result.get('product_page_url'),
                    'price': walmart_price
                },
                'eBay': {
                    'thumbnail': ebay_result.get('thumbnail'),
                    'title': ebay_result.get('title'),
                    'link': ebay_result.get('link'),
                    'price': ebay_price
                },
                'Profit': profit
            })

    return data


def compare_ebay_with_walmart(query: str, number_of_products: int, percentage_of_uniqueness: float) -> list:
    data = []

    ebay_results = get_ebay_results(query)

    for ebay_result in ebay_results[:number_of_products]:
        walmart_results = get_walmart_results(ebay_result.get('title'))

        for walmart_result in walmart_results:
            if Levenshtein.ratio(ebay_result.get('title'), walmart_result.get('title')) < percentage_of_uniqueness:
                continue

            ebay_price = ebay_result.get('price', {}).get('extracted')
            walmart_price = walmart_result.get('primary_offer', {}).get('offer_price')

            if not ebay_price:
                ebay_price = ebay_result.get('price', {}).get('from', {}).get('extracted')
            
            profit = 0

            if ebay_price and walmart_price:
                profit = round(ebay_price - walmart_price, 2)

            data.append({
                'eBay': {
                    'thumbnail': ebay_result.get('thumbnail'),
                    'title': ebay_result.get('title'),
                    'link': ebay_result.get('link'),
                    'price': ebay_price
                },
                'Walmart': {
                    'thumbnail': walmart_result.get('thumbnail'),
                    'title': walmart_result.get('title'),
                    'link': walmart_result.get('product_page_url'),
                    'price': walmart_price
                },
                'Profit': profit
            })

    return data


def create_table(data: list, where_to_sell: str):
    with open('table_style.css') as file:
        style = file.read()

    products = ''
    
    for product in data:
        profit_color = 'lime' if product.get('Profit') >= 0 else 'red'

        if where_to_sell == 'Walmart':
            products += f'''
            <tr>
                <td><div><img src="{product['Walmart']['thumbnail']}" width="50"></div></td>
                <td><div><a href="{product['Walmart']['link']}" target="_blank">{product['Walmart']['title']}</div></td>
                <td><div>{str(product['Walmart']['price'])}$</div></td>
                <td><div><img src="{product['eBay']['thumbnail']}" width="50"></div></td>
                <td><div><a href="{product['eBay']['link']}" target="_blank">{product['eBay']['title']}</div></td>
                <td><div>{str(product['eBay']['price'])}$</div></td>
                <td><div style="color:{profit_color}">{str(product['Profit'])}$</div></td>
            </tr>
            '''
        elif where_to_sell == 'eBay':
            products += f'''
            <tr>
                <td><div><img src="{product['eBay']['thumbnail']}" width="50"></div></td>
                <td><div><a href="{product['eBay']['link']}" target="_blank">{product['eBay']['title']}</div></td>
                <td><div>{str(product['eBay']['price'])}$</div></td>
                <td><div><img src="{product['Walmart']['thumbnail']}" width="50"></div></td>
                <td><div><a href="{product['Walmart']['link']}" target="_blank">{product['Walmart']['title']}</div></td>
                <td><div>{str(product['Walmart']['price'])}$</div></td>
                <td><div style="color:{profit_color}">{str(product['Profit'])}$</div></td>
            </tr>
            '''

    table = f'''
    <style>
        {style}
    </style>
    <table border="1">
        <thead>
            <tr>
                <th colspan="3"><div>{list(data[0].keys())[0]}</div></th>
                <th colspan="3"><div>{list(data[0].keys())[1]}</div></th>
                <th><div>{list(data[0].keys())[2]}</div></th>
            </tr>
        </thead>
        <tbody>{products}</tbody>
    </table>
    '''

    return table


def save_to_json(data: list):
    json_file = pd.DataFrame(data=data).to_json(index=False, orient='table')
    
    st.download_button(
        label='Download JSON',
        file_name='comparison-results.json',
        mime='application/json',
        data=json_file,
    )


def save_to_csv(data: list):
    csv_file = pd.DataFrame(data=data).to_csv(index=False)

    st.download_button(
        label='Download CSV',
        file_name='comparison-results.csv',
        mime='text/csv',
        data=csv_file
    )


def main():
    st.title('💸Product Comparison')
    st.markdown(body='This demo compares products from Walmart and eBay to find a profit. SerpApi Demo Project ([repository](https://github.com/chukhraiartur/dropshipping-tool-demo)). Made with [Streamlit](https://streamlit.io/) and [SerpApi](http://serpapi.com/) 🧡')

    if 'visibility' not in st.session_state:
        st.session_state.visibility = 'visible'
        st.session_state.disabled = False

    SEARCH_QUERY: str = st.text_input(
        label='Search query',
        placeholder='Search',
        help='Multiple search queries is not supported.'
    )
    WHERE_TO_SELL = st.selectbox(
        label='Where to sell',
        options=('Walmart', 'eBay'),
        help='Select the platform where you want to sell products. The program will look for the same products on another site and calculate the profit.'
    )
    NUMBER_OF_PRODUCTS: int = st.slider(
        label='Number of products to search',
        min_value=1,
        max_value=20,
        value=10,
        help='Limit the number of products to analyze.'
    )
    PERCENTAGE_OF_UNIQUENESS: int = st.slider(
        label='Percentage of uniqueness',
        min_value=1,
        max_value=100,
        value=50,
        help='The percentage of uniqueness is used to compare how similar one title is to another. The higher this parameter, the more accurate the result.'
    )
    SAVE_OPTION = st.selectbox(
        label='Choose file format to save',
        options=(None, 'JSON', 'CSV'),
        help='By default data won\'t be saved. Choose JSON or CSV format if you want to save the results.'
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col3:
        submit_button_holder = st.empty()
        submit_search = submit_button_holder.button(label='Compare products')

    if submit_search and not SEARCH_QUERY:
        st.error(body='Looks like you click a button without a search query. Please enter a search query 👆')
        st.stop()

    if submit_search and SEARCH_QUERY and WHERE_TO_SELL:
        with st.spinner(text='Parsing Product Data...'):
            comparison_results = []

            if WHERE_TO_SELL == 'Walmart':
                comparison_results = compare_walmart_with_ebay(SEARCH_QUERY, NUMBER_OF_PRODUCTS, PERCENTAGE_OF_UNIQUENESS/100)
            elif WHERE_TO_SELL == 'eBay':
                comparison_results = compare_ebay_with_walmart(SEARCH_QUERY, NUMBER_OF_PRODUCTS, PERCENTAGE_OF_UNIQUENESS/100)

        parsing_is_success = st.success('Done parsing 🎉')
        time.sleep(1)
        parsing_is_success.empty()
        submit_button_holder.empty()

        comparison_results_header = st.markdown(body='#### Comparison results')

        if comparison_results:
            table = create_table(comparison_results, WHERE_TO_SELL)
            components.html(table, height=len(comparison_results)*62 + 40)
            time.sleep(1)

        with col3:
            start_over_button_holder = st.empty()
            start_over_button = st.button(label='Start over')  # centered button

        if SAVE_OPTION and comparison_results:
            with st.spinner(text=f'Saving data to {SAVE_OPTION}...'):
                if SAVE_OPTION == 'JSON':
                    save_to_json(comparison_results)
                elif SAVE_OPTION == 'CSV':
                    save_to_csv(comparison_results)

            saving_is_success = st.success('Done saving 🎉')

            time.sleep(1)
            saving_is_success.empty()
            submit_button_holder.empty()

            start_over_info_holder = st.empty()
            start_over_info_holder.error(body='To rerun the script, click on the "Start over" button, or refresh the page.')

            if start_over_button:
                comparison_results_header.empty()
                start_over_button_holder.empty()
                start_over_info_holder.empty()

        if SAVE_OPTION and not comparison_results:
            comparison_results_header.empty()

            no_data_holder = st.empty()
            no_data_holder.error(body='No product found. Click "Start Over" button and try different search query.')

            if start_over_button:
                no_data_holder.empty()
                start_over_button_holder.empty()

        if SAVE_OPTION is None and comparison_results:
            start_over_info_holder = st.empty()
            start_over_info_holder.error(body='To rerun the script, click on the "Start over" button, or refresh the page.')

            if start_over_button:
                comparison_results_header.empty()
                start_over_button_holder.empty()
                start_over_info_holder.empty()

        if SAVE_OPTION is None and not comparison_results:
            comparison_results_header.empty()

            no_data_holder = st.empty()
            no_data_holder.error(body='No product found. Click "Start Over" button and try different search query.')

            if start_over_button:
                comparison_results_header.empty()
                no_data_holder.empty()
                start_over_button_holder.empty()


if __name__ == '__main__':
    main()