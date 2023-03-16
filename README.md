<h1 align="center">Dropshipping Tool Demo 💸</h1>

<p align="center";><a href="https://dropshipping-tool.streamlit.app/">Demonstration of dropshipping tool on Walmart and eBay</a></p>

## Idea

The main idea comes from a tool called [Zik Analytics](https://www.zikanalytics.com/), which used by dropshippers. 

This demo shows a comparison between Walmart and eBay products to determine profit. The user selects a product and a place of sale, and the program finds the same product in another place and calculates the profit. 
 
There are two main fields on the demo:
- The first is the search field in which you need to conduct a query or a specific product. 
- The second field is responsible for the place where the user wants to sell this product. 

In addition to the main fields, there are optional ones: 
- number of products to search slider. 
- percentage of uniqueness slider that uses to compare product names. 
 
As a result, the user receives a table with data such as title, link, thumbnail and price for each product on Walmart and eBay and profit. There is also an option to save the result in JSON or CSV format.

📌Note: Use the dark Streamlit theme to view the table normally.

<details>
<summary>Things to improve</summary>
<ol>
<li>Asynchronous data retrieval.</li>
<li>Add other places for sale (Home Depot).</li>
<li>Add a table display for the light Streamlit theme.</li>
<ol>
</details> 

## Video Example

![comparison-results](https://user-images.githubusercontent.com/81998012/213615345-ca16108f-8698-4162-9ae1-aef87cf19b6d.gif)

This is how comparison results (if any) would look like:

![table](https://user-images.githubusercontent.com/81998012/213613314-63be4777-d77b-4346-bbc0-e4f8327f74b9.png)

## Usage

This section if you want to use your own API key. [The demo on `streamlit`](https://dropshipping-tool.streamlit.app/) doesn't require you to use any API key.

Clone repository:

```bash
$ git clone https://github.com/chukhraiartur/dropshipping-tool-demo.git
```

Install dependencies:

```bash
$ cd dropshipping-tool-demo && pip install -r requriements.txt
```

Add [SerpApi api key](https://serpapi.com/manage-api-key) for current shell and all processes started from current shell:

```bash
# used to parse Walmart and eBay results, has a plan of 100 free searches
$ export SERPAPI_API_KEY=<your-api-key>
```

Run the app:

```bash
$ streamlit run main.py
```

<p align="center";>Sponsored by <a href="https://serpapi.com/">SerpApi</a> 🧡</p>
