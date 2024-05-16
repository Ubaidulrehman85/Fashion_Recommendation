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
    URL_STRING = "http://localhost/weiboo/PHP/index-two.php"
    st.markdown(
    f'<div style="position: absolute; top: 10px; right: 0px;">'
    f'<a href="{URL_STRING}" style="display: inline-block; padding: 12px 20px; background-color: #4CAF50; color: white; text-align: center; text-decoration: none; font-size: 16px; border-radius: 4px;">Action Text on Button</a>'
    f'</div>',
    unsafe_allow_html=True
    )
     
    #return images[0], images[1], images[2]


def main():
    # Add header using HTML
    header="""
    <header id="header" class="header">
    <div class="header-top bg-theme-colored sm-text-center">
      <div class="container">
        <div class="row">
          <div class="col-md-3">
            <div class="widget no-border m-0">
              <ul class="styled-icons icon-dark icon-theme-colored icon-sm sm-text-center">
                <li><a href="#"><i class="fa fa-facebook"></i></a></li>
                <li><a href="#"><i class="fa fa-twitter"></i></a></li>
                <li><a href="#"><i class="fa fa-google-plus"></i></a></li>
                <li><a href="#"><i class="fa fa-linkedin"></i></a></li>
              </ul>
            </div>
          </div>
          <div class="col-md-9">
            <div class="widget no-border m-0">
              <ul class="list-inline pull-right flip sm-pull-none sm-text-center mt-5">
                <li class="m-0 pl-10 pr-10"> <i class="fa fa-phone text-white"></i> <a class="text-white" href="#">03117363526</a> </li>
                <li class="text-white m-0 pl-10 pr-10"> <i class="fa fa-clock-o text-white"></i> Mon-Fri 8:00 to 2:00 </li>
                <li class="m-0 pl-10 pr-10"> <i class="fa fa-envelope-o text-white"></i> <a class="text-white" href="#">ubaidulrehman85@gmail.com</a> </li>
                
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="header-nav">
      <div class="header-nav-wrapper navbar-scrolltofixed bg-lightest">
        <div class="container">
          <nav id="menuzord-right" class="menuzord blue bg-lightest">
            <a class="menuzord-brand pull-left flip" href="javascript:void(0)">
              <img src="images/plantixlogo.png" alt="">
            </a>
            <div id="side-panel-trigger" class="side-panel-trigger"><a href="#"><i class="fa fa-bars font-24 text-gray"></i></a></div>
            <ul class="menuzord-menu">
              <li class=""><a href="index.php">Home</a>
              </li>
				  <li ><a href="about.php">About</a>
                    
                  </li> 
				  <li><a href="services.php">Services</a>
                    
                  </li>
				  <li><a href="contact.php">Contact</a>
                    
                  </li>
                
				  <li><a href="checkup.php">CheckUp</a>
                
                  </li>
              <li><a href="comming_soon.php">Blog</a>
                
              </li>
             
            </ul>
          </nav>
        </div>
      </div>
    </div>
    </header>"""
    st.markdown(header,unsafe_allow_html=True)

    # Your Streamlit app content goes here

    st.title("Fashion Prediction")
    gender = st.radio("Select Gender", ("Male", "Female"))
    age = st.number_input("Enter Your Age", min_value=0, max_value=150, step=1, value=20)
    fashion_type = st.radio("Select Fashion Type", ("Wedding", "Job", "Party", "Daily_Life"))
    country = st.text_input("Enter Country Name")
    color = st.text_input("Enter Dress Color")
    if st.button("Predict"):
        predictfun(gender,age,fashion_type,country,color)
if __name__ == '__main__':
    main()
