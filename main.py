import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import date
import pandas as pd
import plotly.express as px
import base64

def add_local_background(image_path):
    with open(image_path, "rb") as f:
        encoded_image = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url(data:image/png;base64,{encoded_image});
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# Database setup
engine = create_engine('sqlite:///carbon_footprint.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Database models
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

class CarbonData(Base):
    __tablename__ = 'carbon_data'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, default=date.today)
    electricity_kwh = Column(Float, nullable=False)
    vehicle_type = Column(String, nullable=False)
    distance_km = Column(Float, nullable=False)
    diet_type = Column(String, nullable=False)
    meals = Column(Integer, nullable=False)
    garbage_kg = Column(Float, nullable=False)

# Ensure the table structure is updated
Base.metadata.create_all(engine)

# Utility functions for user authentication
def add_user(username, password):
    if session.query(User).filter_by(username=username).first():
        return False
    user = User(username=username, password=password)
    session.add(user)
    session.commit()
    return True

def authenticate_user(username, password):
    user = session.query(User).filter_by(username=username, password=password).first()
    return user

# Streamlit UI for user authentication and main app
def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'

    if st.session_state['logged_in']:
        display_home_page()
    else:
        if st.session_state['page'] == 'login':
            login_page()
        elif st.session_state['page'] == 'signup':
            signup_page()

