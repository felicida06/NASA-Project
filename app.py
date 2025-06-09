import streamlit as st
import pandas as pd
import pymysql
import datetime

st.title("NASA PROJECT ☄️ ")

myconnection = pymysql.connect(host = '127.0.0.1',user='root',passwd='Alby@0308',database = "near_earth_objects")
cur = myconnection.cursor()

from streamlit_option_menu import option_menu

with st.sidebar:
    selected = option_menu("Asteroid Approaches", ["Home","Filter criteria", 'Queries'], 
        icons=['house', 'gear'], menu_icon="cast", default_index=1)
    

if selected == "Home":
                    
                    st.write("NASA - Near earth object ☄️ Project")

if selected == "Filter criteria":
                             start_date = st.date_input("Start Date", datetime.date(2024, 1, 1))
                             end_date = st.date_input("End Date", datetime.date(2024, 12, 31))
                             min_mag = st.slider("magmitude",13.8,32.61,(13.8,32.61))
                             lunar_dist = st.slider("miss_distance_lunar", 0.5, 2.0, (0.5, 2.0))
                             astro = st.slider("miss_distance_ast", 0.0, 2.0, (0.0, 2.0))
                             velocity = st.slider("Relative Velocity (km/h)",1418.21, 173071.83,value=(1418.21, 173071.83))
                             dia_min = st.slider("Min Estimated Diameter (km)", 0.00, 4.62, (0.00, 4.62))
                             dia_max = st.slider("Max Estimated Diameter (km)", 0.00, 10.33, (0.00, 10.33))
                             hazardous = st.selectbox("Hazardous?", [ "1", "0"])
                             

                             
                             button = st.button("Filter")
                             query ="""
                                    SELECT  
                                        asteroids.id,
                                        asteroids.name,
                                        asteroids.absolute_magnitude_h,
                                        asteroids.estimated_diameter_min_km,
                                        asteroids.estimated_diameter_max_km,
                                        asteroids.is_potentially_hazardous_asteroid,
                                        close_approach.close_approach_date,
                                        close_approach.relative_velocity_kmph,
                                        close_approach.miss_distance_ast,
                                        close_approach.miss_distance_km,
                                        close_approach.miss_distance_lunar,
                                        close_approach.orbiting_body
                                    FROM asteroids 
                                    JOIN close_approach ON asteroids.id = close_approach.neo_reference_id 
                                    WHERE asteroids.absolute_magnitude_h BETWEEN %s AND %s
                                    AND asteroids.estimated_diameter_min_km BETWEEN %s AND %s
                                    AND asteroids.estimated_diameter_max_km BETWEEN %s AND %s
                                    AND close_approach.relative_velocity_kmph BETWEEN %s AND %s
                                    AND close_approach.close_approach_date BETWEEN %s AND %s
                                    AND close_approach.miss_distance_ast BETWEEN %s AND %s
                                    AND close_approach.miss_distance_lunar BETWEEN %s AND %s
                                    AND asteroids.is_potentially_hazardous_asteroid = %s
                                    """
                             params = [
                                 min_mag[0],min_mag[1],
                                 dia_min[0],dia_min[1],
                                 dia_max[0],dia_max[1],
                                 velocity[0],velocity[1],
                                 start_date, end_date,
                                 astro[0],astro[1],
                                 lunar_dist[0],lunar_dist[1],
                                 hazardous]
                             
                             if button:
                                 cur.execute(query,params)
                                 rows = cur.fetchall()
                             
                                 columns = [desc[0] for desc in cur.description]
                             
                                 df = pd.DataFrame(rows,columns=columns)
                                 
                                 st.subheader("Filtered asteroid Results")
                                 st.dataframe(df)
                            
                              

