import os
from PIL import Image
from bing_image_downloader import downloader
import random
from bokeh.models.widgets import Div
from joblib import dump, load
import shutil
import streamlit as st
import webbrowser

model_impact = load('Fashionmodel.joblib')

def delete_everything(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def predictfun(gender, age, fashion_type, country, color):
    try:
        deleted_folder='Final_Data'
        delete_everything(deleted_folder)
    except:
        pass
    
    gen = 0 if gender == "Male" else 1
    
    fashionType = 0 if fashion_type == "Wedding" else \
                  1 if fashion_type == "Job" else \
                  2 if fashion_type == "Party" else \
                  3 if fashion_type == "Daily_Life" else 0
    
    result = model_impact.predict([[gen, age, fashionType]])[0]
    
    fashionBook = {
        0: ['Sherwani', 'Pent coat', 'Achkan', 'Waist-coat suit', 'Shalwar kameez', 'Kurta Pajama', 'Kurta with Waistcoat', 'Tuxedo suit'],
        1: ['Lehenga Choli', 'Anarkali Suit', 'Sharara', 'Gharara', 'Bridal Lehenga', 'Saree', 'Anarkali Gown', 'Maxi', 'Frock', 'Kurta Pajama', 'Shalwar kameez'],
        2: ['Suit and Tie', 'Dress Shirt with Dress Pants', 'Blazer with Chinos', 'Collared Shirt with Jeans', 'Sweater with Dress Pants', 'Polo Shirt with Jeans', 'Casual Button-Down Shirt with Khakis', 'Expressive Shirts with Tailored Pants'],
        3: ['Formal Suit with Dress Shirt or Kameez and Trousers', 'Traditional Shalwar Kameez with Dupatta (formal style)', 'Kurti or Tunic with Trousers or Palazzos', 'A-line Kurta with Churidar or Cigarette Pants', 'Casual Kurti with Jeans or Leggings', 'Printed Blouse with Smart Trousers or Culottes', 'Informal Kurti or Top with Jeans or Khakis', 'Casual Salwar Kameez with Straight Pants', 'Funky/Artistic Blouses or Tunics with Tailored Pants or Skirts', 'Fusion Wear combining traditional elements like a Kameez with modern cuts or styles'],
        4: ['Polo Shirt with Jeans', 'Short-sleeved Button-Down Shirt with Chinos', 'Blazer with T-shirt and Jeans', 'Dress Shirt with Dressy Jeans or Chinos', 'Dress Shirt with Dress Pants', 'Blazer with Dress Pants', 'Collared Shirt with Chinos', 'Sweater with Smart Trousers', 'Dress Shirt with Dark Suit', 'Dress Shirt with Dress Pants and Tie', 'Tuxedo with Bow Tie', 'Three-Piece Suit', 'Black or Navy Suit with Optional Tie', 'Dress Shirt with Dark Suit and Optional Bow Tie', 'Statement Jacket with Dress Pants', 'Unique Blazer with Trousers'],
        5: ['Printed or Embroidered Kurti with Jeans or Trousers', 'Colorful Casual Shalwar Kameez with Dupatta', 'Kurti with Palazzo Pants or Culottes', 'A-line Kurta with Churidar', 'Embellished Knee-length Kameez with Trousers or Sharara', 'Printed Anarkali Suit or Long Kurti with Elegant Bottoms', 'Formal Kurti or Shirt with Straight Pant', 'A-line Kurta with Trousers', 'Embroidered or Sequined Anarkali Gown or Lehenga', 'Stylish Sharara or Gharara Suit', 'Heavy Embellished Lehenga or Bridal Gown Floor-length Anarkali Gown', 'Traditional Heavy Lehenga Choli with Elegant Jewelry', 'Exquisite Saree with Luxurious Embellishments', 'Fusion Wear combining Traditional and Modern Elements', 'Unique Designer Dress with Cultural Influences'],
        6: ['T-Shirt and Jeans', 'Shalwar Kameez,Polo Shirt with Chinos Kurta with Jeans or Trousers', 'Button-Down Shirt with Dress Pants', 'Polo Shirt with Shorts', 'Shalwar Kameez, Casual Shirt with Trousers', 'Blazer with Dress Pants'],
        7: ['T-Shirt with Jeans or Leggings', 'Kurti with Trousers or Jeans', 'Salwar Kameez', 'Kurti with Leggings or Palazzos', 'Casual Blouse with Trousers or Jeans', 'Salwar Kameez or Churidar', 'Salwar Kameez or Straight Suit', 'Casual Kurti with Trousers', 'Traditional Saree or Shalwar Kameez']
    }
    
    fashion = fashionBook.get(result)
    random_fashion = []
    
    for i in range(3):
        if gen == 0:
            random_fashion.append("Male" + " " + fashion[random.randrange(0, len(fashion))] + " " + fashion_type + " " + country + " " + color)
        elif gen == 1:
            random_fashion.append("female" + "" + fashion[random.randrange(0, len(fashion))] + " " + fashion_type + " " + country + " " + color)
    
    for i in range(len(random_fashion)-1):
        downloader.download(random_fashion[i], limit=2, output_dir='Final_Data', adult_filter_off=True, force_replace=False, timeout=60, verbose=True)
    
    main_directory = 'Final_Data'
    images = []
    
    for root, _, files in os.walk(main_directory):
        for file in files:
            if file.endswith(('png', 'jpg', 'jpeg', 'gif')):
                try:
                    image_path = os.path.join(root, file)
                    images.append(image_path)
                except Exception as e:
                    print(f"Error reading {file}: {e}")
    if(os.path.exists(images[0])):
        st.image(images[0], caption='Generated Image', use_column_width=True)
    if(os.path.exists(images[1])):
        st.image(images[1], caption='Generated Image', use_column_width=True)
    if(os.path.exists(images[2])):
        st.image(images[2], caption='Generated Image', use_column_width=True)
    
     
    #return images[0], images[1], images[2]


def main():
    st.title("Fashion Prediction")
    nav_options = ["Home", "About", "Localhost"]
    # Render the navigation bar
    selected_page = st.sidebar.radio("Navigation", nav_options)
    # Render content based on the selected page
    if st.button('Go to Streamlit'):
        js = "window.open('http://localhost/Plantix/PHP/services.php')"  # New tab or window
        js = "window.location.href = 'http://localhost/Plantix/PHP/services.php'"  # Current tab
        html = '<img src onerror="{}">'.format(js)
        div = Div(text=html)
        st.bokeh_chart(div)
    elif selected_page == "About":
       st.write("This is the About page.")
    elif selected_page == "Localhost":
       st.write("Redirecting to localhost webpage...")
       # Open the localhost webpage in the browser
       webbrowser.open_new_tab("http://localhost/Plantix/PHP/services.php")
    gender = st.radio("Select Gender", ("Male", "Female"))
    age = st.number_input("Enter Your Age", min_value=0, max_value=150, step=1, value=20)
    fashion_type = st.radio("Select Fashion Type", ("Wedding", "Job", "Party", "Daily_Life"))
    country = st.text_input("Enter Country Name")
    color = st.text_input("Enter Dress Color")
    if st.button("Predict"):
        predictfun(gender,age,fashion_type,country,color)
if __name__ == '__main__':
    main()