def login_page():
    st.title("Carbon Footprint Calculator")
    st.subheader("Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = authenticate_user(username, password)
        if user:
            st.session_state['logged_in'] = True
            st.session_state['user_id'] = user.id
            st.session_state['page'] = 'home'
        else:
            st.error("Invalid username or password")

    st.text("Don't have an account?")
    if st.button("Go to Signup"):
        st.session_state['page'] = 'signup'

def signup_page():
    st.title("Create New Account")
    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")
    if st.button("Signup"):
        if add_user(username, password):
            st.success("Account created successfully! Please go back to login.")
            st.session_state['page'] = 'login'
        else:
            st.error("Username already exists!")

    if st.button("Back to Login"):
        st.session_state['page'] = 'login'

# Inject CSS to set a background image for the sidebar
def display_home_page():
    # Read the image and encode it in base64
    image_path = "sidebar.jpg"  # Replace with the correct path to your image
    try:
        with open(image_path, "rb") as f:
            encoded_image = base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        st.error(f"Image file not found: {image_path}")
        return

    # Inject CSS for sidebar background
    st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] {{
            background-image: url(data:image/png;base64,{encoded_image});
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar header
    st.sidebar.markdown(
        """
        <style>
        .custom-header {
            font-size: 20px; /* Increase font size */
            color: #509B4C;
            font-weight: bold; /* Make it bold */
        }
        </style>
        <div class="custom-header">Navigation</div>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar navigation
    options = ["Home", "Add Today's Data", "View Daily Data", "Weekly Overview", "Monthly Overview", "Yearly Overview", "Graphical Data", "Solution"]
    choice = st.sidebar.radio("Select an option", options)

    # Your other page logic here...

    if choice == "Home":

        st.markdown(
    '<h1 style="font-weight:650; font-size:92px; margin-top:-50px;">'
    '<span style="color:#509B4C;">ENVIRO</span> '
    '<span style="color:#509B4C;">TRACKER</span>'
    '</h1>',
    unsafe_allow_html=True
)

        st.markdown('<br><h1 style="font-weight:650; font-size:32px;margin-top:-150px;text-align: center;">'
        '<span style="color:#509B4C;">"Welcome </span> '
        '<span style="color:#CBE8CA;">to  the  Carbon  Footprint Calculator"</span> '
        '</h1>',
        unsafe_allow_html=True)
       

        
        st.markdown(
        '<h1 style="color:#CBE8CA; font-weight:700; font-size:25px; margin-top:-40px;text-align: center;">'
        'Track your daily <span style="color:#509B4C;">Carbon Footprint</span> and make informed      '
        '</h1>',
        unsafe_allow_html=True
)
        st.markdown(
        '<div style="font-weight:700;color:#CBE8CA; text-align: center; font-size:25px;margin-top: -20px;">decisions to reduce it</div>',
        unsafe_allow_html=True
)

        st.markdown('<h1 style="color:#CBE8CA;font-weight:500; font-size:20px;margin-top:-10px;text-align: center;">This tool helps you monitor and reduce your carbon emissions effectively.</h1><br>', unsafe_allow_html=True)        

        st.markdown("### ⚠️ **Current State of Global Emissions**")
        st.markdown('<p style="color:#3C928D;font-weight:300; font-size:28px;margin-top:-5px;">2024 Projection </p>', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 2])
        with col1:
           
            st.markdown('<p style="color:red;font-weight:400; font-size:27px;margin-top:-18px;">37.4B metric tonnes</p>', unsafe_allow_html=True)
            st.markdown('<p style="color:#45CB24; font-size:17px;text-align: center;margin-top: -20px;"> ↟+0.8%(inc.rate)</p>', unsafe_allow_html=True)
        with col2:
                
            st.markdown(
            '<h1 style="color:#CBE8CA; font-weight:600; font-size:18px; margin-top:-35px;">'
            'Global CO2 emissions from fossil fuels are projected to reach a record high of <span style="color:red;"> 37.4 billion metric tons </span>in 2024, representing a <span style="color:red;">0.8% increase</span>from 2023.     '
            '</h1>',
            unsafe_allow_html=True
)

        
        st.divider()

        # India's Contribution
        st.markdown("### 🌏 **India's Contribution**")
        st.write(
            """
            - India’s CO2 emissions are expected to rise by **4.6% in 2024**.
            - India will contribute **8% of the global total**.
            """
        )
        st.divider()

        # Impacts of Carbon Emissions
        st.markdown("### ⚠️ **The Impacts of Carbon Emissions**")
        col3, col4 = st.columns([1, 2])
        with col3:
            st.image(
                "img.jpg",
                width=300,
            )  # Replace with a local or online image URL
        with col4:
            st.write(
                """
                - **Climate Change:** Increasing temperatures and unpredictable weather patterns.
                - **Natural Disasters:** Rising sea levels, floods, and droughts.
                - **Resource Scarcity:** Shortages of water, food, and habitable land.
                - **Global Conflict:** Resource-driven wars, economic collapse, and mass migrations.
                """
            )

        # Call to Action
        st.markdown("### 💡 **Act Now to Mitigate These Risks**")
        st.info("Together, we can reduce our carbon footprint and create a sustainable future.") 
        # Adding Our World in Data graph
        st.markdown("### 🌐 *Historical CO2 Emissions*")
        st.write("Below is a graph showing annual CO2 emissions (including land use) from *Our World in Data*:")
        # Fetch the data
        try:
            df = pd.read_csv("home.csv", encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv("home.csv", encoding='ISO-8859-1')




        # Clean and filter the data for better visualization
        df = df[df['Year'] >= 1850]  # Filter for years from 1850 onwards
        fig = px.line(
            df,
            x='Year',
            y='Annual CO2 emissions including land-use change',
            color='Entity',
            title='Annual CO2 Emissions Over Time',
            labels={'Annual CO2 emissions (tonnes)': 'CO2 Emissions (tonnes)', 'Year': 'Year'},
        )
        fig.update_layout(
            width=800,
            height=600,
            xaxis_title="Year",
            yaxis_title="CO2 Emissions (tonnes)",
        )
        st.plotly_chart(fig)
        st.divider()  
    elif choice == "Add Today's Data":
        add_daily_data()
    elif choice == "View Daily Data":
        view_data('daily')
    elif choice == "Weekly Overview":
        view_data('weekly')
    elif choice == "Monthly Overview":
        view_data('monthly')
    elif choice == "Yearly Overview":
        view_data('yearly')
    elif choice == "Graphical Data":
        # Adding Per capita CO₂ emissions Data graph
        st.markdown("### 🌐 *Per capita CO₂ emissions*")
        st.write("Below is a graph showing Carbon dioxide (CO₂) emissions from fossil fuels and industry from *Our World in Data*:")
        # Fetch the data
        try:
            df = pd.read_csv("percapita.csv", encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv("percapita.csv", encoding='ISO-8859-1')




        # Clean and filter the data for better visualization
        df = df[df['Year'] >= 1750]  # Filter for years from 1750 onwards
        fig = px.line(
            df,
            x='Year',
            y='Annual CO2 emissions (per capita)',
            color='Entity',
            title='Per capita CO₂ emissions',
            labels={'Annual CO2 emissions (tonnes)': 'CO2 Emissions (tonnes)', 'Year': 'Year'},
        )
        fig.update_layout(
            width=800,
            height=600,
            xaxis_title="Year",
            yaxis_title="CO2 Emissions (tonnes)",
        )
        st.plotly_chart(fig)
        st.divider()

        # Adding Annual CO₂ emissions by world region Data graph
        st.markdown("### 🌐 *Annual CO₂ emissions by world region*")
        st.write('''Below is a graph of Emissions from fossil fuels and industry. International aviation and shipping are included as separate entities, as they are not included in
any country's emissions from *Our World in Data*:''')
        # Fetch the data
        try:
            df = pd.read_csv("Annual CO₂ emissions by world region.csv", encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv("Annual CO₂ emissions by world region.csv", encoding='ISO-8859-1')




        # Clean and filter the data for better visualization
        df = df[df['Year'] >= 1750]  # Filter for years from 1750 onwards
        fig = px.line(
            df,
            x='Year',
            y='Annual CO2 emissions',
            color='Entity',
            title='Annual CO₂ emissions by world region',
            labels={'Annual CO2 emissions (tonnes)': 'CO2 Emissions (tonnes)', 'Year': 'Year'},
        )
        fig.update_layout(
            width=800,
            height=600,
            xaxis_title="Year",
            yaxis_title="CO2 Emissions (tonnes)",
        )
        st.plotly_chart(fig)
        st.divider()

        

        # Title and description
        st.markdown("### 🌍 *Greenhouse Gas Emissions by Sector*")
        st.write("This graph shows greenhouse gas emissions by various sectors over time.")

        # Load the dataset
        file_path = "green house gases.csv"  # Update with your actual path
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding='ISO-8859-1')

        # Filter for years from 1990 onwards
        df = df[df['Year'] >= 1990]

        # Melt the dataframe to have a long format for better visualization
        emission_columns = [
            'Greenhouse gas emissions from agriculture',
            'Greenhouse gas emissions from land use change and forestry',
            'Greenhouse gas emissions from waste',
            'Greenhouse gas emissions from buildings',
            'Greenhouse gas emissions from industry',
            'Greenhouse gas emissions from manufacturing and construction',
            'Greenhouse gas emissions from transport',
            'Greenhouse gas emissions from electricity and heat',
            'Fugitive emissions of greenhouse gases from energy production',
            'Greenhouse gas emissions from other fuel combustion',
            'Greenhouse gas emissions from bunker fuels',
        ]
        df_long = df.melt(
            id_vars=['Entity', 'Year'],
            value_vars=emission_columns,
            var_name='Emission Source',
            value_name='Emissions (tonnes)'
        )

        # Create a line graph
        fig = px.line(
            df_long,
            x='Year',
            y='Emissions (tonnes)',
            color='Emission Source',
            title='Greenhouse Gas Emissions by Sector',
            labels={
                'Year': 'Year',
                'Emissions (tonnes)': 'Emissions (tonnes)',
                'Emission Source': 'Emission Source'
            }
        )

        # Update layout for better readability
        fig.update_layout(
            width=900,
            height=600,
            xaxis_title="Year",
            yaxis_title="Emissions (tonnes)",
            legend_title="Emission Source"
        )

        # Display the plot
        st.plotly_chart(fig)
        st.divider()  

        
    elif choice == "Solution":
        st.subheader("To reduce carbon emissions, certain plants are more effective at absorbing CO2. Here's a list of plants and the recommended number to plant based on their carbon absorption potential:")
        st.write("""
            1. *Tree Planting (Large Trees)*:
            - *Oak*: Absorbs about 48 pounds of CO2 per year.
            - *Maple*: Absorbs around 30-40 pounds of CO2 per year.
            - *Pine*: Absorbs 30-40 pounds of CO2 per year.
            - *Recommendation: Plant **1-2 large trees* per person for significant impact.

            2. *Smaller Plants (Bushes & Shrubs)*:
            - *Lavender*: Absorbs around 7 pounds of CO2 per year.
            - *Bamboo*: Absorbs up to 40% more CO2 than trees in the same area.
            - *Cactus*: Absorbs around 2 pounds of CO2 per year.
            - *Recommendation: Plant **5-10 bushes/shrubs* or *10+ small plants* like lavender or bamboo for smaller space.

            3. *Ground Cover Plants*:
            - *Clover*: Absorbs 5-10 pounds of CO2 per year.
            - *Grass*: Absorbs about 10 pounds of CO2 per year.
            - *Recommendation: Plant **15-20 ground cover plants* for carbon sequestration in large outdoor areas.

            By planting a mix of trees, shrubs, and ground cover plants, individuals can help offset carbon emissions effectively.
        """)

        col1, col2, col3 = st.columns([1, 5, 1])  # Adjust the column widths
        with col2:
            st.image("c02.jpg", width=600)


        st.subheader("Reducing carbon emissions from the agriculture sector on a personal level:")
        st.write("""
            1. *Adopt a Plant-Based Diet*: Reduce meat and dairy consumption, especially red meat, as livestock farming is a major source of methane emissions.

            2. *Minimize Food Waste*: Plan meals, store food properly, and compost organic waste instead of sending it to landfills.

            3. *Choose Local and Seasonal Foods*: Buy from local farmers to reduce transportation emissions and prefer seasonal produce to avoid energy-intensive farming practices.

            4. *Support Sustainable Farming*: Purchase organic or sustainably grown products that avoid synthetic fertilizers and pesticides.

            5. *Grow Your Own Food*: Start a small garden to produce fruits, vegetables, or herbs, reducing the need for commercially grown produce.

            By making these changes, individuals can contribute to reducing emissions associated with agriculture.
        """)



        st.subheader("To reduce carbon emissions from the garbage sector on a personal level:")
        st.write("""
            1. *Reduce Waste*: Avoid single-use items and buy products with minimal packaging.  
            2. *Reuse*: Use durable, reusable items like bags, bottles, and containers.  
            3. *Recycle*: Properly separate and recycle paper, plastic, metal, and glass.  
            4. *Compost*: Turn organic waste into compost instead of sending it to landfills.  
            5. *Donate and Repurpose*: Give away or upcycle items instead of throwing them away.  

            These practices minimize landfill waste and lower methane emissions from decomposing trash.
        """)

        st.subheader("Other Methods For Reducing Your Carbon Footprint")
        st.write("""
        **Reducing your personal carbon footprint involves making small, consistent changes to your daily habits. Here are practical steps you can take:**

        **1. Reduce Energy Use at Home**
        - **Switch to Renewable Energy**: Opt for solar panels or subscribe to green energy plans if available.
        - **Energy-Efficient Appliances**: Use devices with high energy-efficiency ratings (e.g., 5-star rated appliances in India).
        - **Conserve Energy**: Turn off lights, fans, and electronics when not in use. Use LEDs instead of incandescent bulbs.

        **2. Choose Sustainable Transportation**
        - **Public Transport**: Use buses, trains, or metros instead of personal vehicles.
        - **Carpool or Rideshare**: Share rides to reduce fuel use.
        - **Electric or Hybrid Vehicles**: Invest in EVs or hybrids to cut emissions.
        - **Walk or Bike**: Opt for non-motorized transport for short distances.

        **3. Minimize Waste**
        - **Reduce, Reuse, Recycle**: Avoid single-use plastics and recycle whenever possible.
        - **Composting**: Compost food and garden waste to reduce methane emissions from landfills.
        - **Buy Responsibly**: Choose products with minimal packaging or made from recycled materials.

        **4. Opt for Sustainable Food Choices**
        - **Eat Less Meat and Dairy**: Plant-based diets generally have a lower carbon footprint.
        - **Buy Local and Seasonal**: Reduce transportation emissions by purchasing locally grown produce.
        - **Avoid Food Waste**: Plan meals and store food properly to minimize waste.

        **5. Save Water**
        - **Fix Leaks**: Repair leaking faucets to conserve water and energy used for heating.
        - **Efficient Fixtures**: Install low-flow showerheads and dual-flush toilets.

        **6. Support Green Initiatives**
        - **Plant Trees**: Engage in tree-planting drives to offset emissions.
        - **Offset Programs**: Purchase carbon offsets for unavoidable emissions.

        **7. Educate and Advocate**
        - **Spread Awareness**: Encourage others to adopt sustainable habits.
        - **Support Policies**: Vote for policies promoting renewable energy and sustainability
                 
        **By adopting these practices, you can significantly lower your carbon emissions while contributing to a healthier planet. Small changes, when multiplied by millions, make a big impact!**
        """)


        st.subheader("Video 1: Climate Change and Global Warming: Explained in Simple Words for Beginners")
        st.video("https://www.youtube.com/watch?v=G9t__9Tmwv4&t=70s")

        st.subheader("Video 2: One Earth - Environmental Short Film")
        st.video("https://www.youtube.com/watch?v=QQYgCxu988s&list=WL&index=2")

        st.subheader("Video 3: How to Reduce Your Carbon Footprint")
        st.video("https://www.youtube.com/watch?v=J_iDcKDAwbA")

        

def add_daily_data():
    st.subheader("Add Today's Data")

    # Check if data has already been entered for today
    user_id = st.session_state['user_id']
    existing_data = session.query(CarbonData).filter_by(user_id=user_id, date=date.today()).first()
    if existing_data:
        st.warning("You have already submitted data for today. Please come back tomorrow.")
        return

    electricity_kwh = st.number_input("Electricity consumption (KWh)", min_value=0.0, format="%.2f")
    vehicle_type = st.selectbox("Vehicle Used", ["Two-wheeler", "Four-wheeler", "EV"])
    distance_km = st.number_input("Distance traveled (km)", min_value=0.0, format="%.2f")
    diet_type = st.selectbox("Diet Type", ["Vegetarian", "Non-Vegetarian"])
    meals = st.number_input("Number of meals", min_value=1, step=1)
    garbage_kg = st.number_input("Garbage generated (Kg)", min_value=0.0, format="%.2f")

    if st.button("Submit"):
        new_data = CarbonData(
            user_id=user_id,
            electricity_kwh=electricity_kwh,
            vehicle_type=vehicle_type,
            distance_km=distance_km,
            diet_type=diet_type,
            meals=meals,
            garbage_kg=garbage_kg
        )
        session.add(new_data)
        session.commit()
        st.success("Data submitted successfully!")

def view_data(period):
    user_id = st.session_state['user_id']
    query = session.query(CarbonData).filter_by(user_id=user_id)

    if period == 'daily':
        query = query.filter(CarbonData.date == date.today())
    elif period == 'weekly':
        query = query.filter(CarbonData.date >= date.today() - pd.Timedelta(days=7))
    elif period == 'monthly':
        query = query.filter(CarbonData.date >= date.today() - pd.Timedelta(days=30))
    elif period == 'yearly':
        query = query.filter(CarbonData.date >= date.today() - pd.Timedelta(days=365))

    data = pd.read_sql(query.statement, session.bind)

    if not data.empty:
        # Calculate CO2 in kilograms (kg)
        data['CO2 Generated (kg)'] = (
            data['electricity_kwh'] * 0.85 +
            data['distance_km'] * 0.12 +
            data['meals'] * (5 if data['diet_type'].str.contains('Non-Vegetarian').any() else 3) +
            data['garbage_kg'] * 0.06
        ).round(2)

        # Split the data into below and above 5.5 kg CO2
        data['Below_5.5'] = data['CO2 Generated (kg)'].apply(lambda x: min(x, 5.5))
        data['Above_5.5'] = data['CO2 Generated (kg)'].apply(lambda x: max(0, x - 5.5))

        # Combine input columns with the calculated columns
        display_columns = [
            'date', 'electricity_kwh', 'vehicle_type', 'distance_km', 'diet_type',
            'meals', 'garbage_kg', 'CO2 Generated (kg)', 'Below_5.5', 'Above_5.5'
        ]
        st.dataframe(data[display_columns])

        # Plot the stacked bar chart
        fig = px.bar(
            data,
            x='date',
            y=['Below_5.5', 'Above_5.5'],
            title='Carbon Dioxide Over Time (Kg)',
            labels={'value': 'CO2 Generated (Kg)', 'date': 'Date'},
            color_discrete_map={'Below_5.5': 'green', 'Above_5.5': 'red'},
        )
        fig.update_layout(
            barmode='stack',  # Stack the bars
            bargap=0.7,       # Adjust bar gap
            width=600,        # Plot width
            height=600,       # Plot height
        )
        fig.update_traces(
            hovertemplate='%{x}<br>%{y:.2f} kg'  # Custom hover info
        )
        st.plotly_chart(fig)
    else:
        st.warning(f"No data available for {period} view.")







if __name__ == "__main__":
    add_local_background("g wallpaper.jpg")
    main()
 