if selected == 'Queries':  

                    options = st.selectbox("Queries",["1.Count how many times each asteroid has approached Earth",
                                                    "2.Average velocity of each asteroid over multiple approaches",
                                                    "3.List top 10 fastest asteroids",
                                                     "4.Find potentially hazardous asteroids that have approached Earth more than 3 times",
                                                     "5.Find the month with the most asteroid approaches",
                                                     "6.Get the asteroid with the fastest ever approach speed",
                                                     "7.Sort asteroids by maximum estimated diameter (descending)",
                                                     "8.An asteroid whose closest approach is getting nearer over time",
                                                     "9.Display the name of each asteroid along with the date and miss distance of its closest approach to Earth",
                                                     "10.List names of asteroids that approached Earth with velocity > 50,000 km/h",
                                                     "11.Count how many approaches happened per month",
                                                     "12.Find asteroid with the highest brightness",
                                                     "13.Get number of hazardous vs non-hazardous asteroids",
                                                     "14.Find asteroids that passed closer than the Moon (lesser than 1 LD), along with their close approach date and distance",
                                                     "15.Find asteroids that came within 0.05 AU",
                                                     "16.List asteroids with the largest size range",
                                                     "17.Find asteroids that only ever approached once",
                                                     "18.Find the average estimated size of all asteroids",
                                                     "19.list hazaedous assteroids with diamoter estimates over 1000km",
                                                     "20.Count how many hazardous asteroids approached earth each year"],placeholder='Choose an option..',index=None)
                    if options == "1.Count how many times each asteroid has approached Earth":
                                            cur.execute('SELECT name, count(*) AS approach_count FROM asteroids GROUP BY name LIMIT 10')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description] 
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data) 
                    elif options == "2.Average velocity of each asteroid over multiple approaches":
                                            cur.execute('SELECT a.name, AVG(CAST(c.relative_velocity_kmph AS DECIMAL(10,2))) AS avg_velocity FROM (SELECT DISTINCT id, name FROM asteroids) AS a JOIN close_approach AS c ON a.id = c.neo_reference_id GROUP BY a.name LIMIT 10')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data) 
                    elif options == "3.List top 10 fastest asteroids":
                                            cur.execute('SELECT a.name, c.relative_velocity_kmph FROM asteroids AS a JOIN close_approach AS c ON a.id = c.neo_reference_id ORDER BY c.relative_velocity_kmph DESC LIMIT 10')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "4.Find potentially hazardous asteroids that have approached Earth more than 3 times":
                                            cur.execute('SELECT a.name, COUNT(*) AS approach_count FROM asteroids AS a JOIN close_approach AS c ON a.id = c.neo_reference_id WHERE a.is_potentially_hazardous_asteroid = 1 GROUP BY a.name HAVING COUNT(*) > 3 LIMIT 5')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "5.Find the month with the most asteroid approaches":
                                            cur.execute('SELECT MONTH(close_approach_date) AS approach_month, COUNT(*) AS total_approaches FROM close_approach GROUP BY MONTH(close_approach_date) ORDER BY total_approaches DESC LIMIT 2')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "6.Get the asteroid with the fastest ever approach speed":
                                            cur.execute('SELECT a.name, c.relative_velocity_kmph FROM asteroids AS a JOIN close_approach AS c ON a.id = c.neo_reference_id ORDER BY c.relative_velocity_kmph DESC LIMIT 1')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "7.Sort asteroids by maximum estimated diameter (descending)":
                                            cur.execute('SELECT name, estimated_diameter_max_km FROM asteroids ORDER BY estimated_diameter_max_km DESC LIMIT 5')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "8.An asteroid whose closest approach is getting nearer over time":
                                            cur.execute('SELECT a.name, c.close_approach_date, c.miss_distance_km FROM asteroids AS a JOIN close_approach AS c ON a.id = c.neo_reference_id ORDER BY a.name, c.close_approach_date LIMIT 5')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "9.Display the name of each asteroid along with the date and miss distance of its closest approach to Earth":
                                            cur.execute('SELECT a.name, c.close_approach_date, c.miss_distance_km FROM asteroids AS a JOIN close_approach AS c ON a.id = c.neo_reference_id JOIN (SELECT neo_reference_id, MIN(miss_distance_km) AS min_miss_distance FROM close_approach GROUP BY neo_reference_id) AS sub ON c.neo_reference_id = sub.neo_reference_id AND c.miss_distance_km = sub.min_miss_distance ORDER BY c.miss_distance_km ASC LIMIT 5')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "10.List names of asteroids that approached Earth with velocity > 50,000 km/h":
                                            cur.execute('SELECT DISTINCT a.name FROM asteroids AS a JOIN close_approach AS c ON a.id = c.neo_reference_id WHERE c.relative_velocity_kmph > 50000 LIMIT 5')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "11.Count how many approaches happened per month":
                                            cur.execute('SELECT MONTH(close_approach_date) AS month, COUNT(*) AS total_approaches FROM close_approach GROUP BY MONTH(close_approach_date) ORDER BY month')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "12.Find asteroid with the highest brightness":
                                            cur.execute('SELECT name, absolute_magnitude_h FROM asteroids ORDER BY absolute_magnitude_h ASC LIMIT 5')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "13.Get number of hazardous vs non-hazardous asteroids":
                                            cur.execute('SELECT is_potentially_hazardous_asteroid AS hazardous_status, COUNT(*) AS total FROM asteroids GROUP BY is_potentially_hazardous_asteroid')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "14.Find asteroids that passed closer than the Moon (lesser than 1 LD), along with their close approach date and distance":
                                            cur.execute('SELECT a.name, c.close_approach_date, c.miss_distance_lunar FROM asteroids AS a JOIN close_approach AS c ON a.id = c.neo_reference_id WHERE c.miss_distance_lunar < 1 ORDER BY c.miss_distance_lunar ASC LIMIT 1')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "15.Find asteroids that came within 0.05 AU":
                                            cur.execute('SELECT a.name, c.close_approach_date, c.miss_distance_ast FROM asteroids AS a JOIN close_approach AS c ON a.id = c.neo_reference_id WHERE c.miss_distance_ast < 0.05 ORDER BY c.miss_distance_ast ASC LIMIT 3')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "16.List asteroids with the largest size range":
                                            cur.execute('SELECT name, estimated_diameter_max_km - estimated_diameter_min_km AS size_range FROM asteroids ORDER BY size_range DESC LIMIT 3')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "17.Find asteroids that only ever approached once":
                                            cur.execute('SELECT a.name, COUNT(c.neo_reference_id) AS approach_count FROM asteroids AS a JOIN close_approach AS c ON a.id = c.neo_reference_id GROUP BY a.name HAVING COUNT(c.neo_reference_id) = 1')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "18.Find the average estimated size of all asteroids":
                                            cur.execute('SELECT AVG((estimated_diameter_min_km + estimated_diameter_max_km)/2) AS avg_estimated_diameter_km FROM asteroids')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "19.list hazaedous assteroids with diamoter estimates over 1000km":
                                            cur.execute('SELECT name, estimated_diameter_max_km FROM asteroids WHERE is_potentially_hazardous_asteroid = TRUE AND estimated_diameter_max_km > 1000')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
                    elif options == "20.Count how many hazardous asteroids approached earth each year":
                                            cur.execute('SELECT YEAR(c.close_approach_date) AS approach_year, COUNT(*) AS hazardous_approaches FROM asteroids AS a JOIN close_approach AS c ON a.id = c.neo_reference_id WHERE a.is_potentially_hazardous_asteroid = TRUE GROUP BY YEAR(c.close_approach_date) ORDER BY approach_year')
                                            result = cur.fetchall()
                                            columns = [desc[0] for desc in cur.description]
                                            data = pd.DataFrame(result,columns=columns)
                                            st.dataframe(data)
myconnection.commit()